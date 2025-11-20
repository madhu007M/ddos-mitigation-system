"""
Rate Limiter Module
Implements token bucket algorithm for rate limiting
"""
import time
from typing import Dict, Optional
from collections import defaultdict
import threading


class RateLimiter:
    """Token bucket based rate limiter"""
    
    def __init__(self, max_requests: int, time_window: int, block_duration: int = 300):
        """
        Initialize rate limiter
        
        Args:
            max_requests: Maximum requests allowed per time window
            time_window: Time window in seconds
            block_duration: Duration to block offending IPs (seconds)
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.block_duration = block_duration
        
        # Track requests per IP
        self.requests: Dict[str, list] = defaultdict(list)
        # Track blocked IPs
        self.blocked_ips: Dict[str, float] = {}
        # Thread lock for thread safety
        self.lock = threading.Lock()
    
    def is_allowed(self, ip: str) -> tuple[bool, Optional[str]]:
        """
        Check if request from IP is allowed
        
        Args:
            ip: IP address
            
        Returns:
            Tuple of (is_allowed, reason)
        """
        with self.lock:
            current_time = time.time()
            
            # Check if IP is blocked
            if ip in self.blocked_ips:
                block_expiry = self.blocked_ips[ip]
                if current_time < block_expiry:
                    remaining = int(block_expiry - current_time)
                    return False, f"IP blocked. Unblock in {remaining} seconds"
                else:
                    # Block expired, remove it
                    del self.blocked_ips[ip]
            
            # Clean old requests outside time window
            self.requests[ip] = [
                req_time for req_time in self.requests[ip]
                if current_time - req_time < self.time_window
            ]
            
            # Check rate limit
            if len(self.requests[ip]) >= self.max_requests:
                # Block the IP
                self.blocked_ips[ip] = current_time + self.block_duration
                return False, f"Rate limit exceeded. IP blocked for {self.block_duration} seconds"
            
            # Allow request and record it
            self.requests[ip].append(current_time)
            return True, None
    
    def get_request_count(self, ip: str) -> int:
        """Get current request count for an IP"""
        with self.lock:
            current_time = time.time()
            self.requests[ip] = [
                req_time for req_time in self.requests[ip]
                if current_time - req_time < self.time_window
            ]
            return len(self.requests[ip])
    
    def is_blocked(self, ip: str) -> bool:
        """Check if an IP is currently blocked"""
        with self.lock:
            if ip in self.blocked_ips:
                if time.time() < self.blocked_ips[ip]:
                    return True
                else:
                    del self.blocked_ips[ip]
            return False
    
    def block_ip(self, ip: str, duration: Optional[int] = None):
        """Manually block an IP"""
        with self.lock:
            block_time = duration if duration else self.block_duration
            self.blocked_ips[ip] = time.time() + block_time
    
    def unblock_ip(self, ip: str):
        """Manually unblock an IP"""
        with self.lock:
            if ip in self.blocked_ips:
                del self.blocked_ips[ip]
    
    def get_stats(self) -> Dict:
        """Get current rate limiter statistics"""
        with self.lock:
            current_time = time.time()
            active_blocks = {
                ip: int(expiry - current_time)
                for ip, expiry in self.blocked_ips.items()
                if current_time < expiry
            }
            
            return {
                'total_tracked_ips': len(self.requests),
                'blocked_ips': len(active_blocks),
                'blocked_ip_list': active_blocks,
                'max_requests': self.max_requests,
                'time_window': self.time_window
            }
    
    def reset(self):
        """Reset all tracking data"""
        with self.lock:
            self.requests.clear()
            self.blocked_ips.clear()
