"""
Traffic Monitor Module
Detects suspicious patterns and potential DDoS attacks
"""
import time
from typing import Dict, List, Optional
from collections import defaultdict
import threading


class TrafficMonitor:
    """Monitors traffic patterns and detects anomalies"""
    
    def __init__(self, suspicious_threshold: int, detection_window: int, alert_threshold: int):
        """
        Initialize traffic monitor
        
        Args:
            suspicious_threshold: Requests per second to be considered suspicious
            detection_window: Time window for detection (seconds)
            alert_threshold: Number of violations before triggering alert
        """
        self.suspicious_threshold = suspicious_threshold
        self.detection_window = detection_window
        self.alert_threshold = alert_threshold
        
        # Track requests per IP
        self.ip_requests: Dict[str, List[float]] = defaultdict(list)
        # Track violations per IP
        self.ip_violations: Dict[str, int] = defaultdict(int)
        # Track alerts
        self.alerts: List[Dict] = []
        # Thread lock
        self.lock = threading.Lock()
    
    def record_request(self, ip: str, endpoint: str = "/", method: str = "GET"):
        """
        Record a request and analyze traffic pattern
        
        Args:
            ip: IP address
            endpoint: Request endpoint
            method: HTTP method
        """
        with self.lock:
            current_time = time.time()
            
            # Clean old requests
            self.ip_requests[ip] = [
                req_time for req_time in self.ip_requests[ip]
                if current_time - req_time < self.detection_window
            ]
            
            # Add new request
            self.ip_requests[ip].append(current_time)
            
            # Check for suspicious activity
            request_rate = len(self.ip_requests[ip]) / self.detection_window
            
            if request_rate > self.suspicious_threshold:
                self.ip_violations[ip] += 1
                
                # Trigger alert if threshold exceeded
                if self.ip_violations[ip] >= self.alert_threshold:
                    self._trigger_alert(ip, request_rate, endpoint, method)
    
    def _trigger_alert(self, ip: str, request_rate: float, endpoint: str, method: str):
        """Trigger a DDoS alert"""
        alert = {
            'timestamp': time.time(),
            'ip': ip,
            'request_rate': round(request_rate, 2),
            'endpoint': endpoint,
            'method': method,
            'violation_count': self.ip_violations[ip],
            'severity': self._calculate_severity(request_rate)
        }
        self.alerts.append(alert)
        
        # Keep only last 100 alerts
        if len(self.alerts) > 100:
            self.alerts.pop(0)
    
    def _calculate_severity(self, request_rate: float) -> str:
        """Calculate severity level based on request rate"""
        if request_rate > self.suspicious_threshold * 10:
            return "CRITICAL"
        elif request_rate > self.suspicious_threshold * 5:
            return "HIGH"
        elif request_rate > self.suspicious_threshold * 2:
            return "MEDIUM"
        else:
            return "LOW"
    
    def is_suspicious(self, ip: str) -> tuple[bool, Optional[Dict]]:
        """
        Check if an IP shows suspicious behavior
        
        Returns:
            Tuple of (is_suspicious, details)
        """
        with self.lock:
            current_time = time.time()
            
            # Clean old requests
            self.ip_requests[ip] = [
                req_time for req_time in self.ip_requests[ip]
                if current_time - req_time < self.detection_window
            ]
            
            if not self.ip_requests[ip]:
                return False, None
            
            request_rate = len(self.ip_requests[ip]) / self.detection_window
            
            if request_rate > self.suspicious_threshold:
                return True, {
                    'request_rate': round(request_rate, 2),
                    'threshold': self.suspicious_threshold,
                    'violations': self.ip_violations[ip],
                    'severity': self._calculate_severity(request_rate)
                }
            
            return False, None
    
    def get_recent_alerts(self, limit: int = 10) -> List[Dict]:
        """Get recent alerts"""
        with self.lock:
            return self.alerts[-limit:]
    
    def get_stats(self) -> Dict:
        """Get traffic monitoring statistics"""
        with self.lock:
            current_time = time.time()
            
            # Calculate overall traffic stats
            total_requests = sum(len(requests) for requests in self.ip_requests.values())
            active_ips = len([ip for ip, requests in self.ip_requests.items() if requests])
            
            suspicious_ips = []
            for ip, requests in self.ip_requests.items():
                if requests:
                    request_rate = len(requests) / self.detection_window
                    if request_rate > self.suspicious_threshold:
                        suspicious_ips.append({
                            'ip': ip,
                            'request_rate': round(request_rate, 2),
                            'violations': self.ip_violations[ip]
                        })
            
            return {
                'total_requests': total_requests,
                'active_ips': active_ips,
                'suspicious_ips_count': len(suspicious_ips),
                'suspicious_ips': suspicious_ips,
                'total_alerts': len(self.alerts),
                'recent_alerts': self.get_recent_alerts(5)
            }
    
    def reset_violations(self, ip: str):
        """Reset violation count for an IP"""
        with self.lock:
            self.ip_violations[ip] = 0
    
    def reset(self):
        """Reset all monitoring data"""
        with self.lock:
            self.ip_requests.clear()
            self.ip_violations.clear()
            self.alerts.clear()
