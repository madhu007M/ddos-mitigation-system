# DDoS Mitigation System - Usage Guide

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/madhu007M/ddos-mitigation-system.git
cd ddos-mitigation-system

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Example

```bash
python example_usage.py
```

This will demonstrate:
- Normal request processing
- DDoS attack detection and blocking
- System statistics
- IP management (whitelist/blacklist)

### 3. Start the Dashboard

```bash
python src/dashboard/app.py
```

Then open your browser and navigate to `http://localhost:5000`

## Common Use Cases

### Use Case 1: Protect a Web Application

```python
from flask import Flask, request, jsonify
from src.core.mitigation_system import DDoSMitigationSystem

app = Flask(__name__)
ddos = DDoSMitigationSystem()

@app.before_request
def protect_endpoint():
    """Check every incoming request"""
    client_ip = request.remote_addr
    is_allowed, reason, details = ddos.process_request(
        client_ip,
        request.path,
        request.method
    )
    
    if not is_allowed:
        return jsonify({
            'error': 'Too Many Requests',
            'message': reason
        }), 429

@app.route('/api/data')
def get_data():
    return jsonify({'data': 'This endpoint is protected'})

if __name__ == '__main__':
    app.run()
```

### Use Case 2: Monitor and Alert

```python
from src.core.mitigation_system import DDoSMitigationSystem
import time

ddos = DDoSMitigationSystem()

# Monitor continuously
while True:
    # Get recent alerts
    alerts = ddos.get_recent_alerts(limit=5)
    
    for alert in alerts:
        if alert['severity'] in ['HIGH', 'CRITICAL']:
            print(f"🚨 ALERT: {alert['ip']} - {alert['request_rate']} req/s")
            # Send notification (email, Slack, etc.)
            send_notification(alert)
    
    # Get stats
    stats = ddos.get_stats()
    if stats['rate_limiter']['blocked_ips'] > 10:
        print("⚠️  Warning: Multiple IPs blocked")
    
    time.sleep(60)  # Check every minute
```

### Use Case 3: Custom Rate Limits per Endpoint

```python
from src.core.rate_limiter import RateLimiter

# Create different rate limiters for different endpoints
api_limiter = RateLimiter(max_requests=100, time_window=60)
login_limiter = RateLimiter(max_requests=5, time_window=60)
public_limiter = RateLimiter(max_requests=1000, time_window=60)

def check_endpoint(ip, endpoint):
    if endpoint.startswith('/api/'):
        return api_limiter.is_allowed(ip)
    elif endpoint == '/login':
        return login_limiter.is_allowed(ip)
    else:
        return public_limiter.is_allowed(ip)
```

### Use Case 4: Whitelist Trusted IPs

```python
from src.core.mitigation_system import DDoSMitigationSystem

ddos = DDoSMitigationSystem()

# Whitelist your office IP
ddos.whitelist_ip("203.0.113.50")

# Whitelist monitoring services
monitoring_ips = [
    "198.51.100.10",
    "198.51.100.11",
    "198.51.100.12"
]

for ip in monitoring_ips:
    ddos.whitelist_ip(ip)
```

### Use Case 5: Temporarily Block Suspicious IP

```python
from src.core.mitigation_system import DDoSMitigationSystem

ddos = DDoSMitigationSystem()

# Block for 1 hour (3600 seconds)
ddos.block_ip("10.0.0.50", duration=3600)

# Block permanently
ddos.block_ip("10.0.0.51", permanent=True)

# Unblock later
ddos.unblock_ip("10.0.0.50")
```

## Dashboard Features

### Real-time Monitoring
- **System Overview**: Track total requests, active IPs, and blocked IPs
- **Rate Limiter Stats**: View current limits and blocked count
- **Recent Alerts**: See security incidents as they happen
- **Auto-refresh**: Updates every 2 seconds

### IP Management
1. **Block IP**: Enter IP and optional duration
2. **Unblock IP**: Remove IP from block list
3. **Whitelist IP**: Add trusted IPs

### Testing
Use the test interface to:
- Simulate requests from specific IPs
- See if an IP would be allowed or blocked
- Test your configuration

## Configuration Tuning

Edit `config.yaml` to customize behavior:

### For High Traffic Sites
```yaml
rate_limiting:
  max_requests_per_window: 500  # Allow more requests
  time_window: 60
  block_duration: 600           # Block longer

monitoring:
  suspicious_threshold: 50      # Higher threshold
  detection_window: 10
  alert_threshold: 5
```

### For Strict Protection
```yaml
rate_limiting:
  max_requests_per_window: 50   # Fewer requests allowed
  time_window: 60
  block_duration: 1800          # 30 minute blocks

monitoring:
  suspicious_threshold: 5       # Lower threshold
  detection_window: 10
  alert_threshold: 2            # Block faster
```

### For Development/Testing
```yaml
rate_limiting:
  max_requests_per_window: 1000
  time_window: 60
  block_duration: 60            # Short blocks

monitoring:
  suspicious_threshold: 100     # Very lenient
```

## Command Line Usage

### Run with Custom Config
```bash
# Use custom config file
CONFIG_FILE=custom_config.yaml python src/dashboard/app.py
```

### Run on Different Port
```bash
python src/dashboard/app.py --port 8080
```

### Debug Mode
```bash
python src/dashboard/app.py --debug
```

## Testing

### Unit Tests
```bash
# Run all tests
python -m unittest discover tests -v

# Run specific test
python -m unittest tests.test_rate_limiter
```

### Attack Simulation
```bash
python simulate_attack.py
```

Choose from:
1. Normal Traffic - Simulates legitimate users
2. Single Source DDoS - Tests blocking of one attacker
3. Distributed DDoS - Tests blocking of multiple attackers
4. Display Statistics - View current system state
5. Reset System - Clear all data

## Docker Deployment

### Build and Run
```bash
# Build image
docker build -t ddos-mitigation .

# Run container
docker run -d -p 5000:5000 ddos-mitigation
```

### Using Docker Compose
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f ddos-mitigation

# Stop services
docker-compose down
```

## API Integration

### Check Request
```python
is_allowed, reason, details = ddos.process_request(
    ip="192.168.1.1",
    endpoint="/api/data",
    method="GET"
)

if not is_allowed:
    # Block the request
    return error_response(reason, 429)
```

### Get Statistics
```python
stats = ddos.get_stats()

print(f"Total Requests: {stats['traffic_monitor']['total_requests']}")
print(f"Blocked IPs: {stats['rate_limiter']['blocked_ips']}")
print(f"Suspicious IPs: {stats['traffic_monitor']['suspicious_ips_count']}")
```

### Get Alerts
```python
alerts = ddos.get_recent_alerts(limit=10)

for alert in alerts:
    print(f"[{alert['severity']}] {alert['ip']}: {alert['request_rate']} req/s")
```

## Troubleshooting

### Issue: Too Many False Positives
**Solution**: Increase rate limits in config.yaml
```yaml
rate_limiting:
  max_requests_per_window: 200  # Increase from 100
```

### Issue: Attacks Not Being Blocked
**Solution**: Lower thresholds
```yaml
rate_limiting:
  max_requests_per_window: 50   # Decrease
monitoring:
  suspicious_threshold: 5        # Decrease
```

### Issue: Dashboard Not Accessible
**Check**:
1. Is the service running? `ps aux | grep python`
2. Is port 5000 available? `netstat -an | grep 5000`
3. Check logs: `tail -f logs/ddos_mitigation.log`

### Issue: Legitimate Users Being Blocked
**Solution**: Add to whitelist
```python
ddos.whitelist_ip("their.ip.address")
```

## Best Practices

1. **Whitelist Important IPs**
   - Your own servers
   - Monitoring services
   - Known partners

2. **Monitor Regularly**
   - Check dashboard daily
   - Review alerts
   - Adjust thresholds as needed

3. **Log Analysis**
   - Review `logs/ddos_mitigation.log`
   - Look for patterns
   - Identify false positives

4. **Gradual Tuning**
   - Start with lenient settings
   - Monitor for a week
   - Gradually tighten as needed

5. **Backup Strategy**
   - This is one layer of defense
   - Use with firewall, CDN, etc.
   - Have incident response plan

## Support

- **Documentation**: See README.md
- **Issues**: Open an issue on GitHub
- **Configuration Help**: Check config.yaml comments

## Examples Directory

Check out the examples:
- `example_usage.py` - Basic integration
- `simulate_attack.py` - Test scenarios
- `src/dashboard/app.py` - Full web application

---

**Ready to protect your application!** 🛡️
