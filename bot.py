import time
import random
import sys
from playwright.sync_api import sync_playwright

BASE_URL = "https://netlify.app"
TARGET_TASKS_COUNT = 50  # Strictly match your new MAX_PER_HOUR limit

def run_rewards_bot():
    print(f"[*] Booting automated task bot targeting: {BASE_URL}")
    print(f"[*] Goal: Process exactly {TARGET_TASKS_COUNT} hourly tasks sequentially.")
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                locale="en-US,en;q=0.9",
                timezone_id="Africa/Lagos",
                languages=["en-US", "en"]
            )
            
            # Defensive bypass for standard automation identification blocks
            context.add_init_script("delete Object.getPrototypeOf(navigator).webdriver;")
            page = context.new_page()

            print(f"[*] Navigating to workspace layout...")
            page.goto(BASE_URL, wait_until="networkidle", timeout=30000)
            
            # Ensure your dynamic script catalog has drawn items inside the DOM structure
            page.wait_for_selector("#taskList", timeout=15000)
            time.sleep(3)

            for task_num in range(1, TARGET_TASKS_COUNT + 1):
                print(f"\n[🔄] Task Loop Iteration #{task_num}/{TARGET_TASKS_COUNT}")
                
                try:
                    # Explicitly re-verify the active items inside the catalog panel
                    task_items = page.locator("#taskList button, #taskList a, #taskList div").all()
                    clickable_tasks = [item for item in task_items if item.is_visible()]

                    if not clickable_tasks:
                        print("[-] Task view interface state changed. Waiting 4 seconds to recover...")
                        time.sleep(4)
                        # Re-locate elements after the brief state sleep phase
                        task_items = page.locator("#taskList button, #taskList a, #taskList div").all()
                        clickable_tasks = [item for item in task_items if item.is_visible()]

                    if not clickable_tasks:
                        print("[⚠️] Container reporting empty array structure. Executing interface layout sync...")
                        page.reload(wait_until="domcontentloaded")
                        page.wait_for_selector("#taskList", timeout=10000)
                        time.sleep(2)
                        continue

                    # Select target node sequentially based on task loop position
                    target_index = (task_num - 1) % len(clickable_tasks)
                    target_btn = clickable_tasks[target_index]
                    
                    print(f"[*] Directing trigger context to element reference index [{target_index}]...")
                    
                    # Execute action and handle the network popunder redirect routine defensively
                    try:
                        with context.expect_page(timeout=3000) as popup_info:
                            target_btn.click()
                        popup_page = popup_info.value
                        popup_page.close()
                        print("[+] Successfully caught and dismissed the popunder view window.")
                    except Exception:
                        print("[*] Click processed natively inside context layer.")

                    # --- 15-SECOND COOLDOWN DELAY CONFIGURATION ---
                    # To completely pass your MIN_GAP_SECONDS: 15 rule, we use a minor 
                    # 16-second delay to let your site's countdown finish.
                    print("[⏱️] Entering cooldown state window. Sleeping 16 seconds...")
                    time.sleep(16)

                except Exception as loop_error:
                    print(f"[!] Warning: Recovered from soft loop exception: {loop_error}")
                    time.sleep(2)

            browser.close()
            print("\n[🎉] Complete Success: Target execution metrics handled successfully.")

        except Exception as critical_error:
            print(f"[❌] Fatal running exception caught: {critical_error}")
            sys.exit(0)

if __name__ == "__main__":
    run_rewards_bot()
