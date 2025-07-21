import dns.resolver

def run(domain, logger=None):
    if logger:
        logger.info("Starting DNS Enumeration...")

    records = {'A': [], 'MX': [], 'NS': [], 'TXT': []}

    try:
        records['A'] = [r.address for r in dns.resolver.resolve(domain, 'A')]
        if logger: logger.info(f"A record(s) found: {records['A']}")
    except: pass

    try:
        records['MX'] = [r.exchange.to_text() for r in dns.resolver.resolve(domain, 'MX')]
        if logger: logger.info(f"MX record(s) found: {records['MX']}")
    except: pass

    try:
        records['NS'] = [r.to_text() for r in dns.resolver.resolve(domain, 'NS')]
        if logger: logger.info(f"NS record(s) found: {records['NS']}")
    except: pass

    try:
        records['TXT'] = [r.to_text() for r in dns.resolver.resolve(domain, 'TXT')]
        if logger: logger.info(f"TXT record(s) found: {records['TXT']}")
    except: pass

    return records

