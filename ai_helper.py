import os
from google import genai
from google.genai import types

def get_healed_locator(broken_locator: str, html_snippet: str) -> str:
    """
    Sends the broken locator and the current page HTML to Gemini 
    to retrieve an alternative, working Playwright locator.
    """
    # 1. Initialize the official Google GenAI client
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[AI-Warning] GEMINI_API_KEY not set. Skipping self-healing.")
        return broken_locator

    client = genai.Client(api_key=api_key)

    # 2. Design a strict system instruction to prevent conversational filler
    # and explicitly prevent strict mode violation errors.
    system_instruction = (
        "You are an expert QA Automation Engineer specialized in Playwright Python. "
        "Your task is to repair broken element locators. You must analyze the provided HTML "
        "and return ONLY the raw, corrected Playwright locator string. "
        "CRITICAL: To avoid Playwright 'strict mode violation' errors caused by multiple matching elements "
        "(like multiple 'Add to Cart' buttons on a page), ensure your locator is highly specific. "
        "If the element is inside a specific card or product section, include the parent text or container "
        "in your locator (e.g., 'div.card-body:has-text(\"ZARA COAT 3\") >> button' or 'button.btn-add'). "
        "Do not include any explanations, markdown code blocks, backticks, or introductory text."
    )

    # 3. Formulate the explicit user prompt
    prompt = f"""
    The following Playwright selector failed to find its target element: '{broken_locator}'
    
    Here is a snippet of the current page HTML surrounding the intended element area:
    ---
    {html_snippet}
    ---
    
    Task:
    1. Analyze the HTML structure.
    2. Find the exact element that matches the original intent (e.g., clicking a specific item's button).
    3. Provide a highly specific, unique CSS selector, text selector, or chained locator that Playwright can resolve without hitting multi-element ambiguity.
    """

    try:
        # 4. Generate content using the gemini-2.5-flash model
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1  # Low temperature ensures highly deterministic, exact answers
            )
        )
        
        # Clean up the output string to ensure no rogue whitespaces or newlines
        healed_locator = response.text.strip()
        return healed_locator

    except Exception as e:
        print(f"[AI-Error] Failed to communicate with Gemini API: {e}")
        return broken_locator
