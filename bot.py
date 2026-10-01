import time
import random
import sys
from playwright.sync_api import sync_playwright

BASE_URL = "https://netlify.app"
TARGET_TASKS_COUNT = 50  # Strictly matches your new MAX_PER_HOUR limit

def run_rewards_bot():
    print(f"[*] Booting 24/7 automated task runner targeting: {BASE_URL}")
    print("[*] Strategy: Targeting raw grid elements inside #taskList directly.")
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                locale="en-US,en;q=0.9",
                timezone_id="Africa/Lagos",
                languages=["en-US", "en"]
            )
            
            # Hide automation markers from site scripts
            context.add_init_script("delete Object.getPrototypeOf(navigator).webdriver;")
            page = context.new_page()

            print(f"[*] Connecting to earning dashboard...")
            page.goto(BASE_URL, wait_until="networkidle", timeout=30000)
            
            # Critical: Wait for your JavaScript buildTasks() loop to draw the rows
            print("[*] Waiting for task list DOM container to initialize...")
            page.wait_for_selector("#taskList", timeout=15000)
            time.sleep(5) # Give the internal engine extra buffer time to fully render the grid elements

            for task_num in range(1, TARGET_TASKS_COUNT + 1):
                print(f"\n[🔄] Task Loop Iteration #{task_num}/{TARGET_TASKS_COUNT}")
                
                try:
                    # Target whatever interactive tags or child element matrices exist inside #taskList
                    # This searches for custom row divs, buttons, or links created inside your script container
                    clickable_tasks = page.locator("#taskList > div, #taskList button, #taskList a").all()

                    if not clickable_tasks:
                        print("[-] Task grid interface state changed. Waiting 4 seconds to sync elements...")
                        time.sleep(4)
                        clickable_tasks = page.locator("#taskList > div, #taskList button, #taskList a").all()

                    if not clickable_tasks:
                        print("[⚠️] Container reporting empty layout. Attempting interface state reload...")
                        page.reload(wait_until="domcontentloaded")
                        page.wait_for_selector("#taskList", timeout=15000)
                        time.sleep(4)
                        continue

                    # Select target node sequentially based on task loop position
                    target_index = (task_num - 1) % len(clickable_tasks)
                    target_btn = clickable_tasks[target_index]
                    
                    print(f"[*] Directing click simulation to row index element: [{target_index}]")
                    
                    # Force a secure dispatch click transaction natively on the item context
                    try:
                        target_btn.click(timeout=4000, force=True)
                    except Exception:
                        pass
                    
                    # Catch and handle accidental frame jumps if the tab tries to rewrite the URL target
                    if page.url != BASE_URL and not page.url.startswith(BASE_URL):
                        print(f"[!] Redirect detected. Bringing browser instance back home...")
                        page.goto(BASE_URL, wait_until="domcontentloaded")
                        page.wait_for_selector("#taskList", timeout=15000)
                        time.sleep(2)

                    # --- ENFORCE MANDATORY 15-SECOND COOLDOWN WINDOW ---
                    # Matches your site's new MIN_GAP_SECONDS limit exactly
                    cooldown_wait = random.randint(16, 17)
                    print(f"[⏱️] Cooldown active. Waiting {cooldown_wait}s for your site's timer...")
                    time.sleep(cooldown_wait)

                except Exception as loop_error:
                    print(f"[!] Anomaly encountered during action step: {loop_error}")
                    time.sleep(2)

            browser.close()
            print("\n[🎉] Complete Success: Automated hourly execution sequence completed.")

        except Exception as critical_error:
            print(f"[❌] Fatal running script exception: {critical_error}")
            sys.exit(0)

if __name__ == "__main__":
    run_rewards_bot()
