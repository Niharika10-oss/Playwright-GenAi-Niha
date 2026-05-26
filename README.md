# Playwright E2E Test Automation Suite with GenAI Self-Healing 🚀

A robust, enterprise-grade end-to-end test automation suite built using **Python**, **Playwright**, and **pytest**. This repository showcases modern UI automation patterns, including the Page Object Model (POM), custom interaction wrappers, and an innovative **Generative AI Self-Healing mechanism** powered by the official Google GenAI SDK.

---

## 🌟 Key Features

* **Production-Ready E2E Workflows:** Automates complex user journeys including user authentication, dynamic product catalog interactions, cart state validation, and checkout flows.
* **🤖 GenAI Smart Self-Healing Wrapper:** Integrated with the `google-genai` SDK using the ultra-fast `gemini-2.5-flash` model. If a standard Playwright element lookup fails due to frontend DOM shifts or layout updates, the framework automatically catches the exception, extracts the local DOM context, and requests an optimized, functional locator from Gemini in real time.
* **Defensive Strict-Mode Architecture:** Custom helper logic automatically intercepts ambiguous or multi-match selectors returned by the LLM (e.g., repeating e-commerce grid buttons) to ensure flawless test recovery without violating Playwright's strict locator constraints.
* **Headless CI Ready:** Designed for seamless integration with GitHub Actions CI workflows to trigger headless test execution automatically on code pushes.

---

## 🛠️ Tech Stack

* **Core Automation:** Playwright Python
* **Test Runner:** pytest
* **AI Integration:** official `google-genai` SDK (`gemini-2.5-flash`)
* **Language:** Python 3.13+

---

## 📐 Architecture: How the AI Self-Healing Works

When a frontend developer updates an element's class name, ID, or structure, standard automation test suites flake and crash. This project prevents that via a smart fallback orchestration loop:

1. **Execution Fail:** A standard element interaction (`page.locator()`) times out.
2. **Context Extraction:** The execution loop captures the page's current state and extracts the contextual HTML DOM snippet.
3. **LLM Analysis:** The broken selector and DOM snapshot are securely routed to the Gemini API using deterministic configuration parameters (`temperature=0.1`).
4. **Resolution & Defensive Guard:** The script evaluates the AI-suggested locator, applies automated index/hierarchy selectors to bypass multi-element ambiguity, and recovers the test execution dynamically.

---

## 🚀 Getting Started & Local Setup

### 1. Clone the Repository
git clone [https://github.com/Niharika10-oss/Playwright-Tests.git](https://github.com/Niharika10-oss/Playwright-Tests.git)

cd Playwright-Tests
### 2.  Install Dependencies pip install -r requirements.txt
                     # Ensure you have the required engines installed:
                     pip install playwright google-genai pytest
                     playwright install
### 3. Configure Your Environment Variables
Generate an API key for free via Google AI Studio and set it up locally:On Windows (Command Prompt):

set GEMINI_API_KEY=your_actual_api_key_here

On macOS / Linux:

export GEMINI_API_KEY="your_actual_api_key_here"
### 4.Run the Test Automation Suite
Execute the tests with the standard pytest CLI tool. Use the -s flag to see the live AI healing logs directly in your terminal console:
pytest tests/test_e2e.py -s



📊 Sample Execution Log
When an intentional locator failure is triggered to test the self-healing capability, the pipeline prints the following tracking details:
[⚠️ Test Alert] Element 'button[name='Wrong-Add-To-Cart-Button']' not found within 5000ms.
Initializing AI Self-Healing...
Sending broken locator and DOM structure to Gemini...
[✨ AI Healed] Gemini suggested a new working locator: 'text=Add To Cart'
[Success] Test recovered seamlessly using healed locator!

