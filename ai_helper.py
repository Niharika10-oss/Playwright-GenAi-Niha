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
    system_instruction = (
        "You are an expert QA Automation Engineer specialized in Playwright Python. "
        "Your task is to repair broken element locators. You must analyze the provided HTML "
        "and return ONLY the raw, corrected Playwright locator string (e.g., 'button.submit-btn' "
        "or 'text=Login'). Do not include any explanations, markdown code blocks, backticks, "
        "or introductory text."
    )

    # 3. Formulate the explicit user prompt
    prompt = f"""
    The following Playwright selector failed to find its element: '{broken_locator}'
    
    Here is a snippet of the current page HTML surrounding the intended element area:
    ---
    {html_snippet}
    ---
    
    Analyze the HTML structure. Find the element that most closely matches the intent of the original selector.
    Provide a robust, optimized alternative CSS selector or text selector that Playwright can resolve.
    """

    try:
        # 4. Generate content using the fast, cost-effective gemini-2.5-flash model
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1 # Low temperature ensures highly deterministic, exact answers
            )
        )
        
        # Clean up the output string to ensure no rogue whitespaces or newlines
        healed_locator = response.text.strip()
        return healed_locator

    except Exception as e:
        print(f"[AI-Error] Failed to communicate with Gemini API: {e}")
        return broken_locator
