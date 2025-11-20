"""
Web Dashboard for DDoS Mitigation System
Real-time monitoring and control interface
"""
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.core.mitigation_system import DDoSMitigationSystem

app = Flask(__name__)
CORS(app)

# Initialize DDoS mitigation system
ddos_system = DDoSMitigationSystem()


@app.route('/')
def index():
    """Dashboard home page"""
    return render_template('dashboard.html')


@app.route('/api/stats')
def get_stats():
    """Get system statistics"""
    try:
        stats = ddos_system.get_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/alerts')
def get_alerts():
    """Get recent alerts"""
    try:
        limit = request.args.get('limit', 20, type=int)
        alerts = ddos_system.get_recent_alerts(limit)
        return jsonify({
            'success': True,
            'data': alerts
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/block', methods=['POST'])
def block_ip():
    """Block an IP address"""
    try:
        data = request.json
        ip = data.get('ip')
        duration = data.get('duration')
        permanent = data.get('permanent', False)
        
        if not ip:
            return jsonify({
                'success': False,
                'error': 'IP address is required'
            }), 400
        
        ddos_system.block_ip(ip, duration, permanent)
        return jsonify({
            'success': True,
            'message': f'IP {ip} blocked successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/unblock', methods=['POST'])
def unblock_ip():
    """Unblock an IP address"""
    try:
        data = request.json
        ip = data.get('ip')
        
        if not ip:
            return jsonify({
                'success': False,
                'error': 'IP address is required'
            }), 400
        
        ddos_system.unblock_ip(ip)
        return jsonify({
            'success': True,
            'message': f'IP {ip} unblocked successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/whitelist', methods=['POST'])
def whitelist_ip():
    """Add IP to whitelist"""
    try:
        data = request.json
        ip = data.get('ip')
        
        if not ip:
            return jsonify({
                'success': False,
                'error': 'IP address is required'
            }), 400
        
        ddos_system.whitelist_ip(ip)
        return jsonify({
            'success': True,
            'message': f'IP {ip} whitelisted successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/test', methods=['POST'])
def test_request():
    """Test endpoint to simulate requests"""
    try:
        data = request.json
        ip = data.get('ip', request.remote_addr)
        endpoint = data.get('endpoint', '/test')
        method = data.get('method', 'GET')
        
        is_allowed, reason, details = ddos_system.process_request(ip, endpoint, method)
        
        return jsonify({
            'success': True,
            'allowed': is_allowed,
            'reason': reason,
            'details': details
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'DDoS Mitigation System'
    })


def run_dashboard(host='0.0.0.0', port=5000, debug=False):
    """Run the dashboard server"""
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='DDoS Mitigation Dashboard')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    print(f"Starting DDoS Mitigation Dashboard on {args.host}:{args.port}")
    run_dashboard(args.host, args.port, args.debug)
