import requests

def run(domain, logger=None):
    if logger:
        logger.info("Starting Technology Detection...")

    technologies = []

    try:
        response = requests.get(f"http://{domain}", timeout=5)
        server = response.headers.get('Server', 'Unknown')
        x_powered_by = response.headers.get('X-Powered-By', 'Unknown')
        content_type = response.headers.get('Content-Type', 'Unknown')

        technologies.append({
            'Server': server,
            'X-Powered-By': x_powered_by,
            'Content-Type': content_type
        })

        if logger:
            logger.info(f"Technologies detected: {technologies}")
    except Exception as e:
        if logger:
            logger.warning(f"Technology detection failed: {e}")

    return technologies