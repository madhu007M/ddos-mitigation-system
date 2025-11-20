"""
Unit tests for Traffic Monitor
"""
import unittest
import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.traffic_monitor import TrafficMonitor


class TestTrafficMonitor(unittest.TestCase):
    """Test cases for TrafficMonitor"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.monitor = TrafficMonitor(
            suspicious_threshold=10,
            detection_window=5,
            alert_threshold=3
        )
    
    def test_initialization(self):
        """Test monitor initialization"""
        self.assertEqual(self.monitor.suspicious_threshold, 10)
        self.assertEqual(self.monitor.detection_window, 5)
        self.assertEqual(self.monitor.alert_threshold, 3)
    
    def test_records_requests(self):
        """Test request recording"""
        test_ip = "192.168.1.1"
        
        for i in range(5):
            self.monitor.record_request(test_ip, "/api/data", "GET")
        
        stats = self.monitor.get_stats()
        self.assertGreaterEqual(stats['total_requests'], 5)
    
    def test_detects_suspicious_activity(self):
        """Test detection of suspicious activity"""
        test_ip = "192.168.1.2"
        
        # Generate high rate of requests
        for i in range(60):
            self.monitor.record_request(test_ip, "/api/data", "GET")
        
        is_suspicious, details = self.monitor.is_suspicious(test_ip)
        self.assertTrue(is_suspicious)
        self.assertIsNotNone(details)
        self.assertIn('request_rate', details)
    
    def test_normal_traffic_not_suspicious(self):
        """Test that normal traffic is not flagged"""
        test_ip = "192.168.1.3"
        
        for i in range(5):
            self.monitor.record_request(test_ip, "/api/data", "GET")
            time.sleep(0.1)
        
        is_suspicious, details = self.monitor.is_suspicious(test_ip)
        self.assertFalse(is_suspicious)
    
    def test_tracks_multiple_ips(self):
        """Test tracking multiple IPs"""
        ip1 = "192.168.1.4"
        ip2 = "192.168.1.5"
        
        for i in range(10):
            self.monitor.record_request(ip1, "/api/data", "GET")
            self.monitor.record_request(ip2, "/api/endpoint", "POST")
        
        stats = self.monitor.get_stats()
        self.assertGreaterEqual(stats['active_ips'], 2)
    
    def test_generates_alerts(self):
        """Test alert generation"""
        test_ip = "192.168.1.6"
        
        # Generate enough violations to trigger alerts
        for i in range(100):
            self.monitor.record_request(test_ip, "/api/data", "GET")
        
        alerts = self.monitor.get_recent_alerts(10)
        self.assertGreater(len(alerts), 0)
    
    def test_severity_calculation(self):
        """Test severity level calculation"""
        test_ip = "192.168.1.7"
        
        # Generate critical level traffic
        for i in range(200):
            self.monitor.record_request(test_ip, "/api/data", "GET")
        
        is_suspicious, details = self.monitor.is_suspicious(test_ip)
        if is_suspicious:
            self.assertIn('severity', details)
            self.assertIn(details['severity'], ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'])
    
    def test_reset(self):
        """Test monitor reset"""
        test_ip = "192.168.1.8"
        
        for i in range(10):
            self.monitor.record_request(test_ip, "/api/data", "GET")
        
        self.monitor.reset()
        
        stats = self.monitor.get_stats()
        self.assertEqual(stats['total_requests'], 0)
        self.assertEqual(stats['total_alerts'], 0)


if __name__ == '__main__':
    unittest.main()
