import time
import random
from playwright.sync_api import sync_playwright

BASE_URL = "https://netlify.app"
TARGET_TASKS_COUNT = 100  # Automatically loop through the 100 available tasks

def run_rewards_bot():
    print(f"[*] Booting automated task bot targeting: {BASE_URL}")
    print("[*] Strategy: Targeting dynamic rows inside #taskList and closing popunders.")
    
    with sync_playwright() as p:
        # Spin up the headless cloud browser instance
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # Open the Netlify web app
        print(f"[*] Navigating to earning hub...")
        page.goto(BASE_URL)
        
        # CRITICAL: Wait for the JavaScript execution to populate the empty '#taskList' div
        print("[*] Waiting for dynamic task list to render elements...")
        page.wait_for_selector("#taskList", timeout=10000)
        time.sleep(2) # Buffer to let the internal layout settle

        for task_num in range(1, TARGET_TASKS_COUNT + 1):
            print(f"\n[🔄] Task Execution #{task_num}/{TARGET_TASKS_COUNT}")
            
            try:
                # 1. Target actionable items specifically inside your dynamic task list container
                # This finds all clickable buttons, links, or rows inside the #taskList container
                task_items = page.locator("#taskList button, #taskList a, #taskList .task-row").all()
                
                # Alternate approach: If the site uses generic clickable tags, pull all inside the list
                if not task_items:
                    task_items = page.locator("#taskList *").all()

                # Filter out elements that are completely empty or unclickable
                clickable_tasks = [item for item in task_items if item.is_visible() and not item.is_disabled()]

                if not clickable_tasks:
                    print("[-] No active task elements ready inside #taskList. Checking again in 3s...")
                    time.sleep(3)
                    continue

                # Target the elements sequentially based on the active available pool loop
                target_index = (task_num - 1) % len(clickable_tasks)
                target_btn = clickable_tasks[target_index]
                
                print(f"[*] Clicking dynamic task item at array index [{target_index}]...")
                
                # 2. Intercept and safely close the popunder window that shoots to the channel page
                try:
                    with context.expect_page(timeout=4000) as popup_info:
                        target_btn.click()
                    
                    # If a new tab/popunder opens, close it in the background immediately
                    popup_page = popup_info.value
                    popup_page.close()
                    print("[+] Intercepted and blocked the popunder channel window successfully.")
                except Exception:
                    # If no new tab opened (handled by regular Javascript triggers), continue smoothly
                    print("[*] Action clicked natively without opening a separate tab window.")

                # 3. Simulate staying right here on the main page while the 10-second site countdown ticks down
                # We stay between 11 to 13 seconds to give the UI script plenty of room to hit 0 and refresh
                countdown_timer = random.choice([11, 12, 13])
                print(f"[⏱️] Waiting {countdown_timer}s for your website's countdown animation to hit 0...")
                time.sleep(countdown_timer)
                
                print("[+] Main site unlocked! Preparing to search for the next task...")

            except Exception as loop_error:
                print(f"[!] Warning: Issue encountered during execution cycle: {loop_error}")
                # Fallback: Hard refresh the Netlify DOM state if buttons lock up or freeze out
                print("[*] Refreshing app to re-sync dashboard states...")
                page.reload()
                page.wait_for_selector("#taskList", timeout=15000)
                time.sleep(2)

        browser.close()
        print("\n[🎉] Complete Success: The automated sequence has finished handling all 100 task queues.")

if __name__ == "__main__":
    run_rewards_bot()
