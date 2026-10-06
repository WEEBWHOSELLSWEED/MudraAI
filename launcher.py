import os
import sys
import time
import json
import socket
import threading
import urllib.request
import subprocess
import webbrowser

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
NGROK_BIN = r"D:\tools\ngrok.exe"

def kill_existing_processes():
    # Kill existing ngrok instances
    subprocess.run("taskkill /F /IM ngrok.exe /T", shell=True, capture_output=True)
    # Kill any lingering process on port 5000
    subprocess.run("powershell -Command \"Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | Select -Expand OwningProcess | Stop-Process -Force -ErrorAction SilentlyContinue\"", shell=True, capture_output=True)
    time.sleep(1)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def copy_to_clipboard(text):
    try:
        p = subprocess.Popen(['clip'], stdin=subprocess.PIPE, close_fds=True)
        p.communicate(input=text.strip().encode('utf-8'))
        return True
    except Exception:
        return False

def wait_for_flask(port=5000, timeout=12):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=1) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            time.sleep(0.3)
    return False

def get_ngrok_url(timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=1) as resp:
                data = json.loads(resp.read().decode())
                tunnels = data.get("tunnels", [])
                for t in tunnels:
                    url = t.get("public_url", "")
                    if url.startswith("https://"):
                        return url
                if tunnels:
                    return tunnels[0].get("public_url", "")
        except Exception:
            time.sleep(0.3)
    return None

def main():
    print("=" * 65, flush=True)
    print("           MUDRAAI — 1-CLICK ALL-IN-ONE LAUNCHER", flush=True)
    print("=" * 65, flush=True)

    print("\n[*] Cleaning up previous sessions...", flush=True)
    kill_existing_processes()

    port = 5000
    print(f"[1/3] Starting MudraAI recognition server on port {port}...", flush=True)
    
    flask_proc = subprocess.Popen(
        [sys.executable, "app.py"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    def log_flask():
        for line in flask_proc.stdout:
            pass

    threading.Thread(target=log_flask, daemon=True).start()

    if not wait_for_flask(port, timeout=10):
        print("[!] Flask server initializing...", flush=True)

    print("[2/3] Establishing high-speed Ngrok HTTPS tunnel...", flush=True)
    
    tunnel_proc = subprocess.Popen(
        [NGROK_BIN, "http", str(port), "--log=stdout"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    def log_tunnel():
        for line in tunnel_proc.stdout:
            pass

    threading.Thread(target=log_tunnel, daemon=True).start()

    tunnel_url = get_ngrok_url(timeout=10)

    if not tunnel_url:
        time.sleep(2)
        tunnel_url = get_ngrok_url(timeout=5)

    if not tunnel_url:
        print("[!] Warning: Tunnel not responding, fallback to local URL.", flush=True)
        tunnel_url = f"http://127.0.0.1:{port}"

    local_ip = get_local_ip()

    print("[3/3] Copying link to clipboard & opening browser...", flush=True)
    copied = copy_to_clipboard(tunnel_url)
    
    time.sleep(1)
    webbrowser.open(tunnel_url)

    print("\n" + "=" * 65, flush=True)
    print("                     MUDRAAI IS NOW LIVE!", flush=True)
    print("=" * 65, flush=True)
    print(f"\n  >> PUBLIC HTTPS LINK:  {tunnel_url}", flush=True)
    if copied:
        print("     [COPIED TO CLIPBOARD!] Press Ctrl + V to share.", flush=True)
    print(f"\n  >> LOCAL WI-FI LINK:   http://{local_ip}:{port}", flush=True)
    print("     (Open on any phone connected to the same Wi-Fi)", flush=True)
    print("\n" + "-" * 65, flush=True)
    print("  * If the link prompts with 'Visit Site' on first open,", flush=True)
    print("    click 'Visit Site' to access the MudraAI dashboard.", flush=True)
    print("  * Keep this window OPEN while presenting.", flush=True)
    print("  * Press Ctrl + C (or close this window) to stop MudraAI.", flush=True)
    print("=" * 65 + "\n", flush=True)

    try:
        while True:
            time.sleep(1)
            if flask_proc.poll() is not None:
                print(f"\n[!] Flask server stopped (code: {flask_proc.poll()})", flush=True)
                break
            if tunnel_proc.poll() is not None:
                print(f"\n[!] Tunnel process stopped (code: {tunnel_proc.poll()})", flush=True)
                break
    except KeyboardInterrupt:
        print("\nStopping server and closing tunnel...", flush=True)
    finally:
        flask_proc.terminate()
        tunnel_proc.terminate()
        kill_existing_processes()
        print("Clean shutdown complete.", flush=True)

if __name__ == "__main__":
    main()
