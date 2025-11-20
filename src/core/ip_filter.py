"""
IP Filter Module
Manages IP whitelisting and blacklisting
"""
from typing import Set, List, Dict
import threading
import time


class IPFilter:
    """Manages IP filtering and blocking"""
    
    def __init__(self, whitelist: List[str] = None, blacklist: List[str] = None):
        """
        Initialize IP filter
        
        Args:
            whitelist: List of IPs to always allow
            blacklist: List of IPs to always block
        """
        self.whitelist: Set[str] = set(whitelist or [])
        self.blacklist: Set[str] = set(blacklist or [])
        
        # Temporary blocks (auto-expire)
        self.temp_blocks: Dict[str, float] = {}
        
        # Thread lock
        self.lock = threading.Lock()
    
    def is_allowed(self, ip: str) -> tuple[bool, str]:
        """
        Check if IP is allowed
        
        Args:
            ip: IP address to check
            
        Returns:
            Tuple of (is_allowed, reason)
        """
        with self.lock:
            # Whitelist always allowed
            if ip in self.whitelist:
                return True, "Whitelisted"
            
            # Check permanent blacklist
            if ip in self.blacklist:
                return False, "IP is blacklisted"
            
            # Check temporary blocks
            if ip in self.temp_blocks:
                current_time = time.time()
                if current_time < self.temp_blocks[ip]:
                    remaining = int(self.temp_blocks[ip] - current_time)
                    return False, f"IP temporarily blocked ({remaining}s remaining)"
                else:
                    # Block expired
                    del self.temp_blocks[ip]
            
            return True, "Allowed"
    
    def add_to_whitelist(self, ip: str):
        """Add IP to whitelist"""
        with self.lock:
            self.whitelist.add(ip)
            # Remove from blacklist if present
            self.blacklist.discard(ip)
            # Remove from temp blocks
            self.temp_blocks.pop(ip, None)
    
    def remove_from_whitelist(self, ip: str):
        """Remove IP from whitelist"""
        with self.lock:
            self.whitelist.discard(ip)
    
    def add_to_blacklist(self, ip: str):
        """Add IP to permanent blacklist"""
        with self.lock:
            self.blacklist.add(ip)
            # Remove from whitelist if present
            self.whitelist.discard(ip)
            # Remove from temp blocks
            self.temp_blocks.pop(ip, None)
    
    def remove_from_blacklist(self, ip: str):
        """Remove IP from blacklist"""
        with self.lock:
            self.blacklist.discard(ip)
    
    def block_temporarily(self, ip: str, duration: int):
        """
        Block IP temporarily
        
        Args:
            ip: IP address
            duration: Block duration in seconds
        """
        with self.lock:
            # Don't block whitelisted IPs
            if ip not in self.whitelist and ip not in self.blacklist:
                self.temp_blocks[ip] = time.time() + duration
    
    def unblock(self, ip: str):
        """Remove IP from temporary blocks"""
        with self.lock:
            self.temp_blocks.pop(ip, None)
    
    def is_whitelisted(self, ip: str) -> bool:
        """Check if IP is whitelisted"""
        with self.lock:
            return ip in self.whitelist
    
    def is_blacklisted(self, ip: str) -> bool:
        """Check if IP is blacklisted"""
        with self.lock:
            return ip in self.blacklist
    
    def is_temp_blocked(self, ip: str) -> bool:
        """Check if IP is temporarily blocked"""
        with self.lock:
            if ip in self.temp_blocks:
                if time.time() < self.temp_blocks[ip]:
                    return True
                else:
                    del self.temp_blocks[ip]
            return False
    
    def get_stats(self) -> Dict:
        """Get IP filter statistics"""
        with self.lock:
            current_time = time.time()
            
            # Clean expired temp blocks
            expired = [ip for ip, expiry in self.temp_blocks.items() if current_time >= expiry]
            for ip in expired:
                del self.temp_blocks[ip]
            
            temp_block_details = {
                ip: int(expiry - current_time)
                for ip, expiry in self.temp_blocks.items()
            }
            
            return {
                'whitelist_count': len(self.whitelist),
                'blacklist_count': len(self.blacklist),
                'temp_blocked_count': len(self.temp_blocks),
                'whitelist': list(self.whitelist),
                'blacklist': list(self.blacklist),
                'temp_blocks': temp_block_details
            }
    
    def reset(self):
        """Reset temporary blocks (keeps whitelist and blacklist)"""
        with self.lock:
            self.temp_blocks.clear()
