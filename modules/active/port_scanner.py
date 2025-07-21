import socket
import threading
import time

COMMON_PORTS = {
    21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
    53: 'DNS', 80: 'HTTP', 110: 'POP3', 143: 'IMAP', 
    443: 'HTTPS', 445: 'SMB', 3306: 'MySQL', 3389: 'RDP',
    8080: 'HTTP-Alt', 8443: 'HTTPS-Alt'
}

THREAD_COUNT = 100
SCAN_TIMEOUT = 0.5


def prompt_port_scan_choice():
    while True:
        print("\nPort Scanning Options:")
        print("1. Scan common ports")
        print("2. Define custom port range")
        choice = input("Select an option (1 or 2): ").strip()

        if choice == '1':
            return list(COMMON_PORTS.keys()), 'common'

        elif choice == '2':
            start_port = int(input("Enter start port (e.g., 1): "))
            end_port = int(input("Enter end port (e.g., 1000): "))
            total_ports = end_port - start_port + 1

            # Rough estimate: number of ports / threads * timeout
            estimated_time = (total_ports / THREAD_COUNT) * SCAN_TIMEOUT
            print(f"Estimated scan time for ports {start_port}-{end_port}: {estimated_time:.1f} seconds")

            proceed = input("Proceed with scan? (y/n): ").strip().lower()
            if proceed == 'y':
                return list(range(start_port, end_port + 1)), 'custom'
            else:
                print("Scan cancelled. Let's choose again.\n")
        else:
            print("Invalid input. Please select 1 or 2.\n")


def scan_port(target, port, open_ports, logger=None):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(SCAN_TIMEOUT)
            result = s.connect_ex((target, port))
            if result == 0:
                service = COMMON_PORTS.get(port, 'Unknown')
                open_ports.append((port, service))
                if logger:
                    logger.info(f"Port {port} is OPEN ({service}) on {target}")
                else:
                    print(f"Port {port} is OPEN ({service}) on {target}")
    except Exception:
        pass


def run(target, logger=None):
    ports, scan_type = prompt_port_scan_choice()
    open_ports = []
    threads = []

    if logger:
        logger.info("Starting Port Scanning...")

    for port in ports:
        t = threading.Thread(target=scan_port, args=(target, port, open_ports, logger))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    open_ports.sort()
    return open_ports