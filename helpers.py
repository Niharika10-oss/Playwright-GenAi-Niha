# helpers.py
import time
from playwright.sync_api import Page
from ai_helper import get_healed_locator

def smart_click(page: Page, locator_str: str, timeout_ms: int = 5000):
    """
    Attempts to click a web element normally. 
    If it fails due to a timeout, leverages Gemini to fix it.
    """
    try:
        page.locator(locator_str).click(timeout=timeout_ms)
        print(f"[Success] Successfully clicked element with: '{locator_str}'")
        
    except Exception as original_error:
        print(f"\n[⚠️ Test Alert] Element '{locator_str}' not found within {timeout_ms}ms.")
        print("Initializing AI Self-Healing...")
        
        # Capture the HTML layout context
        html_content = page.content()
        dom_snippet = html_content[:60000] 

        print("Sending broken locator and DOM structure to Gemini...")
        new_locator = get_healed_locator(locator_str, dom_snippet)
        
        if new_locator and new_locator != locator_str:
            print(f"[✨ AI Healed] Gemini suggested a new working locator: '{new_locator}'")
            
            # --- DEFENSIVE GUARD FOR MULTIPLE MATCHES ---
            # If Gemini gives us a simple text locator like 'text=Add To Cart', 
            # we automatically handle strict mode by using the first available match.
            try:
                target_locator = page.locator(new_locator)
                
                # If it's a generic text or class match, target the first instance
                if "text=" in new_locator or new_locator.startswith(".") or new_locator.startswith("button"):
                    target_locator = target_locator.first
                
                target_locator.click(timeout=timeout_ms)
                print(f"[Success] Test recovered seamlessly using healed locator!")
                
            except Exception as retry_error:
                print(f"[Failure] Re-try failed even with healed locator: {retry_error}")
                raise original_error
        else:
            print("[Failure] GenAI could not deduce an alternative selector. Crashing test.")
            raise original_error
