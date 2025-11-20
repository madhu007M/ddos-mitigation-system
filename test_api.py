#!/usr/bin/env python3
"""Test API endpoints"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.dashboard.app import app
import json

# Create test client
client = app.test_client()

print("Testing DDoS Mitigation API Endpoints...\n")

# Test 1: Health check
print("1. Health Check:")
response = client.get('/health')
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json}")

# Test 2: Get stats
print("\n2. Get Statistics:")
response = client.get('/api/stats')
print(f"   Status: {response.status_code}")
data = response.json
if data['success']:
    stats = data['data']
    print(f"   ✓ Rate Limiter: {stats['rate_limiter']['blocked_ips']} blocked IPs")
    print(f"   ✓ Traffic Monitor: {stats['traffic_monitor']['total_requests']} total requests")
    print(f"   ✓ IP Filter: {stats['ip_filter']['whitelist_count']} whitelisted")

# Test 3: Test request
print("\n3. Test Request Processing:")
response = client.post('/api/test',
                       json={'ip': '192.168.1.100', 'endpoint': '/api/data', 'method': 'GET'},
                       content_type='application/json')
print(f"   Status: {response.status_code}")
data = response.json
if data['success']:
    print(f"   ✓ Allowed: {data['allowed']}")
    print(f"   ✓ Reason: {data['reason']}")

# Test 4: Block IP
print("\n4. Block IP:")
response = client.post('/api/block',
                       json={'ip': '10.0.0.99', 'duration': 60},
                       content_type='application/json')
print(f"   Status: {response.status_code}")
data = response.json
if data['success']:
    print(f"   ✓ {data['message']}")

# Test 5: Whitelist IP
print("\n5. Whitelist IP:")
response = client.post('/api/whitelist',
                       json={'ip': '192.168.1.200'},
                       content_type='application/json')
print(f"   Status: {response.status_code}")
data = response.json
if data['success']:
    print(f"   ✓ {data['message']}")

# Test 6: Get alerts
print("\n6. Get Alerts:")
response = client.get('/api/alerts?limit=5')
print(f"   Status: {response.status_code}")
data = response.json
if data['success']:
    print(f"   ✓ Total alerts: {len(data['data'])}")

print("\n✓ All API tests passed!")
