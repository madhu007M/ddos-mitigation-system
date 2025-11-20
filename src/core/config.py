"""
Configuration Manager for DDoS Mitigation System
"""
import yaml
import os
from typing import Dict, Any, List


class ConfigManager:
    """Manages configuration loading and access"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file)
                return config
        except FileNotFoundError:
            print(f"Warning: Config file {self.config_path} not found. Using defaults.")
            return self.get_default_config()
        except yaml.YAMLError as e:
            print(f"Error parsing config file: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            'rate_limiting': {
                'enabled': True,
                'max_requests_per_window': 100,
                'time_window': 60,
                'block_duration': 300
            },
            'monitoring': {
                'enabled': True,
                'suspicious_threshold': 10,
                'detection_window': 10,
                'alert_threshold': 3
            },
            'ip_blocking': {
                'enabled': True,
                'whitelist': ['127.0.0.1', '::1'],
                'blacklist': [],
                'auto_block': True
            },
            'logging': {
                'level': 'INFO',
                'file': 'logs/ddos_mitigation.log'
            },
            'dashboard': {
                'enabled': True,
                'port': 5000,
                'host': '0.0.0.0',
                'debug': False
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (supports nested keys with dots)"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value
    
    def get_rate_limit_config(self) -> Dict[str, Any]:
        """Get rate limiting configuration"""
        return self.config.get('rate_limiting', {})
    
    def get_monitoring_config(self) -> Dict[str, Any]:
        """Get monitoring configuration"""
        return self.config.get('monitoring', {})
    
    def get_ip_blocking_config(self) -> Dict[str, Any]:
        """Get IP blocking configuration"""
        return self.config.get('ip_blocking', {})
    
    def is_whitelisted(self, ip: str) -> bool:
        """Check if IP is whitelisted"""
        whitelist = self.get('ip_blocking.whitelist', [])
        return ip in whitelist
    
    def is_blacklisted(self, ip: str) -> bool:
        """Check if IP is blacklisted"""
        blacklist = self.get('ip_blocking.blacklist', [])
        return ip in blacklist
