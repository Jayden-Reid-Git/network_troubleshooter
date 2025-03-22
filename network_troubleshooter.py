import subprocess
import platform
import socket
import re

def get_ip_address():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.gaierror:
        return None

def is_apipa(ip_address):
    return ip_address.startswith("169.254")

def check_internet():
    try:
        if platform.system() == "Windows":
            subprocess.run(["ping", "-n", "4", "8.8.8.8"], check=True)
        else:
            subprocess.run(["ping", "-c", "4", "8.8.8.8"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def check_dns():
    try:
        socket.gethostbyname("www.google.com")
        return True
    except socket.gaierror:
        return False

def main():
    print("🔍 Running Network Troubleshooter...")

    # Step 1: Get IP Address
    ip_address = get_ip_address()
    if not ip_address:
        print("❌ No network connection detected.")
        return

    print(f"🖥️ Local IP Address: {ip_address}")

    # Step 2: Check for APIPA
    if is_apipa(ip_address):
        print("⚠️ Warning: Your IP address is in the APIPA range (169.254.x.x).")
        print("   This means your computer is not getting a proper IP from the router.")
        print("   Try restarting your router or checking your network cable.")
        return

    # Step 3: Check Internet Access
    if check_internet():
        print("✅ Internet connection is working.")
    else:
        print("❌ No internet access. Check your WiFi or Ethernet connection.")
        return

    # Step 4: Check DNS
    if check_dns():
        print("✅ DNS resolution is working correctly.")
    else:
        print("⚠️ Warning: DNS resolution failed.")
        print("   You may need to change your DNS settings (try Google DNS: 8.8.8.8).")

if __name__ == "__main__":
    main()
