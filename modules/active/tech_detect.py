import requests

REQUEST_TIMEOUT = 5  # seconds

def run(target, logger=None):
    try:
        response = requests.get(f'http://{target}', timeout=REQUEST_TIMEOUT)
        headers = response.headers
        if logger:
            logger.info(f"Headers received: {headers}")

        technologies = {
            'Server': headers.get('Server', 'Unknown'),
            'X-Powered-By': headers.get('X-Powered-By', 'Unknown'),
            'Content-Type': headers.get('Content-Type', 'Unknown'),
        }
        return [technologies]
    except Exception as e:
        if logger:
            logger.error(f"Technology detection failed: {e}")
        return {}
