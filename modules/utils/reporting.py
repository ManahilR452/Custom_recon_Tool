import json
import os
from datetime import datetime

def generate_txt_report(target, data):
    if not os.path.exists('reports'):
        os.makedirs('reports')

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'reports/{target}_recon_report_{timestamp}.txt'
    
    with open(filename, 'w') as f:
        f.write(f"Reconnaissance Report for {target}\n")
        f.write(f"Generated on: {datetime.now()}\n")
        f.write("="*60 + "\n\n")
        
        for section, content in data.items():
            f.write(f"--- {section.upper()} ---\n")
            if isinstance(content, list) or isinstance(content, dict):
                f.write(json.dumps(content, indent=4))
            else:
                f.write(str(content))
            f.write("\n\n")

    print(f"[+] Text report saved to: {filename}")


def generate_json_report(target, data):
    if not os.path.exists('reports'):
        os.makedirs('reports')

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'reports/{target}_recon_report_{timestamp}.json'

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"[+] JSON report saved to: {filename}")
