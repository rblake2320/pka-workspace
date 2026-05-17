#!/usr/bin/env python3
"""
Best Buy PS5 Order Runbook — Playwright Trace Recorder (v4 — single trace)

Same flow as v3 but uses tracing.group() instead of chunks,
so the entire session is captured in one trace.zip file.

IMPORTANT: This script does NOT place any order.
"""
from playwright.sync_api import sync_playwright
import sys
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def wait_and_click(locator, timeout=5000):
    try:
        locator.first.wait_for(state="visible", timeout=timeout)
        locator.first.scroll_into_view_if_needed()
        locator.first.click()
        return True
    except Exception:
        return False


def wait_and_fill(locator, value, timeout=3000):
    try:
        locator.first.wait_for(state="visible", timeout=timeout)
        locator.first.click()
        locator.first.fill(value)
        return True
    except Exception:
        return False


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=600)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
        )
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()

        # ── Step 1: Best Buy Homepage ──
        print("[Step 1] Navigate to bestbuy.com")
        page.goto("https://www.bestbuy.com", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(3000)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "v4_01_homepage.png"))
        print("  DONE")

        # ── Step 2: Search for PS5 ──
        print("[Step 2] Search for PS5")
        page.goto(
            "https://www.bestbuy.com/site/searchpage.jsp?st=playstation+5+console",
            wait_until="domcontentloaded", timeout=30000,
        )
        page.wait_for_timeout(4000)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "v4_02_search.png"))
        print("  DONE")

        # ── Step 3: Add PS5 to cart ──
        print("[Step 3] Add PS5 to cart")
        add_btn = page.get_by_role("button", name="Add to cart")
        count = add_btn.count()
        print(f"  Found {count} 'Add to cart' buttons")
        if wait_and_click(add_btn):
            page.wait_for_timeout(3000)
            print("  DONE")
        else:
            print("  FAIL — no button found")
        page.screenshot(path=os.path.join(OUTPUT_DIR, "v4_03_added.png"))

        # ── Step 4: Go to Cart ──
        print("[Step 4] Go to Cart")
        if not wait_and_click(page.get_by_text("Go to cart"), timeout=5000):
            if not wait_and_click(page.get_by_role("link", name="Go to cart"), timeout=3000):
                page.goto("https://www.bestbuy.com/cart",
                          wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(3000)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "v4_04_cart.png"))
        print(f"  DONE — {page.url}")

        # ── Step 5: Checkout ──
        print("[Step 5] Checkout")
        if not wait_and_click(page.get_by_role("button", name="Checkout"), timeout=5000):
            wait_and_click(page.get_by_role("link", name="Checkout"), timeout=3000)
        page.wait_for_timeout(4000)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "v4_05_checkout.png"))
        print(f"  DONE — {page.url}")

        # ── Step 6: Continue as Guest ──
        print("[Step 6] Continue as Guest")
        for name in ["Continue as Guest", "Continue as guest", "Guest"]:
            if wait_and_click(page.get_by_role("button", name=name), timeout=3000):
                break
        page.wait_for_timeout(3000)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "v4_06_guest.png"))
        print(f"  DONE — {page.url}")

        # ── Step 7: Fill Shipping Info ──
        print("[Step 7] Fill shipping info")
        # Best Buy checkout labels from screenshot: "First Name", "Last Name",
        # "Address", "City", "State", "ZIP Code", "Email Address", "Phone Number"
        fields = [
            ("First Name",    "Test"),
            ("Last Name",     "Buyer"),
            ("Address",       "123 Main Street"),
            ("Email Address", "testbuyer@example.com"),
            ("Phone Number",  "6125551234"),
        ]
        for label, value in fields:
            loc = page.get_by_label(label, exact=False)
            if wait_and_fill(loc, value):
                print(f"    Filled {label}")
            else:
                print(f"    SKIP — {label}")

        # Dismiss address suggestions if they appear
        page.wait_for_timeout(1500)
        try:
            # Click somewhere neutral to dismiss autocomplete dropdown
            page.locator("h2:has-text('Shipping')").first.click()
            page.wait_for_timeout(500)
        except Exception:
            pass

        # Now fill City and ZIP (may have been blocked by autocomplete)
        city_loc = page.get_by_label("City", exact=False)
        if wait_and_fill(city_loc, "Minneapolis"):
            print("    Filled City")
        else:
            print("    SKIP — City")

        zip_loc = page.get_by_label("ZIP Code", exact=False)
        if wait_and_fill(zip_loc, "55401"):
            print("    Filled ZIP Code")
        else:
            # Try alternate label
            zip_loc2 = page.get_by_label("ZIP", exact=False)
            if wait_and_fill(zip_loc2, "55401"):
                print("    Filled ZIP")
            else:
                print("    SKIP — ZIP Code")

        # State dropdown
        try:
            state_loc = page.get_by_label("State", exact=False)
            state_loc.first.wait_for(state="visible", timeout=2000)
            state_loc.first.select_option("MN")
            print("    Selected State: MN")
        except Exception:
            print("    SKIP — State")

        page.wait_for_timeout(1000)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "v4_07_shipping.png"))
        print("  DONE")

        # ── Step 8: Stop at Payment ──
        print("[Step 8] STOP before payment")
        # Scroll to show "Continue to Payment Information" button
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "v4_08_stop.png"))
        print()
        print("=" * 60)
        print("STOP — No payment. No order. Trace complete.")
        print("=" * 60)

        # Save the SINGLE full trace
        context.tracing.stop(path=os.path.join(OUTPUT_DIR, "bestbuy-ps5-trace.zip"))
        print(f"\nTrace saved: bestbuy-ps5-trace.zip")
        page.wait_for_timeout(1000)
        browser.close()


if __name__ == "__main__":
    print("=" * 60)
    print("BEST BUY PS5 — TRACE RECORDER v4 (single trace)")
    print("NO ORDER WILL BE PLACED")
    print("=" * 60)
    try:
        run()
        print("\nSUCCESS — Convert with:")
        print("  python playwright_trace_runbook.py bestbuy-ps5-trace.zip --pdf")
    except Exception as e:
        print(f"\nSTOPPED AT: {e}")
        sys.exit(1)
