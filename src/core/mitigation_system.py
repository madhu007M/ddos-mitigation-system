"""
DDoS Mitigation System - Main Module
Integrates all components for comprehensive DDoS protection
"""
import time
from typing import Optional, Dict
from .config import ConfigManager
from .rate_limiter import RateLimiter
from .traffic_monitor import TrafficMonitor
from .ip_filter import IPFilter
import logging
import os


class DDoSMitigationSystem:
    """Main DDoS mitigation system coordinator"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize DDoS mitigation system
        
        Args:
            config_path: Path to configuration file
        """
        # Load configuration
        self.config = ConfigManager(config_path)
        
        # Initialize logging
        self._setup_logging()
        
        # Initialize components
        self._initialize_components()
        
        self.logger.info("DDoS Mitigation System initialized")
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_file = self.config.get('logging.file', 'logs/ddos_mitigation.log')
        log_level = self.config.get('logging.level', 'INFO')
        
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('DDoSMitigation')
    
    def _initialize_components(self):
        """Initialize all mitigation components"""
        # Rate limiter
        rate_config = self.config.get_rate_limit_config()
        self.rate_limiter = RateLimiter(
            max_requests=rate_config.get('max_requests_per_window', 100),
            time_window=rate_config.get('time_window', 60),
            block_duration=rate_config.get('block_duration', 300)
        )
        
        # Traffic monitor
        monitor_config = self.config.get_monitoring_config()
        self.traffic_monitor = TrafficMonitor(
            suspicious_threshold=monitor_config.get('suspicious_threshold', 10),
            detection_window=monitor_config.get('detection_window', 10),
            alert_threshold=monitor_config.get('alert_threshold', 3)
        )
        
        # IP filter
        ip_config = self.config.get_ip_blocking_config()
        self.ip_filter = IPFilter(
            whitelist=ip_config.get('whitelist', []),
            blacklist=ip_config.get('blacklist', [])
        )
    
    def process_request(self, ip: str, endpoint: str = "/", method: str = "GET") -> tuple[bool, str, Dict]:
        """
        Process incoming request and determine if it should be allowed
        
        Args:
            ip: Client IP address
            endpoint: Request endpoint
            method: HTTP method
            
        Returns:
            Tuple of (is_allowed, reason, details)
        """
        details = {
            'ip': ip,
            'endpoint': endpoint,
            'method': method,
            'timestamp': time.time()
        }
        
        # Check whitelist/blacklist first
        is_allowed, filter_reason = self.ip_filter.is_allowed(ip)
        if not is_allowed:
            self.logger.warning(f"Request blocked by IP filter: {ip} - {filter_reason}")
            details['blocked_by'] = 'ip_filter'
            details['reason'] = filter_reason
            return False, filter_reason, details
        
        # Skip rate limiting for whitelisted IPs
        if self.ip_filter.is_whitelisted(ip):
            self.traffic_monitor.record_request(ip, endpoint, method)
            details['allowed_by'] = 'whitelist'
            return True, "Whitelisted IP", details
        
        # Check rate limiter
        is_allowed, rate_reason = self.rate_limiter.is_allowed(ip)
        if not is_allowed:
            self.logger.warning(f"Request blocked by rate limiter: {ip} - {rate_reason}")
            details['blocked_by'] = 'rate_limiter'
            details['reason'] = rate_reason
            
            # Auto-block if configured
            if self.config.get('ip_blocking.auto_block', True):
                self.ip_filter.block_temporarily(ip, self.rate_limiter.block_duration)
            
            return False, rate_reason, details
        
        # Record request for monitoring
        self.traffic_monitor.record_request(ip, endpoint, method)
        
        # Check for suspicious activity
        is_suspicious, suspicious_details = self.traffic_monitor.is_suspicious(ip)
        if is_suspicious:
            self.logger.warning(f"Suspicious activity detected: {ip} - {suspicious_details}")
            details['suspicious'] = True
            details['suspicious_details'] = suspicious_details
            
            # Auto-block if configured and severity is high
            if (self.config.get('ip_blocking.auto_block', True) and 
                suspicious_details.get('severity') in ['HIGH', 'CRITICAL']):
                self.ip_filter.block_temporarily(ip, 600)  # Block for 10 minutes
                self.logger.warning(f"Auto-blocking suspicious IP: {ip}")
                return False, f"Suspicious activity: {suspicious_details}", details
        
        details['allowed_by'] = 'all_checks_passed'
        return True, "Request allowed", details
    
    def get_stats(self) -> Dict:
        """Get comprehensive system statistics"""
        return {
            'rate_limiter': self.rate_limiter.get_stats(),
            'traffic_monitor': self.traffic_monitor.get_stats(),
            'ip_filter': self.ip_filter.get_stats(),
            'system_uptime': time.time()
        }
    
    def block_ip(self, ip: str, duration: Optional[int] = None, permanent: bool = False):
        """
        Manually block an IP
        
        Args:
            ip: IP address to block
            duration: Block duration in seconds (for temporary block)
            permanent: If True, add to permanent blacklist
        """
        if permanent:
            self.ip_filter.add_to_blacklist(ip)
            self.logger.info(f"IP permanently blacklisted: {ip}")
        else:
            block_time = duration or self.rate_limiter.block_duration
            self.ip_filter.block_temporarily(ip, block_time)
            self.logger.info(f"IP temporarily blocked: {ip} for {block_time} seconds")
    
    def unblock_ip(self, ip: str):
        """Unblock an IP"""
        self.ip_filter.unblock(ip)
        self.rate_limiter.unblock_ip(ip)
        self.traffic_monitor.reset_violations(ip)
        self.logger.info(f"IP unblocked: {ip}")
    
    def whitelist_ip(self, ip: str):
        """Add IP to whitelist"""
        self.ip_filter.add_to_whitelist(ip)
        self.logger.info(f"IP whitelisted: {ip}")
    
    def get_recent_alerts(self, limit: int = 10):
        """Get recent security alerts"""
        return self.traffic_monitor.get_recent_alerts(limit)
    
    def reset_all(self):
        """Reset all tracking data (for testing/maintenance)"""
        self.rate_limiter.reset()
        self.traffic_monitor.reset()
        self.ip_filter.reset()
        self.logger.info("System reset completed")
