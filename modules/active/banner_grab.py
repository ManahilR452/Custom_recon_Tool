import socket
import ssl
import threading

DEFAULT_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3389, 8080, 8443]
TIMEOUT = 3

def grab_banner(target, port):
    try:
        with socket.create_connection((target, port), timeout=TIMEOUT) as sock:
            if port in [443, 8443]:
                context = ssl.create_default_context()
                with context.wrap_socket(sock, server_hostname=target) as ssock:
                    cert = ssock.getpeercert()
                    issuer = cert.get('issuer') if cert else None
                    return f'SSL Issuer: {issuer}' if issuer else 'SSL certificate unavailable'
            else:
                sock.sendall(b'HEAD / HTTP/1.0\r\n\r\n')
                data = sock.recv(1024).decode(errors='ignore').strip()
                return data.split('\n')[0] if data else 'No banner received'
    except Exception as e:
        return f'Error - {e}'

def get_ports_choice():
    print("\nPort Selection Options:")
    print("1. Scan common ports (21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3389, 8080, 8443)")
    print("2. Specify custom ports (comma-separated)")
    print("3. Define port range")
    choice = input("Select an option (1, 2, or 3): ").strip()

    if choice == '1':
        return sorted(DEFAULT_PORTS)
    elif choice == '2':
        ports = input("Enter ports separated by commas (e.g., 22,80,443): ")
        return sorted([int(p.strip()) for p in ports.split(',') if p.strip().isdigit()])
    elif choice == '3':
        start = int(input("Enter start port: "))
        end = int(input("Enter end port: "))
        return sorted(range(start, end + 1))
    else:
        print("Invalid choice. Using default ports.")
        return sorted(DEFAULT_PORTS)

def run(target, ports=None, logger=None):
    if ports is None:
        ports = get_ports_choice()

    print("\nStarting banner grabbing...")

    banners = {}
    failed_ports = {}

    def worker(port):
        banner = grab_banner(target, port)
        if not banner.startswith('Error'):
            banners[port] = banner
            if logger:
                logger.info(f"Port {port}: {banner}")
            else:
                print(f"Port {port}: {banner}")
        else:
            failed_ports[port] = banner

    threads = []
    for port in ports:
        t = threading.Thread(target=worker, args=(port,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    if failed_ports:
        choice = input("\nDo you want to see details of failed/closed ports? (y/n): ").strip().lower()
        if choice == 'y':
            print("\n--- Verbose Output for Failed Ports ---")
            for port in sorted(failed_ports):
                print(f"Port {port}: {failed_ports[port]}")

    return dict(sorted(banners.items()))