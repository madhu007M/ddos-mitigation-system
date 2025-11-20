#!/usr/bin/env python3
"""
Final Verification Script
Demonstrates that the DDoS Mitigation System is working correctly
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

print("="*70)
print("🛡️  DDoS MITIGATION SYSTEM - FINAL VERIFICATION")
print("="*70)
print()

# Test 1: Import all modules
print("Test 1: Importing modules...")
try:
    from src.core.config import ConfigManager
    from src.core.rate_limiter import RateLimiter
    from src.core.traffic_monitor import TrafficMonitor
    from src.core.ip_filter import IPFilter
    from src.core.mitigation_system import DDoSMitigationSystem
    print("✅ All core modules imported successfully")
except Exception as e:
    print(f"❌ Failed to import modules: {e}")
    sys.exit(1)

# Test 2: Initialize system
print("\nTest 2: Initializing system...")
try:
    ddos = DDoSMitigationSystem()
    print("✅ System initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize: {e}")
    sys.exit(1)

# Test 3: Process normal requests
print("\nTest 3: Processing normal requests...")
try:
    success_count = 0
    for i in range(5):
        is_allowed, reason, details = ddos.process_request("192.168.1.100", "/api/test", "GET")
        if is_allowed:
            success_count += 1
    print(f"✅ Processed {success_count}/5 normal requests successfully")
except Exception as e:
    print(f"❌ Failed to process requests: {e}")
    sys.exit(1)

# Test 4: Detect DDoS attack
print("\nTest 4: Detecting DDoS attack...")
try:
    blocked = False
    for i in range(150):
        is_allowed, reason, details = ddos.process_request("10.0.0.1", "/api/test", "GET")
        if not is_allowed:
            print(f"✅ DDoS detected and blocked at request {i+1}")
            blocked = True
            break
    if not blocked:
        print("❌ Failed to block DDoS attack")
        sys.exit(1)
except Exception as e:
    print(f"❌ Failed during DDoS test: {e}")
    sys.exit(1)

# Test 5: Whitelist functionality
print("\nTest 5: Testing whitelist...")
try:
    test_ip = "192.168.1.200"
    ddos.whitelist_ip(test_ip)
    
    # Try many requests (should all pass)
    all_passed = True
    for i in range(200):
        is_allowed, reason, details = ddos.process_request(test_ip, "/api/test", "GET")
        if not is_allowed:
            all_passed = False
            break
    
    if all_passed:
        print("✅ Whitelist functionality working (200 requests allowed)")
    else:
        print("❌ Whitelist failed")
        sys.exit(1)
except Exception as e:
    print(f"❌ Failed whitelist test: {e}")
    sys.exit(1)

# Test 6: Statistics
print("\nTest 6: Retrieving statistics...")
try:
    stats = ddos.get_stats()
    print(f"✅ Statistics retrieved:")
    print(f"   - Total Requests: {stats['traffic_monitor']['total_requests']}")
    print(f"   - Active IPs: {stats['traffic_monitor']['active_ips']}")
    print(f"   - Blocked IPs: {stats['rate_limiter']['blocked_ips']}")
    print(f"   - Suspicious IPs: {stats['traffic_monitor']['suspicious_ips_count']}")
except Exception as e:
    print(f"❌ Failed to get stats: {e}")
    sys.exit(1)

# Test 7: Alerts
print("\nTest 7: Checking alerts...")
try:
    alerts = ddos.get_recent_alerts(5)
    print(f"✅ Retrieved {len(alerts)} recent alerts")
    if alerts:
        latest = alerts[-1]
        print(f"   Latest alert: {latest['ip']} - Severity: {latest['severity']}")
except Exception as e:
    print(f"❌ Failed to get alerts: {e}")
    sys.exit(1)

# Test 8: Dashboard import
print("\nTest 8: Testing dashboard module...")
try:
    from src.dashboard.app import app
    with app.test_client() as client:
        response = client.get('/health')
        if response.status_code == 200:
            print("✅ Dashboard health check passed")
        else:
            print(f"❌ Dashboard health check failed: {response.status_code}")
            sys.exit(1)
except Exception as e:
    print(f"❌ Failed dashboard test: {e}")
    sys.exit(1)

# Final Summary
print("\n" + "="*70)
print("✅ ALL TESTS PASSED!")
print("="*70)
print("\n🎉 The DDoS Mitigation System is fully operational!")
print("\nNext steps:")
print("  1. Run: python example_usage.py")
print("  2. Start dashboard: python src/dashboard/app.py")
print("  3. Visit: http://localhost:5000")
print("  4. Simulate attacks: python simulate_attack.py")
print("\n" + "="*70)
