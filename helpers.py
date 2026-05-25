# helpers.py
import time
from playwright.sync_api import Page
from ai_helper import get_healed_locator

def smart_click(page: Page, locator_str: str, timeout_ms: int = 5000):
    """
    Attempts to click a web element normally. 
    If it fails due to a timeout (e.g., the UI changed), 
    it automatically passes the page HTML to Gemini to heal the locator and retries.
    """
    try:
        # 1. Try to click using the original selector
        page.locator(locator_str).click(timeout=timeout_ms)
        print(f"[Success] Successfully clicked element with: '{locator_str}'")
        
    except Exception as original_error:
        # 2. If it fails, don't crash yet! Trigger the AI self-healing flow
        print(f"\n[⚠️ Test Alert] Element '{locator_str}' not found within {timeout_ms}ms.")
        print("Initializing AI Self-Healing...")
        
        # 3. Capture the current page's HTML structure
        # We grab the first 50,000 characters to stay within reasonable token sizes
        html_content = page.content()
        dom_snippet = html_content[:50000] 

        # 4. Call our Gemini function to deduce the corrected selector
        print("Sending broken locator and DOM structure to Gemini...")
        new_locator = get_healed_locator(locator_str, dom_snippet)
        
        # 5. Verify if Gemini actually found a new alternative path
        if new_locator and new_locator != locator_str:
            print(f"[✨ AI Healed] Gemini suggested a new working locator: '{new_locator}'")
            try:
                # 6. Retry the critical action with the AI-provided solution
                page.locator(new_locator).click(timeout=timeout_ms)
                print(f"[Success] Test recovered seamlessly using healed locator!")
            except Exception as retry_error:
                print(f"[Failure] Re-try failed even with healed locator: {retry_error}")
                raise original_error
        else:
            print("[Failure] GenAI could not deduce an alternative selector. Crashing test.")
            raise original_error
