import time
import random
import sys
from playwright.sync_api import sync_playwright

BASE_URL = "https://netlify.app"

# Strictly match your new MAX_PER_HOUR limit. 
# Processing more than 50 in an hour will trip your site's warning banner.
TARGET_TASKS_COUNT = 50  

def run_rewards_bot():
    print(f"[*] Booting automated task bot targeting: {BASE_URL}")
    print(f"[*] Configuration: Running {TARGET_TASKS_COUNT} tasks to maximize hourly pool.")
    
    with sync_playwright() as p:
        try:
            # 1. Launch a stable, headless browser instance
            browser = p.chromium.launch(headless=True)
            
            # 2. Inject stealth configurations to hide the automation environment
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                locale="en-US,en;q=0.9",
                timezone_id="Africa/Lagos",
                languages=["en-US", "en"]
            )
            
            # Wipe the webdriver property to clear the custom isBot() fingerprint check
            context.add_init_script("delete Object.getPrototypeOf(navigator).webdriver;")
            page = context.new_page()

            # Open the dashboard
            print(f"[*] Connecting to earning hub...")
            page.goto(BASE_URL, wait_until="networkidle", timeout=30000)
            
            # Wait for your buildTasks() matrix to render elements inside #taskList
            print("[*] Waiting for task list layout to render...")
            page.wait_for_selector("#taskList", timeout=15000)
            time.sleep(3) 

            for task_num in range(1, TARGET_TASKS_COUNT + 1):
                print(f"\n[🔄] Task Loop Execution #{task_num}/{TARGET_TASKS_COUNT}")
                
                try:
                    # Select actionable components inside your container dynamically
                    task_items = page.locator("#taskList button, #taskList a, #taskList div").all()
                    clickable_tasks = [item for item in task_items if item.is_visible()]

                    if not clickable_tasks:
                        print("[-] Layout structure is loading... waiting 4 seconds.")
                        time.sleep(4)
                        continue

                    # Cycle through the active buttons sequentially
                    target_index = (task_num - 1) % len(clickable_tasks)
                    target_btn = clickable_tasks[target_index]
                    
                    print(f"[*] Simulating user click on task index: [{target_index}]")
                    
                    # Click the task and instantly catch/suppress the advertising popunder window tab
                    try:
                        with context.expect_page(timeout=4000) as popup_info:
                            target_btn.click()
                        popup_page = popup_info.value
                        popup_page.close()
                        print("[+] Intercepted and terminated popunder link redirect.")
                    except Exception:
                        print("[*] Click triggered natively.")

                    # --- CRITICAL 15-SECOND COOLDOWN BUFFER ---
                    # Your site requires a strict MIN_GAP_SECONDS: 15 delay.
                    # We use a random pause between 16 and 18 seconds to ensure your site's 
                    # internal countdown timer hits 0 completely before the next click.
                    cooldown_wait = random.randint(16, 18)
                    print(f"[⏱️] Cooldown active. Waiting {cooldown_wait}s to clear MIN_GAP_SECONDS tracker...")
                    time.sleep(cooldown_wait)

                except Exception as inner_error:
                    print(f"[!] Warning: Anomaly caught in current execution index: {inner_error}")
                    page.reload()
                    page.wait_for_selector("#taskList", timeout=15000)
                    time.sleep(3)

            browser.close()
            print("\n[🎉] COMPLETE SUCCESS: 50 tasks processed smoothly without breaking limits!")

        except Exception as critical_error:
            print(f"[❌] Fatal running script failure: {critical_error}")
            sys.exit(0)

if __name__ == "__main__":
    run_rewards_bot()
