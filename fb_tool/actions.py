import subprocess
import time
from logger import get_logger

logger = get_logger()

FB_PKG      = "com.facebook.lite"
FB_FULL_PKG = "com.facebook.katana"  # fallback only


def run(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return result.returncode == 0, result.stdout.strip()
    except FileNotFoundError as e:
        return False, str(e)
    except subprocess.TimeoutExpired:
        return False, "timed out"
    except Exception as e:
        return False, str(e)


def am_start(uri=None, action=None, pkg=None, component=None):
    cmd = ["am", "start"]
    if action:    cmd += ["-a", action]
    if uri:       cmd += ["-d", uri]
    if pkg:       cmd += ["-p", pkg]
    if component: cmd += ["-n", component]
    return run(cmd)


def open_post(url, delay=3.0):
    logger.info(f"Opening post: {url}")
    print(f"[*] Launching: {url}")

    # Method 1: termux-open
    ok, out = run(["termux-open", url])
    if ok:
        print(f"[*] Waiting {delay}s for post to load...")
        time.sleep(delay)
        print("[+] Done. Post should be open in Facebook Lite.")
        logger.info("Opened via termux-open")
        return True

    # Method 2: am start VIEW intent (FB Lite)
    print("[*] termux-open failed, trying am start...")
    ok, out = am_start(uri=url, action="android.intent.action.VIEW", pkg=FB_PKG)
    if ok:
        print(f"[*] Waiting {delay}s for post to load...")
        time.sleep(delay)
        print("[+] Done. Post should be open in Facebook Lite.")
        logger.info("Opened via am start (FB Lite)")
        return True

    # Method 3: fb:// URI scheme
    fb_uri = url.replace("https://www.facebook.com", "fb://")
    ok, out = am_start(uri=fb_uri, action="android.intent.action.VIEW")
    if ok:
        print(f"[*] Waiting {delay}s for post to load...")
        time.sleep(delay)
        print("[+] Done. Post should be open in Facebook Lite.")
        logger.info("Opened via fb:// URI")
        return True

    print(f"[-] Failed to open Facebook Lite. Last error: {out}")
    print("    Try manually: termux-open \"<url>\"")
    logger.error(f"All launch methods failed: {out}")
    return False


def switch_account(account, delay=2.0):
    alias = account.get("alias", f"Account {account['id']}")
    logger.info(f"Opening Facebook Lite for account switch: {alias}")
    print(f"[*] Opening Facebook Lite for: {alias}")

    # Method 1: FB Lite main activity
    ok, out = am_start(
        action="android.intent.action.MAIN",
        component=f"{FB_PKG}/com.facebook.lite.MainActivity"
    )

    if not ok:
        # Method 2: monkey launcher
        ok, out = run(["monkey", "-p", FB_PKG, "-c",
                       "android.intent.category.LAUNCHER", "1"])

    if not ok:
        # Method 3: fallback to full FB
        ok, out = am_start(
            action="android.intent.action.MAIN",
            component=f"{FB_FULL_PKG}/com.facebook.main.MainActivity"
        )

    if ok:
        time.sleep(delay)
        print("[+] Facebook Lite opened.")
        print()
        print("    To switch accounts:")
        print("    1. Tap the Menu (bottom-right)")
        print("    2. Tap your profile name")
        print("    3. Tap 'Switch Account'")
        print(f"    4. Select '{alias}'")
        logger.info(f"Facebook Lite opened for manual switch to: {alias}")
    else:
        print(f"[-] Could not open Facebook Lite. Error: {out}")
        logger.error(f"Failed to open Facebook Lite: {out}")
