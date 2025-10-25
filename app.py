"""
Fyyur application entry point.
"""
import socket
from app import create_app

# Create app instance
app = create_app()

def find_free_port(start_port=5000, max_port=5010):
    """Find a free port starting from start_port."""
    for port in range(start_port, max_port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    return start_port  # Fallback to original port

if __name__ == '__main__':
    port = find_free_port()
    print(f"🚀 Starting Fyyur on http://127.0.0.1:{port}")
    app.run(host='127.0.0.1', port=port, debug=True)