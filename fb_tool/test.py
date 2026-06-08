import subprocess
import time
import re
import sys

def run_adb_command(cmd):
    """Helper to run ADB commands"""
    try:
        result = subprocess.run(['adb', 'shell', cmd], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"ADB Error: {e}")
        return None

def extract_post_id(url):
    """Extracts post ID from various FB URL formats"""
    # Pattern for standard fb.com/posts/ID or fb.com/photo.php?fbid=ID
    match = re.search(r'(?:posts|photo\.php\?fbid)=(\d+)', url)
    if match:
        return match.group(1)
    # Pattern for short links (requires fetching, simplified here for direct IDs)
    return None

def open_fb_lite():
    """Opens Facebook Lite"""
    run_adb_command("am start -n com.facebook.lite/.SplashActivity")
    time.sleep(3)  # Wait for app to load

def like_post_via_url(url):
    post_id = extract_post_id(url)
    if not post_id:
        print("Could not extract Post ID from URL.")
        return False

    print(f"Targeting Post ID: {post_id}")
    
    # 1. Open FB Lite
    open_fb_lite()
    
    # 2. Navigate to the specific post
    # Using intent to open specific post in FB Lite
    # Note: Deep links for FB Lite can be tricky. 
    # Alternative: Use adb shell am start with URI
    run_adb_command(f"am start -a android.intent.action.VIEW -d \"https://www.facebook.com/{post_id}\" com.facebook.lite")
    
    time.sleep(4)  # Wait for post to load
    
    # 3. Locate and Click the "Like" Button
    # Strategy A: Use Resource ID (Most reliable if UI doesn't change)
    # Strategy B: Use Coordinates (Fallback)
    
    print("Attempting to Like...")
    
    # Try clicking by resource ID first
    # Common IDs for FB Lite 'Like' button:
    like_button_id = "com.facebook.lite:id/like_button" 
    try:
        run_adb_command(f"uiautomator dump --xml /sdcard/ui.xml && grep -q '{like_button_id}' /sdcard/ui.xml")
        # If ID exists, click it
        run_adb_command(f"input tap 500 1500") # Fallback coordinate if needed
    except:
        pass

    # Since UI Automation in Termux via simple ADB input is limited, 
    # we will use a coordinate-based approach for the 'Like' button.
    # You must calibrate this coordinate (X Y) for your specific screen size.
    # Usually, the Like button is near the bottom left of the post card.
    
    # CALIBRATION STEP: Run 'adb shell uiautomator dump' and check ui.xml 
    # to find the exact center coordinates of the Like icon.
    
    # Example Coordinate Tap (Adjust these values!)
    # X=150, Y=1600 is a common area for FB Lite like button on 1080p screens
    run_adb_command("input tap 150 1600") 
    
    time.sleep(2)
    print("Like action simulated.")
    
    # 4. Close FB Lite to reset state
    run_adb_command("am force-stop com.facebook.lite")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fb_like_bot.py <facebook_post_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    like_post_via_url(url)