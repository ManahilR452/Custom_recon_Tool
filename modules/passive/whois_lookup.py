import whois
from datetime import datetime

def format_date(date_value):
    """Format single or list of datetime to readable string."""
    if isinstance(date_value, list) and date_value:
        date_value = date_value[0]  # Pick the first date if multiple
    if isinstance(date_value, datetime):
        return date_value.strftime('%Y-%m-%d %H:%M:%S')
    return date_value

def run(domain, logger=None):
    if logger:
        logger.info("Starting WHOIS Lookup...")

    try:
        w = whois.whois(domain)
        result = {
            'Domain Name': w.domain_name,
            'Registrar': w.registrar,
            'Creation Date': format_date(w.creation_date),
            'Expiration Date': format_date(w.expiration_date),
            'Name Servers': w.name_servers,
            'Emails': w.emails
        }

        if logger:
            logger.info("WHOIS lookup completed successfully.")
            for key, value in result.items():
                logger.info(f"{key}: {value}")
        else:
            print("WHOIS lookup completed successfully.\n")
            for key, value in result.items():
                print(f"{key}: {value}")

        return result

    except Exception as e:
        if logger:
            logger.error(f"WHOIS lookup failed: {e}")
        else:
            print(f"WHOIS lookup failed: {e}")
        return {}