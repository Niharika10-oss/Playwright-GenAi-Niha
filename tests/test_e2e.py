import sys
import os
is_ci = os.getenv("CI") == "true"

# Dynamically append the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.sync_api import sync_playwright, expect
from helpers import smart_click

def test_error():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=is_ci)
        context = browser.new_context()
        page = context.new_page()
        
        page.goto("https://rahulshettyacademy.com/client")
        # Setting a global timeout
        page.set_default_timeout(30000)

        # Wait for and fill the email
        email_field = page.wait_for_selector("input[placeholder='email@example.com']", timeout=10000)
        email_field.fill("kolarnihar@gmail.com")

        # Wait and fill password
        page.wait_for_selector("#userPassword", timeout=20000)
        page.fill("#userPassword", "NihaK10#")

        # Click login button
        login_button = page.locator('input[name="login"]')
        login_button.wait_for(state='visible', timeout=30000)
        login_button.click(timeout=60000)

        # Execute the cart workflow (Converted to pure synchronous execution)
        add_items_to_cart(page)
        
        browser.close()

def add_items_to_cart(page):
    """Handles adding items and checkout synchronously."""
    
    # 1. Adding ZARA COAT 3
    zaracoat = page.locator("div.card-body:has-text('ZARA COAT 3')")
    zaracoat.wait_for(state='visible', timeout=30000)
    
    # --- DEMO: INTENTIONAL BROKEN LOCATOR FOR AI TESTING ---
    # The real locator is button[name="Add To Cart"] or similar.
    # We pass a wrong one ("button[name='Wrong-Add-To-Cart-Button']") to force smart_click to invoke Gemini!
    smart_click(page, "button[name='Wrong-Add-To-Cart-Button']", timeout_ms=5000)

    # 2. Adding ADIDAS ORIGINAL
    adidas = page.locator("div.card-body:has-text('ADIDAS ORIGINAL')")
    adidas.wait_for(state='visible', timeout=30000)
    
    # Using normal click helper for the second one
    add_to_cart_2 = adidas.locator('button:has-text("Add To Cart")')
    add_to_cart_2.wait_for(state='visible', timeout=30000)
    add_to_cart_2.click(timeout=60000)

    # 3. Check cart items count
    # Let's use smart_click here too just in case the UI changes the cart button properties later!
    smart_click(page, 'button[routerlink*="cart"]') 
    
    # Verify both items exist in the checkout preview
    expect(page.locator("div.cart li")).to_have_count(2)

