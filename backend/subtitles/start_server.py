#!/usr/bin/env python3
"""
Simple HTTP server to serve the interactive subtitles web app
"""

import http.server
import socketserver#!/usr/bin/env python3
"""
Runs burn_word_subs.py, then starts a local HTTP server to serve the interactive subtitles web app.
"""

import http.server
import socketserver
import webbrowser
import os
import subprocess
import sys

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def run_burn_word_subs():
    """Run the burn_word_subs.py script before starting the server."""
    script_path = r"C:\Users\divya\HTH\backend\subtitles\burn_word_subs.py"

    if not os.path.exists(script_path):
        print(f"❌ Could not find burn_word_subs.py at {script_path}")
        sys.exit(1)

    print("🎬 Running burn_word_subs.py ... this may take a while.")
    try:
        subprocess.run([sys.executable, script_path], check=True)
        print("✅ Subtitles burned successfully!")
    except subprocess.CalledProcessError as e:
        print("❌ burn_word_subs.py failed.")
        sys.exit(1)

def main():
    # Step 1: Run burn_word_subs first
    run_burn_word_subs()

    # Step 2: Serve the files
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🚀 Server started at http://localhost:{PORT}")
        print("📱 Opening web app in your browser...")
        webbrowser.open(f'http://localhost:{PORT}')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped. Goodbye!")

if __name__ == "__main__":
    main()

import webbrowser
import os

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    # Change to the directory containing the files
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🚀 Server started at http://localhost:{PORT}")
        print("📱 Opening web app in your browser...")
        print("🎬 Interactive subtitles are ready!")
        print("\nPress Ctrl+C to stop the server")
        
        # Open browser
        webbrowser.open(f'http://localhost:{PORT}')
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped. Goodbye!")

if __name__ == "__main__":
    main() 