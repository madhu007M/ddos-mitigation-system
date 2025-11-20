#!/usr/bin/env python3
"""
DDoS Attack Simulator
Used for testing the mitigation system
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.core.mitigation_system import DDoSMitigationSystem
import time
import random
from datetime import datetime


def simulate_normal_traffic(ddos, num_ips=10, requests_per_ip=5):
    """Simulate normal traffic"""
    print(f"\n{'='*60}")
    print("Simulating Normal Traffic")
    print(f"{'='*60}")
    
    for i in range(num_ips):
        ip = f"192.168.1.{i+1}"
        print(f"\nIP: {ip}")
        
        for j in range(requests_per_ip):
            is_allowed, reason, details = ddos.process_request(ip, "/api/data", "GET")
            status = "✓" if is_allowed else "✗"
            print(f"  Request {j+1}: {status} {reason}")
            time.sleep(0.1)


def simulate_ddos_attack(ddos, attack_ip="10.0.0.100", num_requests=200):
    """Simulate a DDoS attack"""
    print(f"\n{'='*60}")
    print("Simulating DDoS Attack")
    print(f"{'='*60}")
    print(f"Attacker IP: {attack_ip}")
    print(f"Attack intensity: {num_requests} rapid requests\n")
    
    allowed_count = 0
    blocked_count = 0
    
    for i in range(num_requests):
        is_allowed, reason, details = ddos.process_request(attack_ip, "/api/data", "GET")
        
        if is_allowed:
            allowed_count += 1
        else:
            blocked_count += 1
            if blocked_count == 1:
                print(f"✗ Attack detected and blocked at request {i+1}!")
                print(f"  Reason: {reason}")
                break
        
        if i < 10 or i % 10 == 0:
            status = "✓" if is_allowed else "✗"
            print(f"  Request {i+1}: {status}")
        
        time.sleep(0.01)
    
    print(f"\nResults:")
    print(f"  Allowed: {allowed_count}")
    print(f"  Blocked: {blocked_count}")
    print(f"  Protection rate: {(blocked_count/(allowed_count+blocked_count)*100):.1f}%")


def simulate_distributed_attack(ddos, num_attackers=10, requests_per_attacker=50):
    """Simulate a distributed DDoS attack"""
    print(f"\n{'='*60}")
    print("Simulating Distributed DDoS Attack")
    print(f"{'='*60}")
    print(f"Number of attackers: {num_attackers}")
    print(f"Requests per attacker: {requests_per_attacker}\n")
    
    for i in range(num_attackers):
        attacker_ip = f"10.0.{i}.100"
        print(f"\nAttacker {i+1}: {attacker_ip}")
        
        allowed = 0
        blocked = 0
        
        for j in range(requests_per_attacker):
            is_allowed, reason, details = ddos.process_request(attacker_ip, "/api/data", "GET")
            
            if is_allowed:
                allowed += 1
            else:
                blocked += 1
                if blocked == 1:
                    print(f"  ✗ Blocked after {j+1} requests - {reason}")
                    break
            
            time.sleep(0.01)
        
        if blocked == 0:
            print(f"  ✓ All {allowed} requests allowed (below threshold)")


def display_stats(ddos):
    """Display system statistics"""
    print(f"\n{'='*60}")
    print("System Statistics")
    print(f"{'='*60}")
    
    stats = ddos.get_stats()
    
    print("\n📊 Traffic Monitor:")
    print(f"  Total Requests: {stats['traffic_monitor']['total_requests']}")
    print(f"  Active IPs: {stats['traffic_monitor']['active_ips']}")
    print(f"  Suspicious IPs: {stats['traffic_monitor']['suspicious_ips_count']}")
    print(f"  Total Alerts: {stats['traffic_monitor']['total_alerts']}")
    
    print("\n🚫 Rate Limiter:")
    print(f"  Blocked IPs: {stats['rate_limiter']['blocked_ips']}")
    print(f"  Max Requests/Window: {stats['rate_limiter']['max_requests']}")
    print(f"  Time Window: {stats['rate_limiter']['time_window']}s")
    
    print("\n🛡️ IP Filter:")
    print(f"  Whitelisted: {stats['ip_filter']['whitelist_count']}")
    print(f"  Blacklisted: {stats['ip_filter']['blacklist_count']}")
    print(f"  Temp Blocked: {stats['ip_filter']['temp_blocked_count']}")
    
    if stats['traffic_monitor']['recent_alerts']:
        print("\n⚠️  Recent Alerts:")
        for alert in stats['traffic_monitor']['recent_alerts'][-5:]:
            timestamp = datetime.fromtimestamp(alert['timestamp']).strftime('%H:%M:%S')
            print(f"  [{timestamp}] {alert['ip']}: {alert['request_rate']} req/s (Severity: {alert['severity']})")


def main():
    """Main simulator function"""
    print("=" * 60)
    print("DDoS Attack Simulator")
    print("=" * 60)
    
    # Initialize system
    print("\nInitializing DDoS Mitigation System...")
    ddos = DDoSMitigationSystem()
    print("✓ System initialized\n")
    
    # Menu
    while True:
        print("\n" + "=" * 60)
        print("Select simulation:")
        print("1. Normal Traffic")
        print("2. Single Source DDoS Attack")
        print("3. Distributed DDoS Attack")
        print("4. Display Statistics")
        print("5. Reset System")
        print("6. Run All Simulations")
        print("0. Exit")
        print("=" * 60)
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            simulate_normal_traffic(ddos)
        elif choice == "2":
            simulate_ddos_attack(ddos)
        elif choice == "3":
            simulate_distributed_attack(ddos)
        elif choice == "4":
            display_stats(ddos)
        elif choice == "5":
            ddos.reset_all()
            print("\n✓ System reset complete")
        elif choice == "6":
            simulate_normal_traffic(ddos, num_ips=5, requests_per_ip=3)
            time.sleep(1)
            simulate_ddos_attack(ddos, num_requests=150)
            time.sleep(1)
            simulate_distributed_attack(ddos, num_attackers=5, requests_per_attacker=30)
            display_stats(ddos)
        elif choice == "0":
            print("\nExiting simulator...")
            break
        else:
            print("\n✗ Invalid choice. Please try again.")
    
    print("\nSimulation complete!")


if __name__ == "__main__":
    main()
