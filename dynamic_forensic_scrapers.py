from playwright.sync_api import sync_playwright
import hashlib
import time
import os
import sys

def dynamic_forensic_scrape(url, output_dir="evidence"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    print(f"[*] Starting advanced forensic acquisition of: {url}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Set a standard desktop viewport size
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        try:
            # 1. Load the page layout
            print("[*] Loading page layout...")
            response = page.goto(url, wait_until="load", timeout=30000)
            
            # 2. Explicitly wait for dynamic JS scripts to settle
            print("[*] Giving JavaScript 5 seconds to render content...")
            page.wait_for_timeout(5000)
            
            # 3. Capture the fully rendered DOM Source Code
            html_content = page.content().encode('utf-8')
            evidence_html = f"{output_dir}/rendered_source_{timestamp}.html"
            with open(evidence_html, 'wb') as f:
                f.write(html_content)
            html_hash = hashlib.sha256(html_content).hexdigest()
            
            # 4. Capture Visual Evidence (Full-Page Screenshot)
            print("[*] Capturing full-page visual evidence...")
            evidence_img = f"{output_dir}/screenshot_{timestamp}.png"
            page.screenshot(path=evidence_img, full_page=True)
            
            # Calculate hash of the image file
            with open(evidence_img, 'rb') as f:
                img_content = f.read()
            img_hash = hashlib.sha256(img_content).hexdigest()
            
            # 5. Log comprehensive metadata for the Chain of Custody
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
                log.write("EVIDENCE FILES & INTEGRITY SIGNATURES:\n")
                log.write(f"HTML Source File:      {os.path.basename(evidence_html)}\n")
                log.write(f"HTML SHA-256 Hash:     {html_hash}\n")
                log.write(f"Screenshot File:       {os.path.basename(evidence_img)}\n")
                log.write(f"Screenshot SHA-256:    {img_hash}\n")
                log.write("==================================================\n")
                
            print(f"[+] Acquisition successful!")
            print(f"[+] HTML saved to:  {evidence_html}")
            print(f"[+] Image saved to: {evidence_img}")
            print(f"[+] Log saved to:   {log_file}")
            
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
