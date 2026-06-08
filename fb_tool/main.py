#!/usr/bin/env python3
"""
fb_tool - Personal Facebook Utility for Termux
Personal use only. One action per run.
"""

import sys
import signal
from config import load_config, update_alias
from actions import open_post, switch_account

def signal_handler(sig, frame):
    print("\n[!] Interrupted. Exiting.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


def main():
    config = load_config()
    delays = config["delays"]

    print("fb_tool - Personal Facebook Utility")
    print("------------------------------------")
    print("[1] Switch Account")
    print("[2] Open Facebook Post")
    print("[3] Rename Account Alias")
    print("[4] Exit")
    print()

    choice = input("Choice: ").strip()

    if choice == "1":
        print()
        accounts = config["accounts"]
        for acc in accounts:
            print(f"  [{acc['id']}] {acc['alias']}")
        print("  [0] Cancel")
        print()
        sel = input("Select account: ").strip()
        if sel == "0":
            sys.exit(0)
        account = next((a for a in accounts if str(a["id"]) == sel), None)
        if not account:
            print("[-] Invalid selection.")
            sys.exit(1)
        print()
        switch_account(account, delay=delays["after_switch"])

    elif choice == "2":
        print()
        url = input("Paste Facebook post URL: ").strip()
        if not url:
            print("[-] No URL entered.")
            sys.exit(1)
        if not (url.startswith("https://www.facebook.com/") or
                url.startswith("https://m.facebook.com/") or
                url.startswith("https://fb.watch/")):
            print("[-] Invalid URL. Must be a Facebook link.")
            sys.exit(1)
        print()
        open_post(url, delay=delays["after_launch"])

    elif choice == "3":
        print()
        accounts = config["accounts"]
        for acc in accounts:
            print(f"  [{acc['id']}] {acc['alias']}")
        print("  [0] Cancel")
        print()
        sel = input("Select account to rename: ").strip()
        if sel == "0":
            sys.exit(0)
        account = next((a for a in accounts if str(a["id"]) == sel), None)
        if not account:
            print("[-] Invalid selection.")
            sys.exit(1)
        new_name = input(f"New name for '{account['alias']}': ").strip()
        if not new_name:
            print("[-] Name cannot be empty.")
            sys.exit(1)
        update_alias(account["id"], new_name)
        print(f"[+] Renamed to '{new_name}'")

    elif choice == "4":
        sys.exit(0)

    else:
        print("[-] Invalid choice.")
        sys.exit(1)


if __name__ == "__main__":
    main()
