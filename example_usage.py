#!/usr/bin/env python3
"""
Example usage script for DDoS Mitigation System
Demonstrates how to integrate the system into your application
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.core.mitigation_system import DDoSMitigationSystem
import time


def main():
    """Example usage of DDoS mitigation system"""
    
    print("=" * 60)
    print("DDoS Mitigation System - Example Usage")
    print("=" * 60)
    print()
    
    # Initialize the system
    print("1. Initializing DDoS Mitigation System...")
    ddos = DDoSMitigationSystem()
    print("   ✓ System initialized\n")
    
    # Example 1: Process a normal request
    print("2. Processing normal request from 192.168.1.100...")
    is_allowed, reason, details = ddos.process_request("192.168.1.100", "/api/data", "GET")
    print(f"   Result: {'✓ ALLOWED' if is_allowed else '✗ BLOCKED'}")
    print(f"   Reason: {reason}\n")
    
    # Example 2: Simulate rapid requests (potential DDoS)
    print("3. Simulating rapid requests from 192.168.1.200 (potential DDoS)...")
    test_ip = "192.168.1.200"
    for i in range(15):
        is_allowed, reason, details = ddos.process_request(test_ip, "/api/data", "GET")
        if not is_allowed:
            print(f"   Request {i+1}: ✗ BLOCKED - {reason}")
            break
        print(f"   Request {i+1}: ✓ Allowed")
        time.sleep(0.05)
    print()
    
    # Example 3: Check system statistics
    print("4. System Statistics:")
    stats = ddos.get_stats()
    print(f"   Active IPs: {stats['traffic_monitor']['active_ips']}")
    print(f"   Total Requests: {stats['traffic_monitor']['total_requests']}")
    print(f"   Blocked IPs: {stats['rate_limiter']['blocked_ips']}")
    print(f"   Suspicious IPs: {stats['traffic_monitor']['suspicious_ips_count']}\n")
    
    # Example 4: Get recent alerts
    print("5. Recent Alerts:")
    alerts = ddos.get_recent_alerts(5)
    if alerts:
        for alert in alerts:
            print(f"   - {alert['ip']}: {alert['request_rate']} req/s (Severity: {alert['severity']})")
    else:
        print("   No alerts")
    print()
    
    # Example 5: Manual IP management
    print("6. Manual IP Management:")
    print("   Whitelisting 192.168.1.100...")
    ddos.whitelist_ip("192.168.1.100")
    print("   ✓ IP whitelisted")
    
    print("   Blocking 10.0.0.50...")
    ddos.block_ip("10.0.0.50", duration=60)
    print("   ✓ IP blocked for 60 seconds\n")
    
    # Example 6: Test whitelisted IP (should always pass)
    print("7. Testing whitelisted IP (192.168.1.100)...")
    for i in range(5):
        is_allowed, reason, details = ddos.process_request("192.168.1.100", "/api/data", "GET")
        print(f"   Request {i+1}: {'✓' if is_allowed else '✗'} {reason}")
    print()
    
    # Example 7: Integration example
    print("8. Integration Example:")
    print("""
   In your web application:
   
   from src.core.mitigation_system import DDoSMitigationSystem
   ddos = DDoSMitigationSystem()
   
   @app.before_request
   def check_ddos():
       client_ip = request.remote_addr
       is_allowed, reason, details = ddos.process_request(
           client_ip,
           request.path,
           request.method
       )
       
       if not is_allowed:
           return jsonify({'error': reason}), 429
    """)
    
    print("\n" + "=" * 60)
    print("Example completed! Check logs/ddos_mitigation.log for details")
    print("=" * 60)


if __name__ == "__main__":
    main()
