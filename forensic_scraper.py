import requests
import hashlib
import time
import os
import sys

def forensic_scrape(url, output_dir="evidence"):
    # Create an evidence directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Generate a precise timestamp
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    print(f"[*] Starting forensic acquisition of: {url}")
    
    try:
        # Fetch the webpage
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Forensic-Acquisition-Tool/1.0)'}
        response = requests.get(url, headers=headers, timeout=10)
        
        # Step 1: Save the raw HTML data
        html_content = response.text.encode('utf-8')
        evidence_file = f"{output_dir}/acquisition_{timestamp}.html"
        
        with open(evidence_file, 'wb') as f:
            f.write(html_content)
            
        # Step 2: Generate a SHA-256 Hash for forensic integrity
        sha256_hash = hashlib.sha256(html_content).hexdigest()
        
        # Step 3: Log the metadata
        log_file = f"{output_dir}/acquisition_{timestamp}.log"
        with open(log_file, 'w') as log:
            log.write(f"Target URL: {url}\n")
            log.write(f"Acquisition Timestamp: {timestamp}\n")
            log.write(f"Status Code: {response.status_code}\n")
            log.write(f"SHA-256 Hash: {sha256_hash}\n")
            
        print(f"[+] Acquisition successful!")
        print(f"[+] Evidence saved to: {evidence_file}")
        print(f"[+] SHA-256 Hash: {sha256_hash}")
        
    except requests.exceptions.RequestException as e:
        print(f"[-] Network error during acquisition: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 forensic_scraper.py <URL>")
    else:
        target_url = sys.argv[1]
        forensic_scrape(target_url)
