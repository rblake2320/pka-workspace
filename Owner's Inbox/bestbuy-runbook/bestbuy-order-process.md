# Best Buy — Order Process Book

**Type:** SelfConnect Process Book (reusable, parameterized)
**Site:** bestbuy.com
**Recorded:** 2026-05-17
**Source Trace:** bestbuy-ps5-trace.zip (67 actions, 0 failures)

---

## Parameters (filled by the agent at runtime)

| Parameter | Type | Example | Description |
|-----------|------|---------|-------------|
| `{search_term}` | string | "PlayStation 5 console" | What to search for |
| `{item_index}` | int | 0 | Which result to select (0 = first) |
| `{first_name}` | string | — | Buyer's first name |
| `{last_name}` | string | — | Buyer's last name |
| `{address}` | string | — | Street address |
| `{city}` | string | — | City |
| `{state}` | string | — | 2-letter state code (e.g. "MN") |
| `{zip}` | string | — | 5-digit ZIP |
| `{email}` | string | — | Email address |
| `{phone}` | string | — | 10-digit phone (e.g. "6125551234") |

---

## Process Steps

### Step 1: Navigate to Best Buy

**Action:** Open browser, go to homepage
**URL:** `https://www.bestbuy.com`
**Wait:** 3 seconds (page fully renders, JS loads)
**Verify:** Page title contains "Best Buy" OR search bar is visible

```
SelfConnect: open_browser("https://www.bestbuy.com")
SelfConnect: wait(3000)
SelfConnect: save_capture(hwnd, "step01_homepage.png")
```

---

### Step 2: Search for Item

**Action:** Navigate to search results
**URL:** `https://www.bestbuy.com/site/searchpage.jsp?st={search_term}`
- Replace spaces in `{search_term}` with `+`
**Wait:** 4 seconds (results load, images render)
**Verify:** Results grid is visible, "Add to cart" buttons appear

```
SelfConnect: navigate("https://www.bestbuy.com/site/searchpage.jsp?st=" + urlencode(search_term))
SelfConnect: wait(4000)
SelfConnect: save_capture(hwnd, "step02_search.png")
```

**Why URL-based search:** The search input selector changes with A/B tests and redesigns. The URL search endpoint is stable — same query param `st=` has worked for years.

---

### Step 3: Add Item to Cart

**Action:** Click "Add to cart" button on the desired item
**Selector:** `role=button[name="Add to cart"]` (nth={item_index})
**Wait:** 3 seconds (flyout confirmation appears)
**Verify:** Flyout shows "Added to cart" with green checkmark, "Go to cart" link appears

```
SelfConnect: click_by_role("button", name="Add to cart", index=item_index)
SelfConnect: wait(3000)
SelfConnect: save_capture(hwnd, "step03_added.png")
```

**Flyout structure (confirmed 2026-05-17):**
- Green check icon + "Added to cart" header
- Product protection upsell (ignore)
- Cart subtotal and item count at bottom
- **"Go to cart"** button — this is the next click target

**If button says "Sold Out" or "Coming Soon":** Item is unavailable. Abort or try next result.

---

### Step 4: Go to Cart

**Action:** Click "Go to cart" in the flyout
**Selector:** `text="Go to cart"` (case-insensitive)
**Fallback URL:** `https://www.bestbuy.com/cart`
**Wait:** 3 seconds
**Verify:** Page shows "Your Cart" with item listed, "Checkout" button visible

```
SelfConnect: click_by_text("Go to cart")
# If flyout dismissed or not found:
SelfConnect: navigate("https://www.bestbuy.com/cart")
SelfConnect: wait(3000)
SelfConnect: save_capture(hwnd, "step04_cart.png")
```

**Cart page layout (confirmed 2026-05-17):**
- Left: Item image, name, price, quantity selector, shipping info
- Right: "Order Summary" — Subtotal, Shipping, Tax, Total
- **"Checkout" button** — large, navy blue, right column
- PayPal Checkout below it (ignore)

---

### Step 5: Checkout

**Action:** Click "Checkout" button
**Selector:** `role=button[name="Checkout"]`
**Wait:** 4 seconds (redirects through identity/signin page)
**Redirect path:** `/cart` → `/identity/signin?token=...` → may auto-advance to checkout

```
SelfConnect: click_by_role("button", name="Checkout")
SelfConnect: wait(4000)
SelfConnect: save_capture(hwnd, "step05_checkout.png")
```

---

### Step 6: Continue as Guest

**Action:** Click "Continue as Guest" button on the sign-in page
**Selector:** `role=button[name="Continue as Guest"]`
**Wait:** 3 seconds (loads fulfillment/shipping page)
**Redirect:** → `/checkout/r/fulfillment`
**Verify:** "Getting your order" heading, shipping form visible

```
SelfConnect: click_by_role("button", name="Continue as Guest")
SelfConnect: wait(3000)
SelfConnect: save_capture(hwnd, "step06_guest.png")
```

**If no guest option:** User may need to sign in. This process book covers guest checkout only.

---

### Step 7: Fill Shipping & Contact Information

**Action:** Fill all form fields in order
**Page:** `/checkout/r/fulfillment`
**Form layout:** Two sections — "Shipping Address" and "Contact Information"

#### Shipping Address Fields

| Order | Label | Selector | Type | Value |
|-------|-------|----------|------|-------|
| 1 | First Name | `label="First Name"` | text input | `{first_name}` |
| 2 | Last Name | `label="Last Name"` | text input | `{last_name}` |
| 3 | Address | `label="Address"` | text input | `{address}` |
| 4 | City | `label="City"` | text input | `{city}` |
| 5 | State | `label="State"` | select dropdown | `{state}` |
| 6 | ZIP Code | `label="ZIP Code"` | text input | `{zip}` |

#### Contact Information Fields

| Order | Label | Selector | Type | Value |
|-------|-------|----------|------|-------|
| 7 | Email Address | `label="Email Address"` | email input | `{email}` |
| 8 | Phone Number | `label="Phone Number"` | tel input | `{phone}` |

#### Fill Sequence

```
# Shipping Address
SelfConnect: click_by_label("First Name")
SelfConnect: type_text(first_name)
SelfConnect: click_by_label("Last Name")
SelfConnect: type_text(last_name)
SelfConnect: click_by_label("Address")
SelfConnect: type_text(address)

# IMPORTANT: Address autocomplete dropdown appears after typing
# Wait 1.5s then click outside the dropdown to dismiss it
SelfConnect: wait(1500)
SelfConnect: click_by_text("Shipping")  # click heading to dismiss dropdown

SelfConnect: click_by_label("City")
SelfConnect: type_text(city)
SelfConnect: select_by_label("State", state)
SelfConnect: click_by_label("ZIP Code")
SelfConnect: type_text(zip)

# Contact Information
SelfConnect: click_by_label("Email Address")
SelfConnect: type_text(email)
SelfConnect: click_by_label("Phone Number")
SelfConnect: type_text(phone)

SelfConnect: save_capture(hwnd, "step07_shipping.png")
```

**Known gotchas:**
- Address field triggers autocomplete suggestions — MUST dismiss before filling City/ZIP
- Phone must be exactly 10 digits, no dashes (e.g. "6125551234" not "612-555-1234")
- "Use as billing address" checkbox is pre-checked by default (leave it)
- "Opt-In For Text Updates" checkbox is unchecked by default (leave it)

---

### Step 8: Continue to Payment (STOP POINT)

**Action:** Verify form is complete, screenshot, DO NOT click "Continue to Payment Information"
**Selector:** `role=button[name="Continue to Payment Information"]`
**STOP:** This is the boundary. Clicking submits shipping and loads payment form.

```
SelfConnect: scroll_to_bottom()
SelfConnect: save_capture(hwnd, "step08_ready.png")
# STOP — do not click "Continue to Payment Information" unless authorized
```

**If authorized to proceed to payment:** Click the button, wait 3s, payment form loads with Credit Card / PayPal / Gift Card options. This process book does NOT cover payment entry.

---

## Error Recovery

| Situation | Recovery |
|-----------|----------|
| "Add to cart" button missing | Item sold out — try next search result or different item |
| Flyout doesn't appear after add | Navigate directly to `bestbuy.com/cart` |
| Sign-in page without Guest option | Site may require account — abort guest flow |
| Address autocomplete blocks City/ZIP | Click any heading text to dismiss, then fill City/ZIP |
| Phone validation error | Ensure exactly 10 digits, no punctuation |
| Page timeout or blank | Refresh once, wait 5s. If still blank, restart from Step 1 |
| CAPTCHA or bot detection | Cannot proceed automatically — flag for human |

---

## Selector Stability Notes

These selectors were verified on 2026-05-17. Best Buy uses React with role-based accessibility, so `role=` and `label=` selectors are more stable than CSS class names.

| Selector | Stability | Notes |
|----------|-----------|-------|
| `role=button[name="Add to cart"]` | HIGH | Core commerce action, unlikely to change |
| `text="Go to cart"` | HIGH | Standard e-commerce language |
| `role=button[name="Checkout"]` | HIGH | Core flow |
| `role=button[name="Continue as Guest"]` | MEDIUM | May change wording |
| `label="First Name"` etc. | HIGH | Standard form labels, accessibility-required |
| `role=button[name="Continue to Payment Information"]` | MEDIUM | Full text may change |
| Search URL `?st=` param | HIGH | Stable for years |

---

## Timing Budget

| Step | Wait (ms) | Why |
|------|-----------|-----|
| Homepage load | 3000 | JS bundle, images, dynamic content |
| Search results | 4000 | API call, product cards render |
| After Add to cart | 3000 | Flyout animation + cart API |
| Cart page | 3000 | Cart contents API |
| After Checkout click | 4000 | Identity redirect chain |
| After Guest click | 3000 | Checkout page load |
| After address type | 1500 | Autocomplete API response |
| After all fields filled | 1000 | Validation runs |

**Total process time:** ~25-30 seconds (without slow_mo)

---

## Adaptation Guide

To create a process book for a DIFFERENT retailer (Amazon, Walmart, Target, etc.):

1. **Record once** with Playwright: `python bestbuy_ps5_trace_v4.py` (adapted for the site)
2. **Convert** with `playwright_trace_runbook.py` to get raw selectors
3. **Extract the skeleton**: Same 8-step pattern applies to most e-commerce:
   - Navigate → Search → Select → Add to Cart → Cart → Checkout → Guest/Login → Shipping → Payment
4. **Parameterize**: Replace specific item names and personal data with `{parameters}`
5. **Document selectors**: Record which selectors are role-based (stable) vs class-based (fragile)
6. **Document gotchas**: Every site has quirks (autocomplete, modals, redirects)

The process is the same. Only the selectors and gotchas change per site.
