"return the 10 items in page"

from playwright.sync_api import sync_playwright
import json

def run():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]

        # Attach to the right tab
        active_page = None
        for pg in context.pages:
            if "provider.nha.gov.in" in pg.url:
                active_page = pg
                break

        if not active_page:
            print("❌ No tab open with provider.nha.gov.in")
            return

        print(f"✅ Connected to tab: {active_page.url}")

        tokens = {}

        def handle_response(response):
            try:
                if "/auth/token/refreshToken" in response.url:
                    print("\n🔁 Refresh token detected")
                    data = response.json()
                    tokens["authorization"] = data.get("authorization")
                    tokens["uauthorization"] = data.get("uauthorization")
                    print("✅ Refreshed Tokens:")
                    print(json.dumps(tokens, indent=2))
            except Exception as e:
                print("⚠️ Token parsing error:", e)

        active_page.on("response", handle_response)

        print("⏳ Waiting for /beneficiary/list POST… Now trigger that action in the tab.")

        try:
            response = context.wait_for_event(
                "response",
                lambda r: (
                    "/pmjay/provider/nproviderdashboard/V3/beneficiary/list" in r.url and r.request.method == "POST"
                ),
                timeout=30000  # 30 seconds
            )

            print("📦 Response received:")
            print(json.dumps(response.json(), indent=2))

        except Exception as e:
            print("❌ Timed out or error waiting for response:", e)

        input("\n🛑 Press Enter to close Playwright connection...")
        browser.close()

if __name__ == "__main__":
    run()
