import re
import tldextract

def extract_features(url):
    features = []

    # 1. URL length
    features.append(len(url))

    # 2. HTTPS present or not
    features.append(1 if "https" in url else 0)

    # 3. Dot count
    features.append(url.count('.'))

    # 4. Slash count
    features.append(url.count('/'))

    # 5. IP address in URL
    features.append(1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0)

    # 6. Domain length
    ext = tldextract.extract(url)
    features.append(len(ext.domain))

    return features