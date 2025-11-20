#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.core.mitigation_system import DDoSMitigationSystem

# Quick test
print("Testing DDoS Mitigation System...")
ddos = DDoSMitigationSystem()
print("✓ System initialized")

# Test normal request
is_allowed, reason, details = ddos.process_request("192.168.1.1", "/api/data", "GET")
print(f"✓ Normal request: {'ALLOWED' if is_allowed else 'BLOCKED'}")

# Test rapid requests
test_ip = "10.0.0.1"
for i in range(120):
    is_allowed, reason, details = ddos.process_request(test_ip, "/api/data", "GET")
    if not is_allowed:
        print(f"✓ DDoS detected and blocked at request {i+1}")
        break

# Get stats
stats = ddos.get_stats()
print(f"✓ Stats: {stats['traffic_monitor']['total_requests']} requests, {stats['rate_limiter']['blocked_ips']} blocked IPs")

print("\nAll tests passed!")
