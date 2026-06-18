import re
from flask import Flask, render_template, request, jsonify
from urllib.parse import urlparse

app = Flask(__name__)

def check_phishing(url):
    reasons = []
    is_suspicious = False

    # Check 1: Presence of "@" symbol
    if "@" in url:
        is_suspicious = True
        reasons.append("URL contains '@' symbol.")

    # Check 2: Suspicious keywords
    suspicious_keywords = ['login', 'verify', 'bank', 'secure', 'update', 'account']
    url_lower = url.lower()
    found_keywords = [kw for kw in suspicious_keywords if kw in url_lower]
    if found_keywords:
        is_suspicious = True
        reasons.append(f"URL contains suspicious keywords: {', '.join(found_keywords)}.")

    # Check 3: URL length
    if len(url) > 75:
        is_suspicious = True
        reasons.append(f"URL is exceptionally long ({len(url)} characters).")

    # Parse URL for domain-specific checks
    try:
        # Add a default scheme if missing for proper parsing
        parse_url = url if "://" in url else "http://" + url
        parsed_url = urlparse(parse_url)
        domain = parsed_url.netloc.lower()

        # Check 4: Use of HTTP instead of HTTPS
        if url.startswith('http://'):
            is_suspicious = True
            reasons.append("URL uses unencrypted HTTP instead of secure HTTPS.")

        # Rare Rule 1: Use of IP Address instead of domain name
        ip_pattern = re.compile(
            r'^(([01]?\d\d?|2[0-4]\d|25[0-5])\.){3}([01]?\d\d?|2[0-4]\d|25[0-5])(:\d+)?$'
        )
        if ip_pattern.match(domain):
            is_suspicious = True
            reasons.append("URL uses an IP address instead of a standard domain name.")

        # Rare Rule 2: Multiple subdomains (e.g., login.bank.com.phishing.com)
        parts = domain.split('.')
        # Removing empty strings just in case
        parts = [p for p in parts if p]
        if len(parts) > 3 and parts[-1] not in ['uk', 'au', 'in', 'jp', 'br']: # Basic heuristic, > 3 parts usually means multiple subdomains unless it's co.uk etc. We'll be simpler and say >4 is very suspicious.
            if len(parts) > 4:
                is_suspicious = True
                reasons.append(f"URL has an unusually high number of subdomains ({len(parts)}).")

        # Rare Rule 3: Use of URL Shorteners
        shorteners = ['bit.ly', 'goo.gl', 't.co', 'tinyurl.com', 'ow.ly', 'is.gd', 'buff.ly']
        if any(short in domain for short in shorteners):
            is_suspicious = True
            reasons.append("URL uses a shortening service, which can hide the true destination.")

        # Rare Rule 4: Suspicious TLDs
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.zip', '.xyz', '.top']
        if any(domain.endswith(tld) for tld in suspicious_tlds):
            is_suspicious = True
            reasons.append("URL uses a Top-Level Domain (TLD) commonly associated with spam/phishing.")

        # Rare Rule 5: Presence of multiple hyphens in domain
        if domain.count('-') > 2:
            is_suspicious = True
            reasons.append("URL domain contains multiple hyphens, often used to spoof legitimate sites.")

        # Rare Rule 6: Punycode / Homograph attack detection
        if domain.startswith('xn--') or '.xn--' in domain:
            is_suspicious = True
            reasons.append("URL uses Punycode (internationalized domain), which can be used for homograph attacks.")

        # Rare Rule 7: Uncommon or suspicious ports
        if parsed_url.port and parsed_url.port not in [80, 443]:
            is_suspicious = True
            reasons.append(f"URL uses a non-standard port ({parsed_url.port}), which is unusual for standard web traffic.")

        # Rare Rule 8: Suspicious file extensions
        suspicious_extensions = ['.exe', '.apk', '.bat', '.cmd', '.scr', '.msi']
        if any(parsed_url.path.lower().endswith(ext) for ext in suspicious_extensions):
            is_suspicious = True
            reasons.append("URL points directly to a potentially dangerous executable file.")

    except Exception as e:
        # If parsing fails, we ignore scheme checks
        pass

    return {
        "status": "Suspicious" if is_suspicious else "Safe",
        "reasons": reasons
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/check', methods=['POST'])
def check_url():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    # Simple validation to ensure it looks like a URL if they didn't include http/https
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url # Prefix for parsing purposes, though ideally user provides full URL
        
    result = check_phishing(url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
