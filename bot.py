import time
import random
import sys
from playwright.sync_api import sync_playwright

BASE_URL = "https://netlify.app"
TARGET_TASKS_COUNT = 50  # Matches your MAX_PER_HOUR limit perfectly

def run_rewards_bot():
    print(f"[*] Booting 24/7 automated task runner targeting: {BASE_URL}")
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                locale="en-US,en;q=0.9",
                timezone_id="Africa/Lagos",
                languages=["en-US", "en"]
            )
            
            context.add_init_script("delete Object.getPrototypeOf(navigator).webdriver;")
            page = context.new_page()

            print(f"[*] Connecting to earning dashboard...")
            page.goto(BASE_URL, wait_until="networkidle", timeout=30000)
            page.wait_for_selector("#taskList", timeout=15000)
            time.sleep(3)

            for task_num in range(1, TARGET_TASKS_COUNT + 1):
                print(f"\n[🔄] Task Loop Iteration #{task_num}/{TARGET_TASKS_COUNT}")
                
                try:
                    # Refresh the active DOM components inside the layout panel
                    task_items = page.locator("#taskList button, #taskList a, #taskList div").all()
                    clickable_tasks = [item for item in task_items if item.is_visible()]

                    if not clickable_tasks:
                        print("[-] Task grid refreshing... pausing 3s.")
                        time.sleep(3)
                        continue

                    # Move sequentially through the active items array
                    target_index = (task_num - 1) % len(clickable_tasks)
                    target_btn = clickable_tasks[target_index]
                    
                    print(f"[*] Simulating secure click interactions on index [{target_index}]...")
                    
                    # Prevent the current tab from navigating away by triggering the click event
                    # while forcing the page instance to remain stable on the current URL path.
                    try:
                        target_btn.click(timeout=3000)
                    except Exception:
                        pass
                    
                    # If the click caused a window switch or direct reload, force re-entry home
                    if page.url != BASE_URL and not page.url.startswith(BASE_URL):
                        print(f"[!] Redirect detected to external domain. Resetting position back home...")
                        page.goto(BASE_URL, wait_until="domcontentloaded")
                        page.wait_for_selector("#taskList", timeout=10000)

                    # --- ENFORCE REQURUIED 15-SECOND COOLDOWN WINDOW ---
                    cooldown_wait = random.randint(16, 17)
                    print(f"[⏱️] Cooldown operational. Sleeping {cooldown_wait} seconds to clear limits...")
                    time.sleep(cooldown_wait)

                except Exception as loop_error:
                    print(f"[!] Anomaly encountered during action step: {loop_error}")
                    try:
                        page.goto(BASE_URL, wait_until="domcontentloaded")
                        time.sleep(2)
                    except Exception:
                        pass

            browser.close()
            print("\n[🎉] Complete Success: Automated hourly execution completed.")

        except Exception as critical_error:
            print(f"[❌] Operational runner exception: {critical_error}")
            sys.exit(0)

if __name__ == "__main__":
    run_rewards_bot()
