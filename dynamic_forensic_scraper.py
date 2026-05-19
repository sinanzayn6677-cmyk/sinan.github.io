from playwright.sync_api import sync_playwright
import hashlib
import time
import os
import sys
import socket
import ssl
from urllib.parse import urlparse
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def get_network_evidence(url):
    """Gathers real-time IP, DNS, and SSL Certificate metadata."""
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    port = parsed_url.port if parsed_url.port else (443 if parsed_url.scheme == 'https' else 80)
    
    network_data = {
        "resolved_ip": "Unknown",
        "cert_issuer": "N/A",
        "cert_serial": "N/A",
        "cert_expires": "N/A"
    }
    
    try:
        # 1. Resolve IP Address (DNS lookup)
        network_data["resolved_ip"] = socket.gethostbyname(hostname)
        
        # 2. Extract SSL Certificate details if HTTPS
        if parsed_url.scheme == 'https':
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert_der = ssock.getpeercert(binary_form=True)
                    cert = x509.load_der_x509_certificate(cert_der, default_backend())
                    
                    # Extract key attributes
                    network_data["cert_issuer"] = cert.issuer.rfc4514_string()
                    network_data["cert_serial"] = str(cert.serial_number)
                    network_data["cert_expires"] = cert.not_valid_after_utc.strftime('%Y-%m-%d %H:%M:%S UTC')
    except Exception as e:
        print(f"[!] Warning: Could not collect full network telemetry: {e}")
        
    return network_data

def dynamic_forensic_scrape(url, output_dir="evidence"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    print(f"[*] Starting advanced forensic network acquisition of: {url}")
    
    # Gather network infrastructure metadata first
    net_evidence = get_network_evidence(url)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        try:
            print("[*] Loading page layout via Chromium...")
            response = page.goto(url, wait_until="load", timeout=30000)
            
            print("[*] Giving JavaScript 5 seconds to render content...")
            page.wait_for_timeout(5000)
            
            # Capture HTML Source Code
            html_content = page.content().encode('utf-8')
            evidence_html = f"{output_dir}/rendered_source_{timestamp}.html"
            with open(evidence_html, 'wb') as f:
                f.write(html_content)
            html_hash = hashlib.sha256(html_content).hexdigest()
            
            # Capture Visual Evidence
            print("[*] Capturing full-page visual evidence...")
            evidence_img = f"{output_dir}/screenshot_{timestamp}.png"
            page.screenshot(path=evidence_img, full_page=True)
            
            with open(evidence_img, 'rb') as f:
                img_content = f.read()
            img_hash = hashlib.sha256(img_content).hexdigest()
            
            # Log Generation (Now including Network layer details)
            log_file = f"{output_dir}/acquisition_{timestamp}.log"
            status_code = response.status if response else "Unknown"
            
            with open(log_file, 'w') as log:
                log.write("==================================================\n")
                log.write("         DIGITAL FORENSIC ACQUISITION LOG         \n")
                log.write("==================================================\n")
                log.write(f"Target URL:            {url}\n")
                log.write(f"Acquisition Timestamp: {timestamp}\n")
                log.write(f"HTTP Status Code:      {status_code}\n")
                log.write(f"Browser Engine:        Playwright (Headless Chromium)\n")
                log.write("--------------------------------------------------\n")
                log.write("NETWORK & INFRASTRUCTURE EVIDENCE:\n")
                log.write(f"Resolved Target IP:    {net_evidence['resolved_ip']}\n")
                log.write(f"SSL Cert Issuer:       {net_evidence['cert_issuer']}\n")
                log.write(f"SSL Cert Serial:       {net_evidence['cert_serial']}\n")
                log.write(f"SSL Cert Expiration:   {net_evidence['cert_expires']}\n")
                log.write("--------------------------------------------------\n")
                log.write("EVIDENCE FILES & INTEGRITY SIGNATURES:\n")
                log.write(f"HTML Source File:      {os.path.basename(evidence_html)}\n")
                log.write(f"HTML SHA-256 Hash:     {html_hash}\n")
                log.write(f"Screenshot File:       {os.path.basename(evidence_img)}\n")
                log.write(f"Screenshot SHA-256:    {img_hash}\n")
                log.write("==================================================\n")
                
            print(f"[+] Acquisition complete with infrastructure mapping!")
            print(f"[+] Log updated: {log_file}")
            
        except Exception as e:
            print(f"[-] Error during dynamic acquisition: {e}")
            
        finally:
            browser.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 dynamic_forensic_scraper.py <URL>")
    else:
        target_url = sys.argv[1]
        dynamic_forensic_scrape(target_url)
