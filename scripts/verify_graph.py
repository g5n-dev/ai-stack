import http.server
import socketserver
import threading
import time
from playwright.sync_api import sync_playwright

PORT = 13131
DIRECTORY = "blog/public"
SCREENSHOT_PATH = "blog/tmp_scenarios_sidebar.png"

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
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        
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

            # Open sidebar by simulating a nodeSelect event
            node_id = page.evaluate(
                """() => {
                  const engine = window.graphEngine;
                  if (!engine || !engine.data || !Array.isArray(engine.data.nodes)) return null;
                  const prefer = engine.data.nodes.find(n => n && n.layer === "tag") || engine.data.nodes[0];
                  return prefer ? prefer.id : null;
                }"""
            )
            if node_id:
                print(f"Selecting node: {node_id}")
                page.evaluate(
                    """(id) => {
                      const engine = window.graphEngine;
                      if (!engine) return;
                      const node = engine.getNodeInfo(id);
                      if (!node) return;
                      engine.container.dispatchEvent(new CustomEvent("graph:nodeSelect", { detail: node, bubbles: true }));
                    }""",
                    node_id,
                )
                page.wait_for_selector("#detail-sidebar:not(.hidden-panel)", timeout=5000)
                time.sleep(1)

                sidebar_metrics = page.evaluate(
                    """() => {
                      const sidebar = document.getElementById("detail-sidebar");
                      const desc = document.getElementById("sidebar-desc");
                      const descWrap = desc ? desc.parentElement : null;
                      const s = sidebar ? sidebar.getBoundingClientRect() : null;
                      const d = desc ? desc.getBoundingClientRect() : null;
                      const w = descWrap ? descWrap.getBoundingClientRect() : null;
                      const style = desc ? getComputedStyle(desc) : null;
                      return {
                        sidebar: s ? { width: s.width, height: s.height } : null,
                        desc: d ? { width: d.width, height: d.height } : null,
                        descWrap: w ? { width: w.width, height: w.height } : null,
                        fontSize: style ? style.fontSize : null,
                        lineHeight: style ? style.lineHeight : null,
                        descTextLen: desc ? (desc.textContent || "").trim().length : 0,
                      };
                    }"""
                )
                print(f"Sidebar metrics: {sidebar_metrics}")

                page.screenshot(path=SCREENSHOT_PATH, full_page=True)
                print(f"Saved screenshot: {SCREENSHOT_PATH}")

                if sidebar_metrics.get("sidebar") and sidebar_metrics["sidebar"]["width"] < 380:
                    print("FAILURE: Sidebar width too small.")
                if sidebar_metrics.get("descWrap") and sidebar_metrics["descWrap"]["height"] < 180:
                    print("FAILURE: Description box height too small.")
                if sidebar_metrics.get("descTextLen", 0) == 0:
                    print("FAILURE: Description text missing.")
            else:
                print("FAILURE: Could not find a node id to select for sidebar test.")

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
