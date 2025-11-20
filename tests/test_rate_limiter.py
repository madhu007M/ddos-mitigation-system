"""
Unit tests for Rate Limiter
"""
import unittest
import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.rate_limiter import RateLimiter


class TestRateLimiter(unittest.TestCase):
    """Test cases for RateLimiter"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.limiter = RateLimiter(max_requests=10, time_window=5, block_duration=10)
    
    def test_initialization(self):
        """Test rate limiter initialization"""
        self.assertEqual(self.limiter.max_requests, 10)
        self.assertEqual(self.limiter.time_window, 5)
        self.assertEqual(self.limiter.block_duration, 10)
    
    def test_allows_requests_under_limit(self):
        """Test that requests under limit are allowed"""
        test_ip = "192.168.1.1"
        
        for i in range(5):
            is_allowed, reason = self.limiter.is_allowed(test_ip)
            self.assertTrue(is_allowed)
            self.assertIsNone(reason)
    
    def test_blocks_requests_over_limit(self):
        """Test that requests over limit are blocked"""
        test_ip = "192.168.1.2"
        
        # Make requests up to the limit
        for i in range(10):
            is_allowed, reason = self.limiter.is_allowed(test_ip)
            self.assertTrue(is_allowed)
        
        # Next request should be blocked
        is_allowed, reason = self.limiter.is_blocked(test_ip)
        self.assertTrue(is_allowed)
    
    def test_tracks_multiple_ips(self):
        """Test tracking multiple IPs independently"""
        ip1 = "192.168.1.3"
        ip2 = "192.168.1.4"
        
        # Make requests from both IPs
        for i in range(5):
            is_allowed1, _ = self.limiter.is_allowed(ip1)
            is_allowed2, _ = self.limiter.is_allowed(ip2)
            self.assertTrue(is_allowed1)
            self.assertTrue(is_allowed2)
        
        # Both should have 5 requests
        self.assertEqual(self.limiter.get_request_count(ip1), 5)
        self.assertEqual(self.limiter.get_request_count(ip2), 5)
    
    def test_manual_block_and_unblock(self):
        """Test manual IP blocking and unblocking"""
        test_ip = "192.168.1.5"
        
        # Block IP
        self.limiter.block_ip(test_ip, duration=5)
        self.assertTrue(self.limiter.is_blocked(test_ip))
        
        # Unblock IP
        self.limiter.unblock_ip(test_ip)
        self.assertFalse(self.limiter.is_blocked(test_ip))
    
    def test_get_stats(self):
        """Test statistics retrieval"""
        test_ip = "192.168.1.6"
        
        # Make some requests
        for i in range(3):
            self.limiter.is_allowed(test_ip)
        
        stats = self.limiter.get_stats()
        self.assertIn('total_tracked_ips', stats)
        self.assertIn('blocked_ips', stats)
        self.assertGreaterEqual(stats['total_tracked_ips'], 1)
    
    def test_reset(self):
        """Test system reset"""
        test_ip = "192.168.1.7"
        
        # Make requests and block
        for i in range(5):
            self.limiter.is_allowed(test_ip)
        self.limiter.block_ip(test_ip)
        
        # Reset
        self.limiter.reset()
        
        # Check everything is cleared
        stats = self.limiter.get_stats()
        self.assertEqual(stats['total_tracked_ips'], 0)
        self.assertEqual(stats['blocked_ips'], 0)


if __name__ == '__main__':
    unittest.main()
