import http.server
import socketserver
import threading
import time
import sys
import os
from playwright.sync_api import sync_playwright

PORT = 13131
DIRECTORY = "blog/public"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()

def verify():
    # Start server in background
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(2) # Wait for server to start

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        print(f"Navigating to http://localhost:{PORT}/scenarios/")
        
        # Capture console logs
        page.on("console", lambda msg: print(f"BROWSER CONSOLE [{msg.type}]: {msg.text}"))
        page.on("pageerror", lambda exc: print(f"BROWSER UNCAUGHT ERROR: {exc}"))

        try:
            response = page.goto(f"http://localhost:{PORT}/scenarios/")
            print(f"Page load status: {response.status}")
            
            # Wait a bit for JS to run
            time.sleep(3)
            
            # Check for Graph Container
            container = page.query_selector("#graph-container")
            if container:
                print("SUCCESS: #graph-container found.")
            else:
                print("FAILURE: #graph-container NOT found.")

            # Check for Canvas (GraphEngine output)
            canvas = page.query_selector("#graph-container canvas")
            if canvas:
                print("SUCCESS: Graph Canvas found. Engine initialized.")
            else:
                print("FAILURE: Graph Canvas NOT found.")

            # Check for Loading Error Message
            loading_msg = page.query_selector("#graph-loading span")
            if loading_msg:
                text = loading_msg.inner_text()
                color = loading_msg.evaluate("el => getComputedStyle(el).color")
                print(f"Loading Message: '{text}' (Color: {color})")
                
                if "ERR" in text or "rgb(239, 68, 68)" in color: # red-500 is ~ rgb(239, 68, 68)
                    print("FAILURE: Error message detected in UI.")
            else:
                print("INFO: Loading message element not found (maybe removed on success?)")

        except Exception as e:
            print(f"TEST EXCEPTION: {e}")
        
        finally:
            browser.close()

if __name__ == "__main__":
    verify()
