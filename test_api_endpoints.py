"""
CinePulse API Endpoint Integration Test
Verifies all backend endpoints respond correctly with valid JSON data.
"""
import urllib.request
import json
import time
import subprocess
import sys
import os

PORT = 5000
BASE_URL = f"http://127.0.0.1:{PORT}"

def test_all():
    print(f"Connecting to {BASE_URL} ...")
    endpoints = [
        ('/api/health', 'GET', None),
        ('/api/kpis', 'GET', None),
        ('/api/movies', 'GET', None),
        ('/api/metadata', 'GET', None),
        ('/api/users', 'GET', None),
        ('/api/recommendations?user_id=1', 'GET', None),
        ('/api/analytics', 'GET', None),
        ('/api/recursive', 'GET', None),
        ('/api/audit', 'GET', None),
        ('/api/nosql/documents', 'GET', None),
        ('/api/vector/search', 'POST', {"query": "space exploration black holes", "top_k": 3}),
        ('/api/auth/login', 'POST', {"username": "alex_admin", "password": "Password@123"})
    ]

    for path, method, payload in endpoints:
        url = BASE_URL + path
        try:
            req = urllib.request.Request(url, method=method)
            req.add_header('Content-Type', 'application/json')
            data = json.dumps(payload).encode('utf-8') if payload else None
            with urllib.request.urlopen(req, data=data, timeout=3) as res:
                body = res.read().decode('utf-8')
                parsed = json.loads(body)
                print(f"[PASS] {method} {path} -> HTTP {res.status} | Items/Keys: {len(parsed) if isinstance(parsed, (list, dict)) else 1}")
        except Exception as e:
            print(f"[FAIL] {method} {path} -> {e}")

if __name__ == '__main__':
    test_all()
