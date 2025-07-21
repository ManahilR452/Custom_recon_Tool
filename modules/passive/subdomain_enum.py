import requests


def query_crtsh(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            data = response.json()
            subdomains = set()
            for entry in data:
                name = entry.get('name_value', '')
                for sub in name.split('\n'):
                    if domain in sub:
                        subdomains.add(sub.strip())
            return list(subdomains)
    except Exception as e:
        print(f"Error querying crt.sh: {e}")
    return None


def query_alienvault(domain, api_key):
    url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"
    headers = {'X-OTX-API-KEY': api_key}
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            data = response.json()
            subdomains = set()
            for record in data.get('passive_dns', []):
                hostname = record.get('hostname')
                if hostname and domain in hostname:
                    subdomains.add(hostname)
            return list(subdomains)
    except Exception as e:
        print(f"Error querying AlienVault OTX: {e}")
    return None


def query_securitytrails(domain, api_key):
    url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains"
    headers = {'APIKEY': api_key}
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            data = response.json()
            subdomains = [f"{sub}.{domain}" for sub in data.get('subdomains', [])]
            return subdomains
    except Exception as e:
        print(f"Error querying SecurityTrails: {e}")
    return None


def run(domain, logger=None, alienvault_api_key=None, securitytrails_api_key=None):
    if logger:
        logger.info("Starting Subdomain Enumeration...")

    subdomains = query_crtsh(domain)
    if subdomains:
        if logger:
            logger.info(f"Found {len(subdomains)} subdomains via crt.sh")
        print("Subdomains found:")
        for sub in subdomains:
            print(f"- {sub}")
        return subdomains

    if alienvault_api_key:
        if logger:
            logger.info("Trying AlienVault OTX...")
        subdomains = query_alienvault(domain, alienvault_api_key)
        if subdomains:
            if logger:
                logger.info(f"Found {len(subdomains)} subdomains via AlienVault OTX")
            print("Subdomains found:")
            for sub in subdomains:
                print(f"- {sub}")
            return subdomains

    if securitytrails_api_key:
        if logger:
            logger.info("Trying SecurityTrails...")
        subdomains = query_securitytrails(domain, securitytrails_api_key)
        if subdomains:
            if logger:
                logger.info(f"Found {len(subdomains)} subdomains via SecurityTrails")
            print("Subdomains found:")
            for sub in subdomains:
                print(f"- {sub}")
            return subdomains

    if logger:
        logger.error("Subdomain enumeration failed via all available sources.")
    return []

