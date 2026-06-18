# 🛡️ Phishing URL Detection Web App

> Analyze. Detect. Protect. A full-stack web application that uses advanced rule-based cybersecurity algorithms to detect whether a given URL is safe or potentially a phishing attack.

## ✨ Features

- **Real-Time URL Validation**: Instantly checks URLs upon submission.
- **Advanced Phishing Detection Logic**: Utilizes 12 rigorous security checks:
  - 🚩 Presence of the `@` symbol.
  - 🚩 Suspicious keywords (e.g., login, verify, bank, secure).
  - 🚩 Exceptionally long URLs.
  - 🚩 Unencrypted HTTP connections.
  - 🚩 IP address spoofing instead of standard domain names.
  - 🚩 Exceptionally high number of subdomains.
  - 🚩 Use of URL shortening services (e.g., bit.ly, tinyurl).
  - 🚩 Malicious/Spam Top-Level Domains (TLDs).
  - 🚩 Multiple hyphens in the domain.
  - 🚩 Punycode / Homograph attack detection (`xn--`).
  - 🚩 Non-standard/suspicious network ports.
  - 🚩 Suspicious executable file extensions in paths.
- **Premium UI/UX Design**: Features a modern, responsive dark mode interface with glassmorphism, animated glowing backgrounds, and dynamic color-coded indicators.
- **URL History Tracking**: Automatically saves and displays a local history of recently checked URLs for quick reference.

## 💻 Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python 3, Flask
- **Production Server**: Gunicorn

## 🚀 Getting Started

### Prerequisites

Make sure you have [Python](https://www.python.org/downloads/) installed on your system.

### Installation

1. Clone this repository (or download the zip):
   ```bash
   git clone https://github.com/YOUR_USERNAME/phishing-detector.git
   cd phishing-detector
   ```

2. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally

Start the Flask application:
```bash
python app.py
```
Open your web browser and navigate to `http://127.0.0.1:5000` to view the app.

## 🌐 Live Deployment

This project is configured and ready to be deployed on platforms like [Render](https://render.com/).

1. Push your code to a GitHub repository.
2. Create a new **Web Service** on Render and connect your repository.
3. Configure the deployment settings:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. Click deploy and your app will be live!
