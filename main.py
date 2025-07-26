import argparse
from colorama import Fore, Style, init

from modules.utils import logger, reporting
from modules.passive import whois_lookup, dns_enum, subdomain_enum
from modules.active import port_scanner, banner_grab, tech_detect

init(autoreset=True)  # For colorama to reset color after each print

log = logger.setup_logger("ReconTool")

def main():
    parser = argparse.ArgumentParser(description='Custom Reconnaissance Tool')
    parser.add_argument('target', help='Target domain')
    parser.add_argument('--whois', action='store_true', help='Perform WHOIS lookup')
    parser.add_argument('--dns', action='store_true', help='Perform DNS enumeration')
    parser.add_argument('--subdomains', action='store_true', help='Perform subdomain enumeration')
    parser.add_argument('--portscan', action='store_true', help='Perform port scanning')
    parser.add_argument('--banner', action='store_true', help='Perform banner grabbing')
    parser.add_argument('--tech', action='store_true', help='Detect technologies used by the target')
    parser.add_argument('--report', action='store_true', help='Generate report (TXT + JSON)')

    args = parser.parse_args()
    target = args.target

    data = {
        'target': target,
        'whois': None,
        'dns': None,
        'subdomains': None,
        'open_ports': None,
        'banners': None,
        'technologies': None
    }

    if args.whois:
        print(Fore.CYAN + Style.BRIGHT + "\n--- Starting WHOIS Lookup ---\n")
        data['whois'] = whois_lookup.run(target, logger=log)

    if args.dns:
        print(Fore.CYAN + Style.BRIGHT + "\n--- Starting DNS Enumeration ---\n")
        data['dns'] = dns_enum.run(target, logger=log)

    if args.subdomains:
        print(Fore.CYAN + Style.BRIGHT + "\n--- Starting Subdomain Enumeration ---\n")
        data['subdomains'] = subdomain_enum.run(target, logger=log)

    if args.portscan:
        print(Fore.CYAN + Style.BRIGHT + "\n--- Starting Port Scanning ---\n")
        data['open_ports'] = port_scanner.run(target, logger=log)

    if args.banner:
        print(Fore.CYAN + Style.BRIGHT + "\n--- Starting Banner Grabbing ---\n")
        open_ports = data.get('open_ports', [])
        if not open_ports:
            print(Fore.YELLOW + "Warning: No open ports available. Please run portscan before banner grabbing.")
        else:
            # Extract only port numbers if open_ports contains (port, service) tuples
            port_numbers = [port if isinstance(port, int) else port[0] for port in open_ports]
            data['banners'] = banner_grab.run(target, port_numbers, logger=log)

    if args.tech:
        print(Fore.CYAN + Style.BRIGHT + "\n--- Starting Technology Detection ---\n")
        data['technologies'] = tech_detect.run(target, logger=log)

    if args.report:
        print(Fore.WHITE + Style.BRIGHT + "\n--- Generating Report ---\n")
        reporting.generate_txt_report(target, data)
        reporting.generate_json_report(target, data)
        log.info("Reports (TXT & JSON) generated successfully.")

if __name__ == '__main__':
    main()