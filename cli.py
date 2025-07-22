import sys
from main import main

def cli_entry():
    # You can just call main() because main() already uses argparse internally.
    main()

if __name__ == '__main__':
    cli_entry()