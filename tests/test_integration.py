"""
Integration tests for DDoS Mitigation System
"""
import unittest
import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.mitigation_system import DDoSMitigationSystem


class TestDDoSMitigationSystem(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.system = DDoSMitigationSystem()
    
    def test_system_initialization(self):
        """Test system initializes correctly"""
        self.assertIsNotNone(self.system.config)
        self.assertIsNotNone(self.system.rate_limiter)
        self.assertIsNotNone(self.system.traffic_monitor)
        self.assertIsNotNone(self.system.ip_filter)
    
    def test_allows_normal_requests(self):
        """Test that normal requests are allowed"""
        test_ip = "192.168.1.1"
        
        for i in range(5):
            is_allowed, reason, details = self.system.process_request(test_ip, "/api/data", "GET")
            self.assertTrue(is_allowed)
    
    def test_blocks_ddos_attack(self):
        """Test that DDoS attacks are blocked"""
        test_ip = "10.0.0.1"
        
        allowed_count = 0
        blocked_count = 0
        
        # Simulate rapid requests
        for i in range(150):
            is_allowed, reason, details = self.system.process_request(test_ip, "/api/data", "GET")
            if is_allowed:
                allowed_count += 1
            else:
                blocked_count += 1
                break
        
        # Should be blocked before all requests complete
        self.assertGreater(blocked_count, 0)
        self.assertLess(allowed_count, 150)
    
    def test_whitelist_bypass(self):
        """Test that whitelisted IPs bypass rate limiting"""
        test_ip = "192.168.1.2"
        
        # Whitelist the IP
        self.system.whitelist_ip(test_ip)
        
        # Make many rapid requests
        for i in range(200):
            is_allowed, reason, details = self.system.process_request(test_ip, "/api/data", "GET")
            self.assertTrue(is_allowed, f"Whitelisted IP should not be blocked at request {i+1}")
    
    def test_manual_block(self):
        """Test manual IP blocking"""
        test_ip = "10.0.0.2"
        
        # Block the IP
        self.system.block_ip(test_ip, duration=5)
        
        # Request should be blocked
        is_allowed, reason, details = self.system.process_request(test_ip, "/api/data", "GET")
        self.assertFalse(is_allowed)
    
    def test_manual_unblock(self):
        """Test manual IP unblocking"""
        test_ip = "10.0.0.3"
        
        # Block then unblock
        self.system.block_ip(test_ip, duration=10)
        self.system.unblock_ip(test_ip)
        
        # Request should be allowed
        is_allowed, reason, details = self.system.process_request(test_ip, "/api/data", "GET")
        self.assertTrue(is_allowed)
    
    def test_get_stats(self):
        """Test statistics retrieval"""
        test_ip = "192.168.1.3"
        
        # Generate some traffic
        for i in range(10):
            self.system.process_request(test_ip, "/api/data", "GET")
        
        stats = self.system.get_stats()
        
        self.assertIn('rate_limiter', stats)
        self.assertIn('traffic_monitor', stats)
        self.assertIn('ip_filter', stats)
    
    def test_get_recent_alerts(self):
        """Test alert retrieval"""
        test_ip = "10.0.0.4"
        
        # Generate suspicious traffic
        for i in range(100):
            self.system.process_request(test_ip, "/api/data", "GET")
        
        alerts = self.system.get_recent_alerts(5)
        self.assertIsInstance(alerts, list)
    
    def test_multiple_ips_independently(self):
        """Test that multiple IPs are tracked independently"""
        ip1 = "192.168.1.4"
        ip2 = "192.168.1.5"
        ip3 = "192.168.1.6"
        
        # IP1: Normal traffic
        for i in range(5):
            is_allowed, _, _ = self.system.process_request(ip1, "/api/data", "GET")
            self.assertTrue(is_allowed)
        
        # IP2: Attack traffic
        for i in range(150):
            is_allowed, _, _ = self.system.process_request(ip2, "/api/data", "GET")
            if not is_allowed:
                break
        
        # IP3: Normal traffic (should still work)
        for i in range(5):
            is_allowed, _, _ = self.system.process_request(ip3, "/api/data", "GET")
            self.assertTrue(is_allowed, "IP3 should not be affected by IP2's blocking")


if __name__ == '__main__':
    unittest.main()
