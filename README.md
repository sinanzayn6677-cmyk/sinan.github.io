# Dynamic Forensic Web Scraper

A forensically sound web acquisition and automation tool built in Python for Linux environments. This tool simultaneously captures target data across the Application, Presentation, and Network layers, ensuring chain-of-custody data integrity using cryptographic hashing.

---

## 🚀 Features

* **Dynamic DOM Capture:** Uses headless Chromium (Playwright) to fully render JavaScript-heavy modern web applications (e.g., ChatGPT) before capturing source code.
* **Visual Evidence Preservation:** Automatically generates high-resolution, full-page PNG screenshots.
* **Network Infrastructure Mapping:** Performs real-time DNS resolution to log target IP addresses and extracts active SSL/TLS certificate details (Issuer, Serial Number, Expiration).
* **Cryptographic Integrity & Logging:** Generates unique SHA-256 hashes for both the HTML and screenshot evidence, embedding them into a tamper-proof acquisition log for chain-of-custody verification.
* **Bulk Ingestion & Automation:** Supports single-target acquisition or automated batch processing via text file inputs.

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/sinanzayn6677-cmyk/sinan.github.io.git](https://github.com/sinanzayn6677-cmyk/sinan.github.io.git)
cd sinan.github.io
2. Configure Environment & Dependencies
It is highly recommended to run this tool inside an isolated Python virtual environment to prevent package conflicts:

Bash
# Install virtual environment package if missing
sudo apt install python3-venv -y

# Create and activate environment
python3 -m venv scraper_env
source scraper_env/bin/activate

# Install required forensic dependencies
pip install -r requirements.txt
playwright install chromium
📖 Usage
Option A: Single URL Target
Pass a single URL directly as a command-line argument:

Bash
python3 dynamic_forensic_scrapers.py [https://example.com](https://example.com)
Option B: Bulk Automation Ingestion
Create a text file (e.g., targets.txt) containing one target URL per line, then pass the file path to the script:

Bash
python3 dynamic_forensic_scrapers.py targets.txt
📂 Evidence Structure & Chain of Custody
All captured data is cleanly organized within the evidence/ directory and isolated by target domain name to keep case files organized:

Plaintext
evidence/
├── chatgpt_com/
│   ├── acquisition_20260519_181740.log       # Cryptographic hashes & network metadata
│   ├── source_20260519_181740.html            # Fully rendered DOM source code
│   └── screenshot_20260519_181740.png        # Full-page visual layout capture
└── example_com/
    ├── acquisition_20260519_183015.log
    ├── source_20260519_183015.html
    └── screenshot_20260519_183015.png
Verification
To verify the integrity of an acquired asset against the generated log file, use the native Linux utility:

Bash
sha256sum evidence/chatgpt_com/source_20260519_181740.html
⚖️ License
This project is open-source and available under the MIT License.
