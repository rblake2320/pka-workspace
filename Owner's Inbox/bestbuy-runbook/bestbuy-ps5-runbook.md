# Playwright Trace Runbook

_Source:_ `C:\Users\techai\AppData\Local\Temp\bestbuy_runbook\bestbuy-ps5-trace.zip`  
_Recorded:_ 2026-05-17T19:43:36+00:00  

## Trace metadata

| Field | Value |
|---|---|
| Browser | chromium  |
| Platform | win32 |
| Playwright version | n/a |
| SDK language | python |
| Viewport | 1920 × 1080 |
| User agent | `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36` |
| Total run duration | 57.41 s |

## Execution summary

- **Functional groups:** 3
- **Actions executed:** 67  (0 failed)
- **Navigations:** 3
- **Network calls:** 1477
- **Console messages:** 1166
- **Errors recorded:** 0

## Contents

1. [Interact on page](#step-1-interact-on-page)
2. [Navigate to https://www.bestbuy.com](#step-2-navigate-to-https-www-bestbuy-com)
3. [Navigate to https://www.bestbuy.com/site/searchpage.jsp?st=playstation+5+console](#step-3-navigate-to-https-www-bestbuy-com-site-searchpage-jsp-st-playstation-5-console)

## Steps

### Step 1: Interact on page

- **Duration:** 189 ms
- **Actions:** 1

| # | Time | Action | Target / Value | Duration | Status |
|---|---|---|---|---|---|
| 1 | 19:43:36.260 | newPage |  | 189 ms | ✓ |

**Narrative**

1. Open a new browser page (tab)

### Step 2: Navigate to https://www.bestbuy.com

- **Duration:** 6.52 s
- **Actions:** 3
- **Page before:** https://www.bestbuy.com

| # | Time | Action | Target / Value | Duration | Status |
|---|---|---|---|---|---|
| 1 | 19:43:36.455 | goto | https://www.bestbuy.com | 2.14 s | ✓ |
| 2 | 19:43:39.405 | waitForTimeout |  | 3.20 s | ✓ |
| 3 | 19:43:42.626 | screenshot |  | 352 ms | ✓ |

**Narrative**

1. Navigate the browser to **https://www.bestbuy.com**
2. Wait **3000 ms**
3. Capture a screenshot of the current page

<details><summary>Action logs</summary>

- `Frame.goto`
  - 2026-05-17T19:43:36.460+00:00 — navigating to "https://www.bestbuy.com/", waiting until "domcontentloaded"
- `Page.screenshot`
  - 2026-05-17T19:43:42.633+00:00 — taking page screenshot
  - 2026-05-17T19:43:42.653+00:00 — waiting for fonts to load...
  - 2026-05-17T19:43:42.659+00:00 — fonts loaded

</details>

### Step 3: Navigate to https://www.bestbuy.com/site/searchpage.jsp?st=playstation+5+console

- **Duration:** 50.66 s
- **Actions:** 63
- **Page before:** https://www.bestbuy.com
- **Page after:** https://www.bestbuy.com/cart

| # | Time | Action | Target / Value | Duration | Status |
|---|---|---|---|---|---|
| 1 | 19:43:43.004 | goto | https://www.bestbuy.com/site/searchpage.jsp?st=playstation+5+console | 2.93 s | ✓ |
| 2 | 19:43:46.627 | waitForTimeout |  | 4.18 s | ✓ |
| 3 | 19:43:50.951 | screenshot |  | 1.64 s | ✓ |
| 4 | 19:43:52.620 | queryCount | `internal:role=button[name="Add to cart"i]` | 44 ms | ✓ |
| 5 | 19:43:52.681 | waitForSelector | `internal:role=button[name="Add to cart"i] >> nth=0` | 218 ms | ✓ |
| 6 | 19:43:52.932 | waitForSelector | `internal:role=button[name="Add to cart"i] >> nth=0` | 64 ms | ✓ |
| 7 | 19:43:53.003 | scrollIntoViewIfNeeded |  | 62 ms | ✓ |
| 8 | 19:43:53.671 | dispose |  | <1 ms | ✓ |
| 9 | 19:43:53.673 | click | `internal:role=button[name="Add to cart"i] >> nth=0` | 413 ms | ✓ |
| 10 | 19:43:54.738 | waitForTimeout |  | 3.02 s | ✓ |
| 11 | 19:43:57.773 | screenshot |  | 372 ms | ✓ |
| 12 | 19:43:58.173 | waitForSelector | `internal:text="Go to cart"i >> nth=0` | 32 ms | ✓ |
| 13 | 19:43:58.223 | waitForSelector | `internal:text="Go to cart"i >> nth=0` | 29 ms | ✓ |
| 14 | 19:43:58.266 | scrollIntoViewIfNeeded |  | 27 ms | ✓ |
| 15 | 19:43:58.916 | dispose |  | <1 ms | ✓ |
| 16 | 19:43:58.918 | click | `internal:text="Go to cart"i >> nth=0` | 1.10 s | ✓ |
| 17 | 19:44:00.754 | waitForTimeout |  | 3.15 s | ✓ |
| 18 | 19:44:03.978 | screenshot |  | 639 ms | ✓ |
| 19 | 19:44:04.627 | waitForSelector | `internal:role=button[name="Checkout"i] >> nth=0` | 24 ms | ✓ |
| 20 | 19:44:04.661 | waitForSelector | `internal:role=button[name="Checkout"i] >> nth=0` | 791 ms | ✓ |
| 21 | 19:44:05.481 | scrollIntoViewIfNeeded |  | 279 ms | ✓ |
| 22 | 19:44:06.759 | dispose |  | 1 ms | ✓ |
| 23 | 19:44:06.762 | click | `internal:role=button[name="Checkout"i] >> nth=0` | 1.36 s | ✓ |
| 24 | 19:44:08.782 | waitForTimeout |  | 4.02 s | ✓ |
| 25 | 19:44:12.812 | screenshot |  | 99 ms | ✓ |
| 26 | 19:44:12.922 | waitForSelector | `internal:role=button[name="Continue as Guest"i] >> nth=0` | 19 ms | ✓ |
| 27 | 19:44:12.947 | waitForSelector | `internal:role=button[name="Continue as Guest"i] >> nth=0` | 10 ms | ✓ |
| 28 | 19:44:12.962 | scrollIntoViewIfNeeded |  | 17 ms | ✓ |
| 29 | 19:44:13.584 | dispose |  | <1 ms | ✓ |
| 30 | 19:44:13.586 | click | `internal:role=button[name="Continue as Guest"i] >> nth=0` | 66 ms | ✓ |
| 31 | 19:44:15.028 | waitForTimeout |  | 3.01 s | ✓ |
| 32 | 19:44:18.071 | screenshot |  | 133 ms | ✓ |
| 33 | 19:44:18.212 | waitForSelector | `internal:label="First Name"i >> nth=0` | 50 ms | ✓ |
| 34 | 19:44:18.272 | click | `internal:label="First Name"i >> nth=0` | 117 ms | ✓ |
| 35 | 19:44:19.022 | fill | `internal:label="First Name"i >> nth=0` ← `Test` | 113 ms | ✓ |
| 36 | 19:44:19.745 | waitForSelector | `internal:label="Last Name"i >> nth=0` | 9 ms | ✓ |
| 37 | 19:44:19.758 | click | `internal:label="Last Name"i >> nth=0` | 92 ms | ✓ |
| 38 | 19:44:20.463 | fill | `internal:label="Last Name"i >> nth=0` ← `Buyer` | 34 ms | ✓ |
| 39 | 19:44:21.115 | waitForSelector | `internal:label="Address"i >> nth=0` | 9 ms | ✓ |
| 40 | 19:44:21.129 | click | `internal:label="Address"i >> nth=0` | 93 ms | ✓ |
| 41 | 19:44:21.833 | fill | `internal:label="Address"i >> nth=0` ← `123 Main Street` | 38 ms | ✓ |
| 42 | 19:44:22.478 | waitForSelector | `internal:label="Email Address"i >> nth=0` | 10 ms | ✓ |
| 43 | 19:44:22.492 | click | `internal:label="Email Address"i >> nth=0` | 106 ms | ✓ |
| 44 | 19:44:23.208 | fill | `internal:label="Email Address"i >> nth=0` ← `testbuyer@example.com` | 36 ms | ✓ |
| 45 | 19:44:23.859 | waitForSelector | `internal:label="Phone Number"i >> nth=0` | 10 ms | ✓ |
| 46 | 19:44:23.873 | click | `internal:label="Phone Number"i >> nth=0` | 55 ms | ✓ |
| 47 | 19:44:24.547 | fill | `internal:label="Phone Number"i >> nth=0` ← `6125551234` | 45 ms | ✓ |
| 48 | 19:44:25.211 | waitForTimeout |  | 1.52 s | ✓ |
| 49 | 19:44:26.739 | click | `h2:has-text('Shipping') >> nth=0` | 67 ms | ✓ |
| 50 | 19:44:27.414 | waitForTimeout |  | 507 ms | ✓ |
| 51 | 19:44:27.926 | waitForSelector | `internal:label="City"i >> nth=0` | 5 ms | ✓ |
| 52 | 19:44:27.934 | click | `internal:label="City"i >> nth=0` | 60 ms | ✓ |
| 53 | 19:44:28.611 | fill | `internal:label="City"i >> nth=0` ← `Minneapolis` | 36 ms | ✓ |
| 54 | 19:44:29.265 | waitForSelector | `internal:label="ZIP Code"i >> nth=0` | 7 ms | ✓ |
| 55 | 19:44:29.276 | click | `internal:label="ZIP Code"i >> nth=0` | 153 ms | ✓ |
| 56 | 19:44:30.039 | fill | `internal:label="ZIP Code"i >> nth=0` ← `55401` | 40 ms | ✓ |
| 57 | 19:44:30.693 | waitForSelector | `internal:label="State"i >> nth=0` | 13 ms | ✓ |
| 58 | 19:44:30.711 | selectOption | `internal:label="State"i >> nth=0` | 33 ms | ✓ |
| 59 | 19:44:31.359 | waitForTimeout |  | 1.02 s | ✓ |
| 60 | 19:44:32.398 | screenshot |  | 129 ms | ✓ |
| 61 | 19:44:32.541 | evaluateExpression | `window.scrollTo(0, document.body.scrollHeight)` | 6 ms | ✓ |
| 62 | 19:44:32.550 | waitForTimeout |  | 1.01 s | ✓ |
| 63 | 19:44:33.568 | screenshot |  | 100 ms | ✓ |

**Narrative**

1. Navigate the browser to **https://www.bestbuy.com/site/searchpage.jsp?st=playstation+5+console**
2. Wait **4000 ms**
3. Capture a screenshot of the current page
4. Frame.queryCount — selector `internal:role=button[name="Add to cart"i]`
5. Wait for **internal:role=button[name="Add to cart"i] >> nth=0** to appear
6. Wait for **internal:role=button[name="Add to cart"i] >> nth=0** to appear
7. ElementHandle.scrollIntoViewIfNeeded
8. ElementHandle.dispose
9. Click on **internal:role=button[name="Add to cart"i] >> nth=0**
10. Wait **3000 ms**
11. Capture a screenshot of the current page
12. Wait for **internal:text="Go to cart"i >> nth=0** to appear
13. Wait for **internal:text="Go to cart"i >> nth=0** to appear
14. ElementHandle.scrollIntoViewIfNeeded
15. ElementHandle.dispose
16. Click on **internal:text="Go to cart"i >> nth=0**
17. Wait **3000 ms**
18. Capture a screenshot of the current page
19. Wait for **internal:role=button[name="Checkout"i] >> nth=0** to appear
20. Wait for **internal:role=button[name="Checkout"i] >> nth=0** to appear
21. ElementHandle.scrollIntoViewIfNeeded
22. ElementHandle.dispose
23. Click on **internal:role=button[name="Checkout"i] >> nth=0**
24. Wait **4000 ms**
25. Capture a screenshot of the current page
26. Wait for **internal:role=button[name="Continue as Guest"i] >> nth=0** to appear
27. Wait for **internal:role=button[name="Continue as Guest"i] >> nth=0** to appear
28. ElementHandle.scrollIntoViewIfNeeded
29. ElementHandle.dispose
30. Click on **internal:role=button[name="Continue as Guest"i] >> nth=0**
31. Wait **3000 ms**
32. Capture a screenshot of the current page
33. Wait for **internal:label="First Name"i >> nth=0** to appear
34. Click on **internal:label="First Name"i >> nth=0**
35. Fill **internal:label="First Name"i >> nth=0** with `Test`
36. Wait for **internal:label="Last Name"i >> nth=0** to appear
37. Click on **internal:label="Last Name"i >> nth=0**
38. Fill **internal:label="Last Name"i >> nth=0** with `Buyer`
39. Wait for **internal:label="Address"i >> nth=0** to appear
40. Click on **internal:label="Address"i >> nth=0**
41. Fill **internal:label="Address"i >> nth=0** with `123 Main Street`
42. Wait for **internal:label="Email Address"i >> nth=0** to appear
43. Click on **internal:label="Email Address"i >> nth=0**
44. Fill **internal:label="Email Address"i >> nth=0** with `testbuyer@example.com`
45. Wait for **internal:label="Phone Number"i >> nth=0** to appear
46. Click on **internal:label="Phone Number"i >> nth=0**
47. Fill **internal:label="Phone Number"i >> nth=0** with `6125551234`
48. Wait **1500 ms**
49. Click on **h2:has-text('Shipping') >> nth=0**
50. Wait **500 ms**
51. Wait for **internal:label="City"i >> nth=0** to appear
52. Click on **internal:label="City"i >> nth=0**
53. Fill **internal:label="City"i >> nth=0** with `Minneapolis`
54. Wait for **internal:label="ZIP Code"i >> nth=0** to appear
55. Click on **internal:label="ZIP Code"i >> nth=0**
56. Fill **internal:label="ZIP Code"i >> nth=0** with `55401`
57. Wait for **internal:label="State"i >> nth=0** to appear
58. Select option `[{"valueOrLabel": "MN"}]` on **internal:label="State"i >> nth=0**
59. Wait **1000 ms**
60. Capture a screenshot of the current page
61. Frame.evaluateExpression — selector `window.scrollTo(0, document.body.scrollHeight)`
62. Wait **1000 ms**
63. Capture a screenshot of the current page

<details><summary>Action logs</summary>

- `Frame.goto`
  - 2026-05-17T19:43:43.016+00:00 — navigating to "https://www.bestbuy.com/site/searchpage.jsp?st=playstation+5+console", waiting until "domcontentloaded"
- `Page.screenshot`
  - 2026-05-17T19:43:51.611+00:00 — taking page screenshot
  - 2026-05-17T19:43:51.761+00:00 — waiting for fonts to load...
  - 2026-05-17T19:43:51.848+00:00 — fonts loaded
- `Frame.waitForSelector`
  - 2026-05-17T19:43:52.751+00:00 — waiting for get_by_role("button", name="Add to cart").first to be visible
  - 2026-05-17T19:43:52.810+00:00 —   locator resolved to visible <button type="button" aria-busy="false" data-brix-version="1.82.0" data-brix-component-name="Button" data-testid="plp-add-to-cart-6646419" class="relative border-xs border-solid rounded-lg justify-center items-center self-start flex flex-col cursor-pointer px-100 py-50 bg-comp-surface-secondary-emphasis border-comp-outline-secondary-muted w-full">…</button>
- `Frame.waitForSelector`
  - 2026-05-17T19:43:52.957+00:00 — waiting for get_by_role("button", name="Add to cart").first
  - 2026-05-17T19:43:52.989+00:00 —   locator resolved to visible <button type="button" aria-busy="false" data-brix-version="1.82.0" data-brix-component-name="Button" data-testid="plp-add-to-cart-6646419" class="relative border-xs border-solid rounded-lg justify-center items-center self-start flex flex-col cursor-pointer px-100 py-50 bg-comp-surface-secondary-emphasis border-comp-outline-secondary-muted w-full">…</button>
- `ElementHandle.scrollIntoViewIfNeeded`
  - 2026-05-17T19:43:53.028+00:00 — attempting scroll into view action
  - 2026-05-17T19:43:53.028+00:00 —   waiting for element to be stable
- `Frame.click`
  - 2026-05-17T19:43:53.690+00:00 — waiting for get_by_role("button", name="Add to cart").first
  - 2026-05-17T19:43:53.730+00:00 —   locator resolved to <button type="button" aria-busy="false" data-brix-version="1.82.0" data-brix-component-name="Button" data-testid="plp-add-to-cart-6646419" class="relative border-xs border-solid rounded-lg justify-center items-center self-start flex flex-col cursor-pointer px-100 py-50 bg-comp-surface-secondary-emphasis border-comp-outline-secondary-muted w-full">…</button>
  - 2026-05-17T19:43:53.745+00:00 — attempting click action
  - 2026-05-17T19:43:53.746+00:00 —   waiting for element to be visible, enabled and stable
  - 2026-05-17T19:43:53.821+00:00 —   element is visible, enabled and stable
  - 2026-05-17T19:43:53.821+00:00 —   scrolling into view if needed
  - 2026-05-17T19:43:53.849+00:00 —   done scrolling
  - 2026-05-17T19:43:53.993+00:00 —   performing click action
  - 2026-05-17T19:43:54.057+00:00 —   click action done
  - 2026-05-17T19:43:54.057+00:00 —   waiting for scheduled navigations to finish
  - 2026-05-17T19:43:54.086+00:00 —   navigations have finished
- `Page.screenshot`
  - 2026-05-17T19:43:58.001+00:00 — taking page screenshot
  - 2026-05-17T19:43:58.011+00:00 — waiting for fonts to load...
  - 2026-05-17T19:43:58.017+00:00 — fonts loaded
- `Frame.waitForSelector`
  - 2026-05-17T19:43:58.186+00:00 — waiting for get_by_text("Go to cart").first to be visible
  - 2026-05-17T19:43:58.200+00:00 —   locator resolved to visible <a href="/cart" tabindex="0" role="button" data-cy="go-to-cart" aria-disabled="false" data-testid="go-to-cart" class="c-button c-button-transparent c-button-md c-button-block c-label-small font-500 fill-comp-outline-primary">…</a>
- `Frame.waitForSelector`
  - 2026-05-17T19:43:58.235+00:00 — waiting for get_by_text("Go to cart").first
  - 2026-05-17T19:43:58.246+00:00 —   locator resolved to visible <a href="/cart" tabindex="0" role="button" data-cy="go-to-cart" aria-disabled="false" data-testid="go-to-cart" class="c-button c-button-transparent c-button-md c-button-block c-label-small font-500 fill-comp-outline-primary">…</a>
- `ElementHandle.scrollIntoViewIfNeeded`
  - 2026-05-17T19:43:58.277+00:00 — attempting scroll into view action
  - 2026-05-17T19:43:58.277+00:00 —   waiting for element to be stable
- `Frame.click`
  - 2026-05-17T19:43:58.927+00:00 — waiting for get_by_text("Go to cart").first
  - 2026-05-17T19:43:58.938+00:00 —   locator resolved to <a href="/cart" tabindex="0" role="button" data-cy="go-to-cart" aria-disabled="false" data-testid="go-to-cart" class="c-button c-button-transparent c-button-md c-button-block c-label-small font-500 fill-comp-outline-primary">…</a>
  - 2026-05-17T19:43:58.939+00:00 — attempting click action
  - 2026-05-17T19:43:58.939+00:00 —   waiting for element to be visible, enabled and stable
  - 2026-05-17T19:43:58.953+00:00 —   element is visible, enabled and stable
  - 2026-05-17T19:43:58.953+00:00 —   scrolling into view if needed
  - 2026-05-17T19:43:58.953+00:00 —   done scrolling
  - 2026-05-17T19:43:58.966+00:00 —   performing click action
  - 2026-05-17T19:43:58.994+00:00 —   click action done
  - 2026-05-17T19:43:58.994+00:00 —   waiting for scheduled navigations to finish
  - 2026-05-17T19:43:59.998+00:00 —   navigated to "https://www.bestbuy.com/cart"
  - 2026-05-17T19:44:00.014+00:00 —   navigations have finished
- `Page.screenshot`
  - 2026-05-17T19:44:04.040+00:00 — taking page screenshot
  - 2026-05-17T19:44:04.119+00:00 — waiting for fonts to load...
  - 2026-05-17T19:44:04.238+00:00 — fonts loaded
- `Frame.waitForSelector`
  - 2026-05-17T19:44:04.632+00:00 — waiting for get_by_role("button", name="Checkout").first to be visible
  - 2026-05-17T19:44:04.648+00:00 —   locator resolved to visible <button type="button" data-track="Checkout - Top" class="btn btn-lg btn-block btn-primary">Checkout</button>
- `Frame.waitForSelector`
  - 2026-05-17T19:44:04.667+00:00 — waiting for get_by_role("button", name="Checkout").first
  - 2026-05-17T19:44:04.906+00:00 —   locator resolved to visible <button type="button" data-track="Checkout - Top" class="btn btn-lg btn-block btn-primary">Checkout</button>
- `ElementHandle.scrollIntoViewIfNeeded`
  - 2026-05-17T19:44:05.501+00:00 — attempting scroll into view action
  - 2026-05-17T19:44:05.502+00:00 —   waiting for element to be stable
- `Frame.click`
  - 2026-05-17T19:44:07.578+00:00 — waiting for get_by_role("button", name="Checkout").first
  - 2026-05-17T19:44:07.890+00:00 —   locator resolved to <button type="button" data-track="Checkout - Top" class="btn btn-lg btn-block btn-primary">Checkout</button>
  - 2026-05-17T19:44:07.902+00:00 — attempting click action
  - 2026-05-17T19:44:07.902+00:00 —   waiting for element to be visible, enabled and stable
  - 2026-05-17T19:44:07.945+00:00 —   element is visible, enabled and stable
  - 2026-05-17T19:44:07.945+00:00 —   scrolling into view if needed
  - 2026-05-17T19:44:07.962+00:00 —   done scrolling
  - 2026-05-17T19:44:08.001+00:00 —   performing click action
  - 2026-05-17T19:44:08.117+00:00 —   click action done
  - 2026-05-17T19:44:08.117+00:00 —   waiting for scheduled navigations to finish
  - 2026-05-17T19:44:08.126+00:00 —   navigations have finished
- `Page.screenshot`
  - 2026-05-17T19:44:12.816+00:00 — taking page screenshot
  - 2026-05-17T19:44:12.821+00:00 — waiting for fonts to load...
  - 2026-05-17T19:44:12.823+00:00 — fonts loaded
- `Frame.waitForSelector`
  - 2026-05-17T19:44:12.926+00:00 — waiting for get_by_role("button", name="Continue as Guest").first to be visible
  - 2026-05-17T19:44:12.939+00:00 —   locator resolved to visible <button type="button" class="c-button c-button-secondary c-button-lg cia-guest-content__continue guest">Continue as Guest</button>
- `Frame.waitForSelector`
  - 2026-05-17T19:44:12.951+00:00 — waiting for get_by_role("button", name="Continue as Guest").first
  - 2026-05-17T19:44:12.955+00:00 —   locator resolved to visible <button type="button" class="c-button c-button-secondary c-button-lg cia-guest-content__continue guest">Continue as Guest</button>
- `ElementHandle.scrollIntoViewIfNeeded`
  - 2026-05-17T19:44:12.965+00:00 — attempting scroll into view action
  - 2026-05-17T19:44:12.965+00:00 —   waiting for element to be stable
- `Frame.click`
  - 2026-05-17T19:44:13.589+00:00 — waiting for get_by_role("button", name="Continue as Guest").first
  - 2026-05-17T19:44:13.592+00:00 —   locator resolved to <button type="button" class="c-button c-button-secondary c-button-lg cia-guest-content__continue guest">Continue as Guest</button>
  - 2026-05-17T19:44:13.593+00:00 — attempting click action
  - 2026-05-17T19:44:13.593+00:00 —   waiting for element to be visible, enabled and stable
  - 2026-05-17T19:44:13.601+00:00 —   element is visible, enabled and stable
  - 2026-05-17T19:44:13.601+00:00 —   scrolling into view if needed
  - 2026-05-17T19:44:13.602+00:00 —   done scrolling
  - 2026-05-17T19:44:13.607+00:00 —   performing click action
  - 2026-05-17T19:44:13.648+00:00 —   click action done
  - 2026-05-17T19:44:13.648+00:00 —   waiting for scheduled navigations to finish
  - 2026-05-17T19:44:13.652+00:00 —   navigations have finished
- `Page.screenshot`
  - 2026-05-17T19:44:18.082+00:00 — taking page screenshot
  - 2026-05-17T19:44:18.095+00:00 — waiting for fonts to load...
  - 2026-05-17T19:44:18.096+00:00 — fonts loaded
- `Frame.waitForSelector`
  - 2026-05-17T19:44:18.216+00:00 — waiting for get_by_label("First Name").first to be visible
  - 2026-05-17T19:44:18.253+00:00 —   locator resolved to visible <input value="" id="firstName" maxlength="50" class="tb-input" name="firstName" data-is-valid="false" autocomplete="given-name"/>
- `Frame.click`
  - 2026-05-17T19:44:18.282+00:00 — waiting for get_by_label("First Name").first
  - 2026-05-17T19:44:18.293+00:00 —   locator resolved to <input value="" id="firstName" maxlength="50" class="tb-input" name="firstName" data-is-valid="false" autocomplete="given-name"/>
  - 2026-05-17T19:44:18.294+00:00 — attempting click action
  - 2026-05-17T19:44:18.294+00:00 —   waiting for element to be visible, enabled and stable
  - 2026-05-17T19:44:18.308+00:00 —   element is visible, enabled and stable
  - 2026-05-17T19:44:18.308+00:00 —   scrolling into view if needed
  - 2026-05-17T19:44:18.310+00:00 —   done scrolling
  - 2026-05-17T19:44:18.325+00:00 —   performing click action
  - 2026-05-17T19:44:18.386+00:00 —   click action done
  - 2026-05-17T19:44:18.386+00:00 —   waiting for scheduled navigations to finish
  - 2026-05-17T19:44:18.389+00:00 —   navigations have finished
- `Frame.fill`
  - 2026-05-17T19:44:19.038+00:00 — waiting for get_by_label("First Name").first
  - 2026-05-17T19:44:19.044+00:00 —   locator resolved to <input value="" id="firstName" maxlength="50" class="tb-input" name="firstName" data-is-valid="false" autocomplete="given-name"/>
  - 2026-05-17T19:44:19.045+00:00 —   fill("Test")
  - 2026-05-17T19:44:19.045+00:00 — attempting fill action
  - 2026-05-17T19:44:19.053+00:00 —   waiting for element to be visible, enabled and editable
- `Frame.waitForSelector`
  - 2026-05-17T19:44:19.749+00:00 — waiting for get_by_label("Last Name").first to be visible
  - 2026-05-17T19:44:19.752+00:00 —   locator resolved to visible <input value="" id="lastName" maxlength="50" name="lastName" class="tb-input" data-is-valid="false" autocomplete="family-name"/>
- `Frame.click`
  - 2026-05-17T19:44:19.760+00:00 — waiting for get_by_label("Last Name").first
  - 2026-05-17T19:44:19.762+00:00 —   locator resolved to <input value="" id="lastName" maxlength="50" name="lastName" class="tb-input" data-is-valid="false" autocomplete="family-name"/>
  - 2026-05-17T19:44:19.763+00:00 — attempting click action
  - 2026-05-17T19:44:19.763+00:00 —   waiting for element to be visible, enabled and stable
  - 2026-05-17T19:44:19.775+00:00 —   element is visible, enabled and stable
  - 2026-05-17T19:44:19.775+00:00 —   scrolling into view if needed
  - 2026-05-17T19:44:19.776+00:00 —   done scrolling
  - 2026-05-17T19:44:19.783+00:00 —   performing click action
  - 2026-05-17T19:44:19.847+00:00 —   click action done
  - 2026-05-17T19:44:19.847+00:00 —   waiting for scheduled navigations to finish
  - 2026-05-17T19:44:19.850+00:00 —   navigations have finished
- `Frame.fill`
  - 2026-05-17T19:44:20.466+00:00 — waiting for get_by_label("Last Name").first
  - 2026-05-17T19:44:20.469+00:00 —   locator resolved to <input value="" id="lastName" maxlength="50" name="lastName" class="tb-input" data-is-valid="false" autocomplete="family-name"/>
  - 2026-05-17T19:44:20.470+00:00 —   fill("Buyer")
  - 2026-05-17T19:44:20.470+00:00 — attempting fill action
  - 2026-05-17T19:44:20.474+00:00 —   waiting for element to be visible, enabled and editable
- `Frame.waitForSelector`
  - 2026-05-17T19:44:21.119+00:00 — waiting for get_by_label("Address").first to be visible
  - 2026-05-17T19:44:21.122+00:00 —   locator resolved to visible <input value="" id="street" name="street" maxlength="35" role="combobox" autocomplete="off" data-is-valid="false" aria-expanded="false" aria-autocomplete="list" aria-activedescendant="" aria-owns="suggestionsMenuId" aria-controls="suggestionsMenuId" class="tb-input  autocomplete__input"/>
- `Frame.click`
  - 2026-05-17T19:44:21.133+00:00 — waiting for get_by_label("Address").first
  - 2026-05-17T19:44:21.136+00:00 —   locator resolved to <input value="" id="street" name="street" maxlength="35" role="combobox" autocomplete="off" data-is-valid="false" aria-expanded="false" aria-autocomplete="list" aria-activedescendant="" aria-owns="suggestionsMenuId" aria-controls="suggestionsMenuId" class="tb-input  autocomplete__input"/>
  - 2026-05-17T19:44:21.137+00:00 — attempting click action
  - 2026-05-17T19:44:21.137+00:00 —   waiting for element to be visible, enabled and stable
  - 2026-05-17T19:44:21.144+00:00 —   element is visible, enabled and stable
  - 2026-05-17T19:44:21.144+00:00 —   scrolling into view if needed
  - 2026-05-17T19:44:21.145+00:00 —   done scrolling
  - 2026-05-17T19:44:21.151+00:00 —   performing click action
  - 2026-05-17T19:44:21.220+00:00 —   click action done
  - 2026-05-17T19:44:21.220+00:00 —   waiting for scheduled navigations to finish
  - 2026-05-17T19:44:21.221+00:00 —   navigations have finished
- `Frame.fill`
  - 2026-05-17T19:44:21.838+00:00 — waiting for get_by_label("Address").first
  - 2026-05-17T19:44:21.841+00:00 —   locator resolved to <input value="" id="street" name="street" maxlength="35" role="combobox" autocomplete="off" data-is-valid="false" aria-expanded="false" aria-autocomplete="list" aria-activedescendant="" aria-owns="suggestionsMenuId" aria-controls="suggestionsMenuId" class="tb-input  autocomplete__input"/>
  - 2026-05-17T19:44:21.841+00:00 —   fill("123 Main Street")
  - 2026-05-17T19:44:21.841+00:00 — attempting fill action
  - 2026-05-17T19:44:21.845+00:00 —   waiting for element to be visible, enabled and editable
- `Frame.waitForSelector`
  - 2026-05-17T19:44:22.482+00:00 — waiting for get_by_label("Email Address").first to be visible
  - 2026-05-17T19:44:22.485+00:00 —   locator resolved to visible <input value="" required="" class="tb-input" name="emailAddress" autocomplete="email" id="user.emailAddress"/>
- `Frame.click`
  - 2026-05-17T19:44:22.495+00:00 — waiting for get_by_label("Email Address").first
  - 2026-05-17T19:44:22.498+00:00 —   locator resolved to <input value="" required="" class="tb-input" name="emailAddress" autocomplete="email" id="user.emailAddress"/>
  - 2026-05-17T19:44:22.498+00:00 — attempting click action
  - 2026-05-17T19:44:22.498+00:00 —   waiting for element to be visible, enabled and stable
  - 2026-05-17T19:44:22.529+00:00 —   element is visible, enabled and stable
  - 2026-05-17T19:44:22.529+00:00 —   scrolling into view if needed
  - 2026-05-17T19:44:22.531+00:00 —   done scrolling
  - 2026-05-17T19:44:22.541+00:00 —   performing click action
  - 2026-05-17T19:44:22.596+00:00 —   click action done
  - 2026-05-17T19:44:22.596+00:00 —   waiting for scheduled navigations to finish
  - 2026-05-17T19:44:22.598+00:00 —   navigations have finished
- `Frame.fill`
  - 2026-05-17T19:44:23.211+00:00 — waiting for get_by_label("Email Address").first
  - 2026-05-17T19:44:23.213+00:00 —   locator resolved to <input value="" required="" class="tb-input" name="emailAddress" autocomplete="email" id="user.emailAddress"/>
  - 2026-05-17T19:44:23.214+00:00 —   fill("testbuyer@example.com")
  - 2026-05-17T19:44:23.214+00:00 — attempting fill action
  - 2026-05-17T19:44:23.218+00:00 —   waiting for element to be visible, enabled and editable
- `Frame.waitForSelector`
  - 2026-05-17T19:44:23.863+00:00 — waiting for get_by_label("Phone Number").first to be visible
  - 2026-05-17T19:44:23.866+00:00 —   locator resolved to visible <input value="" type="tel" required="" name="phone" maxlength="12" id="user.phone" class="tb-input" autocomplete="tel"/>
- `Frame.click`
  - 2026-05-17T19:44:23.876+00:00 — waiting for get_by_label("Phone Number").first
  - 2026-05-17T19:44:23.878+00:00 —   locator resolved to <input value="" type="tel" required="" name="phone" maxlength="12" id="user.phone" class="tb-input" autocomplete="tel"/>
  - 2026-05-17T19:44:23.879+00:00 — attempting click action
  - 2026-05-17T19:44:23.879+00:00 —   waiting for element to be visible, enabled and stable
  - 2026-05-17T19:44:23.889+00:00 —   element is visible, enabled and stable
  - 2026-05-17T19:44:23.889+00:00 —   scrolling into view if needed
  - 2026-05-17T19:44:23.889+00:00 —   done scrolling
  - 2026-05-17T19:44:23.895+00:00 —   performing click action
  - 2026-05-17T19:44:23.928+00:00 —   click action done
  - 2026-05-17T19:44:23.928+00:00 —   waiting for scheduled navigations to finish
  - 2026-05-17T19:44:23.928+00:00 —   navigations have finished
- `Frame.fill`
  - 2026-05-17T19:44:24.552+00:00 — waiting for get_by_label("Phone Number").first
  - 2026-05-17T19:44:24.554+00:00 —   locator resolved to <input value="" type="tel" required="" name="phone" maxlength="12" id="user.phone" class="tb-input" autocomplete="tel"/>
  - 2026-05-17T19:44:24.555+00:00 —   fill("6125551234")
  - 2026-05-17T19:44:24.555+00:00 — attempting fill action
  - 2026-05-17T19:44:24.558+00:00 —   waiting for element to be visible, enabled and editable
- `Frame.click`
  - 2026-05-17T19:44:26.747+00:00 — waiting for locator("h2:has-text('Shipping')").first
  - 2026-05-17T19:44:26.752+00:00 —   locator resolved to <h2 tabindex="-1" class="heading-5 location-group-title" id="location-card-heading-shipping-4tjstbt1675kh-4c2zlzvnxyr3r">Shipping Details</h2>
  - 2026-05-17T19:44:26.752+00:00 — attempting click action
  - 2026-05-17T19:44:26.752+00:00 —   waiting for element to be visible, enabled and stable
  - 2026-05-17T19:44:26.762+00:00 —   element is visible, enabled and stable
  - 2026-05-17T19:44:26.762+00:00 —   scrolling into view if needed
  - 2026-05-17T19:44:26.763+00:00 —   done scrolling
  - 2026-05-17T19:44:26.770+00:00 —   performing click action
  - 2026-05-17T19:44:26.805+00:00 —   click action done
  - 2026-05-17T19:44:26.805+00:00 —   waiting for scheduled navigations to finish
  - 2026-05-17T19:44:26.806+00:00 —   navigations have finished
- `Frame.waitForSelector`
  - 2026-05-17T19:44:27.927+00:00 — waiting for get_by_label("City").first to be visible
  - 2026-05-17T19:44:27.929+00:00 —   locator resolved to visible <input value="" id="city" name="city" maxlength="30" class="tb-input" data-is-valid="false" autocomplete="address-level2"/>
- `Frame.click`
  - 2026-05-17T19:44:27.937+00:00 — waiting for get_by_label("City").first
  - 2026-05-17T19:44:27.939+00:00 —   locator resolved to <input value="" id="city" name="city" maxlength="30" class="tb-input" data-is-valid="false" autocomplete="address-level2"/>
  - 2026-05-17T19:44:27.939+00:00 — attempting click action
  - 2026-05-17T19:44:27.939+00:00 —   waiting for element to be visible, enabled and stable
  - 2026-05-17T19:44:27.948+00:00 —   element is visible, enabled and stable
  - 2026-05-17T19:44:27.948+00:00 —   scrolling into view if needed
  - 2026-05-17T19:44:27.948+00:00 —   done scrolling
  - 2026-05-17T19:44:27.956+00:00 —   performing click action
  - 2026-05-17T19:44:27.993+00:00 —   click action done
  - 2026-05-17T19:44:27.993+00:00 —   waiting for scheduled navigations to finish
  - 2026-05-17T19:44:27.994+00:00 —   navigations have finished
- `Frame.fill`
  - 2026-05-17T19:44:28.613+00:00 — waiting for get_by_label("City").first
  - 2026-05-17T19:44:28.615+00:00 —   locator resolved to <input value="" id="city" name="city" maxlength="30" class="tb-input" data-is-valid="false" autocomplete="address-level2"/>
  - 2026-05-17T19:44:28.616+00:00 —   fill("Minneapolis")
  - 2026-05-17T19:44:28.616+00:00 — attempting fill action
  - 2026-05-17T19:44:28.620+00:00 —   waiting for element to be visible, enabled and editable
- `Frame.waitForSelector`
  - 2026-05-17T19:44:29.268+00:00 — waiting for get_by_label("ZIP Code").first to be visible
  - 2026-05-17T19:44:29.270+00:00 —   locator resolved to visible <input value="" type="tel" id="zipcode" maxlength="5" name="zipcode" class="tb-input" data-is-valid="false" autocomplete="postal-code"/>
- `Frame.click`
  - 2026-05-17T19:44:29.278+00:00 — waiting for get_by_label("ZIP Code").first
  - 2026-05-17T19:44:29.280+00:00 —   locator resolved to <input value="" type="tel" id="zipcode" maxlength="5" name="zipcode" class="tb-input" data-is-valid="false" autocomplete="postal-code"/>
  - 2026-05-17T19:44:29.281+00:00 — attempting click action
  - 2026-05-17T19:44:29.281+00:00 —   waiting for element to be visible, enabled and stable
  - 2026-05-17T19:44:29.295+00:00 —   element is visible, enabled and stable
  - 2026-05-17T19:44:29.295+00:00 —   scrolling into view if needed
  - 2026-05-17T19:44:29.297+00:00 —   done scrolling
  - 2026-05-17T19:44:29.311+00:00 —   performing click action
  - 2026-05-17T19:44:29.428+00:00 —   click action done
  - 2026-05-17T19:44:29.428+00:00 —   waiting for scheduled navigations to finish
  - 2026-05-17T19:44:29.428+00:00 —   navigations have finished
- `Frame.fill`
  - 2026-05-17T19:44:30.043+00:00 — waiting for get_by_label("ZIP Code").first
  - 2026-05-17T19:44:30.047+00:00 —   locator resolved to <input value="" type="tel" id="zipcode" maxlength="5" name="zipcode" class="tb-input" data-is-valid="false" autocomplete="postal-code"/>
  - 2026-05-17T19:44:30.048+00:00 —   fill("55401")
  - 2026-05-17T19:44:30.048+00:00 — attempting fill action
  - 2026-05-17T19:44:30.052+00:00 —   waiting for element to be visible, enabled and editable
- `Frame.waitForSelector`
  - 2026-05-17T19:44:30.696+00:00 — waiting for get_by_label("State").first to be visible
  - 2026-05-17T19:44:30.704+00:00 —   locator resolved to visible <select id="state" name="state" class="tb-select" autocomplete="off" data-is-valid="false">…</select>
- `Frame.selectOption`
  - 2026-05-17T19:44:30.713+00:00 — waiting for get_by_label("State").first
  - 2026-05-17T19:44:30.716+00:00 —   locator resolved to <select id="state" name="state" class="tb-select" autocomplete="off" data-is-valid="false">…</select>
  - 2026-05-17T19:44:30.717+00:00 — attempting select option action
  - 2026-05-17T19:44:30.720+00:00 —   waiting for element to be visible and enabled
  - 2026-05-17T19:44:30.743+00:00 —   selected specified option(s)
- `Page.screenshot`
  - 2026-05-17T19:44:32.418+00:00 — taking page screenshot
  - 2026-05-17T19:44:32.429+00:00 — waiting for fonts to load...
  - 2026-05-17T19:44:32.432+00:00 — fonts loaded
- `Page.screenshot`
  - 2026-05-17T19:44:33.572+00:00 — taking page screenshot
  - 2026-05-17T19:44:33.575+00:00 — waiting for fonts to load...
  - 2026-05-17T19:44:33.578+00:00 — fonts loaded

</details>

## Navigation timeline

| Time | Page | Event | URL |
|---|---|---|---|
| 19:43:36.449 | — | new-page | (new page) |
| 19:43:38.591 | page@c5a712525244ddbb96935726031a7339 | navigation | https://www.bestbuy.com |
| 19:43:45.937 | page@c5a712525244ddbb96935726031a7339 | navigation | https://www.bestbuy.com/site/searchpage.jsp?st=playstation+5+console |
| 19:43:59.998 | page@c5a712525244ddbb96935726031a7339 | navigation | https://www.bestbuy.com/cart |

## Network appendix

| Time | Method | URL | Status | Type | Duration |
|---|---|---|---|---|---|
| 19:43:36.469 | GET | https://www.bestbuy.com/ | 200 | — | 1.27 s |
| 19:43:37.564 | GET | https://pisces.bbystatic.com/image2/BestBuy_US/dam/5770989-ghp2-appls-mds-e461e84b-5ee5-4… | 200 | — | 314 ms |
| 19:43:37.565 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/css/25201a07a0b87c… | 200 | — | 107 ms |
| 19:43:37.565 | GET | https://pisces.bbystatic.com/image2/BestBuy_US/dam/ghp4-ref5694572-bose_der-3f446736-a48c… | 200 | — | 298 ms |
| 19:43:37.566 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/css/f81cd44ffaa432… | 200 | — | 270 ms |
| 19:43:37.566 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/css/7985fddaf38c84… | 200 | — | 269 ms |
| 19:43:37.567 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/css/0b38a8ba3ed923… | 200 | — | 111 ms |
| 19:43:37.567 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/css/8f099566d01898… | 200 | — | 143 ms |
| 19:43:37.567 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/css/aab2e41613d889… | 200 | — | 285 ms |
| 19:43:37.568 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/css/b1de9aa06d285e… | 200 | — | 153 ms |
| 19:43:37.568 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/css/ff3771c172f5bc… | 200 | — | 154 ms |
| 19:43:37.568 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/css/5957a085267896… | 200 | — | 155 ms |
| 19:43:37.568 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/css/b64909cbf44e84… | 200 | — | 161 ms |
| 19:43:37.568 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/css/8d7aadbcf62d03… | 200 | — | 284 ms |
| 19:43:37.568 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/webpack-923… | 200 | — | 468 ms |
| 19:43:37.568 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/1528-17b96b… | 200 | — | 475 ms |
| 19:43:37.568 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/main-app-ce… | 200 | — | 473 ms |
| 19:43:37.568 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/1dd3208c-8e… | 200 | — | 475 ms |
| 19:43:37.569 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/bb7f45ac-fc… | 200 | — | 474 ms |
| 19:43:37.569 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/8bb4d8db-a5… | 200 | — | 475 ms |
| 19:43:37.569 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/7bf36345-4f… | 200 | — | 476 ms |
| 19:43:37.569 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/1052-a91342… | 200 | — | 476 ms |
| 19:43:37.569 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/96c7d161-45… | 200 | — | 475 ms |
| 19:43:37.569 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/8076c734-ba… | 200 | — | 478 ms |
| 19:43:37.569 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/47dcceb7-ca… | 200 | — | 477 ms |
| 19:43:37.569 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/84f9ef10-4b… | 200 | — | 590 ms |
| 19:43:37.570 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/523-2910780… | 200 | — | 600 ms |
| 19:43:37.570 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/app/layout-… | 200 | — | 607 ms |
| 19:43:37.570 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/4dc235f5-58… | 200 | — | 620 ms |
| 19:43:37.570 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/15809608-b8… | 200 | — | 620 ms |
| 19:43:37.570 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/bdca1010-ff… | 200 | — | 620 ms |
| 19:43:37.570 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/990a3170-5c… | 200 | — | 619 ms |
| 19:43:37.570 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/eb2fce1c-a6… | 200 | — | 624 ms |
| 19:43:37.570 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/55c739f6-c1… | 200 | — | 623 ms |
| 19:43:37.570 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/3247-7017b3… | 200 | — | 625 ms |
| 19:43:37.570 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/2580-a33a2e… | 200 | — | 623 ms |
| 19:43:37.570 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/8019-126b6e… | 200 | — | 627 ms |
| 19:43:37.570 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/5139-0ea9da… | 200 | — | 627 ms |
| 19:43:37.570 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/15f9c5db-da… | 200 | — | 624 ms |
| 19:43:37.570 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/8409-7879f9… | 200 | — | 628 ms |
| 19:43:37.570 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/8455-71bbcb… | 200 | — | 625 ms |
| 19:43:37.570 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/50f238d9-09… | 200 | — | 628 ms |
| 19:43:37.570 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/74197371-7b… | 200 | — | 624 ms |
| 19:43:37.570 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/820-7932892… | 200 | — | 657 ms |
| 19:43:37.570 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/4420-527959… | 200 | — | 648 ms |
| 19:43:37.571 | GET | https://www.google.com/recaptcha/enterprise.js?render=6LeP0dgrAAAAAFn_1X2rBkI8vJKKsU0-LOJ… | 200 | — | 161 ms |
| 19:43:37.571 | GET | https://www.bestbuy.com/~assets/bby/_com/deo-client-script.js | 200 | — | 173 ms |
| 19:43:37.571 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/fonts/164de2c41958… | 200 | — | 287 ms |
| 19:43:37.571 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/app/page-66… | 200 | — | 663 ms |
| 19:43:37.571 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/app/error-0… | 200 | — | 664 ms |
| 19:43:37.571 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/app/not-fou… | 200 | — | 664 ms |
| 19:43:37.571 | GET | https://www.bestbuy.com/~assets/bby/_com/@ds/unified-chat/dist/javascript/unified-chat-in… | 200 | — | 663 ms |
| 19:43:37.571 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/9230-1fc8f9… | 200 | — | 677 ms |
| 19:43:37.572 | GET | https://www.bestbuy.com/~assets/bby/_com/gvp/lib-config-service/2.3.3/dist/main.js | 200 | — | 108 ms |
| 19:43:37.572 | GET | https://nexus.ensighten.com/bestbuy/privacy_init/Bootstrap.js | 200 | — | 157 ms |
| 19:43:37.572 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/fonts/ff935616cc06… | 200 | — | 192 ms |
| 19:43:37.572 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/fonts/983f6f02206e… | 200 | — | 214 ms |
| 19:43:37.572 | GET | https://www.bestbuy.com/~assets/bby/_com/deo-lss-activation.js | 200 | — | 261 ms |
| 19:43:37.572 | GET | https://www.bestbuy.com/~assets/bby/_com/libs/goteam/v26.16.2.js | 200 | — | 260 ms |
| 19:43:37.572 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/fonts/e034ae9741bc… | 200 | — | 299 ms |
| 19:43:37.572 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/fonts/563588ea1956… | 200 | — | 301 ms |
| 19:43:37.572 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/fonts/dfda316ca723… | 200 | — | 309 ms |
| 19:43:37.572 | GET | https://www.bestbuy.com/~assets/bby/_js/ext/bbydyn/dyn_digital_homepage.js | 200 | — | 673 ms |
| 19:43:37.572 | GET | https://www.bestbuy.com/akam/13/270d3632 | 200 | — | 674 ms |
| 19:43:37.624 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/lib-mf-assets/2.1.2/dist/main.js | 200 | — | 272 ms |
| 19:43:37.624 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/platformContainerOrchestrationProxy.1… | 200 | — | 614 ms |
| 19:43:37.624 | GET | https://www.bestbuy.com/lux.js | 200 | — | 615 ms |
| 19:43:37.625 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/lib-eventmanager/3.1.0/dist/event-manager.js | 200 | — | 615 ms |
| 19:43:37.625 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-q/6.0.4/dist/analyticsQ.bundle.js | 200 | — | 615 ms |
| 19:43:37.625 | GET | https://www.bestbuy.com/~assets/bby/_com/setup-event-manager.8.9.11.js | 200 | — | 616 ms |
| 19:43:37.625 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/@bestbuy/bby-debug/dist/client/auto-loader-… | 200 | — | 616 ms |
| 19:43:37.625 | GET | https://www.bestbuy.com/~assets/bby/_com/brix/7.11.35/js/brixRemoteEntry.js | 200 | — | 616 ms |
| 19:43:37.625 | GET | https://www.bestbuy.com/~assets/bby/_com/@ds/unified-chat/dist/javascript/unified-chat-in… | 200 | — | 617 ms |
| 19:43:37.663 | GET | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 200 | — | 275 ms |
| 19:43:37.663 | GET | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/kDGYzLOQ/d2YKXBFXew4/TD/gwXSZsbmQt?v… | 200 | — | 585 ms |
| 19:43:37.925 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:37.936 | GET | https://nexus.ensighten.com/bestbuy/privacy_prod/Bootstrap.js | 200 | — | 75 ms |
| 19:43:38.102 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 321 ms |
| 19:43:38.132 | GET | https://t.nc0.co/pc/bestbuy/privacy?publishPath=privacy_prod&ensDisableTracking=user&form… | 200 | — | 345 ms |
| 19:43:38.458 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/6884-8473bcd8b57cc8b1d5c… | 200 | — | 148 ms |
| 19:43:38.458 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/2286-f4563db0fdf951734eb… | 200 | — | 147 ms |
| 19:43:38.459 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/2378-ebef7a4d3d8251107ee… | 200 | — | 148 ms |
| 19:43:38.459 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/2163-ab6cfceaf386ebcfe52… | 200 | — | 151 ms |
| 19:43:38.538 | GET | https://www.bestbuy.com/~assets/bby/_com/@ds/unified-chat/dist/javascript/unified-chat-in… | 200 | — | 94 ms |
| 19:43:38.539 | GET | https://www.bestbuy.com/~assets/bby/_com/@ds/unified-chat/dist/javascript/unified-chat-in… | 200 | — | 82 ms |
| 19:43:38.539 | GET | https://www.bestbuy.com/~assets/bby/_com/@ds/unified-chat/dist/javascript/unified-chat-in… | 200 | — | 95 ms |
| 19:43:38.539 | GET | https://www.bestbuy.com/~assets/bby/_com/@ds/unified-chat/dist/javascript/unified-chat-in… | 200 | — | 95 ms |
| 19:43:38.589 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=0&c=2493&i=68voct&p=privacy_prod&… | 204 | — | 240 ms |
| 19:43:38.625 | GET | https://www.bestbuy.com/~assets/bby/_com/@ds/unified-chat/dist/javascript/unified-chat-in… | 200 | — | 119 ms |
| 19:43:38.935 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/1766.93e807… | 200 | — | 139 ms |
| 19:43:39.014 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/@bestbuy/bby-debug/dist/client/bby-debug-fe… | 200 | — | 147 ms |
| 19:43:39.380 | POST | https://www.bestbuy.com/akam/13/pixel_270d3632 | 200 | — | 146 ms |
| 19:43:39.413 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:39.421 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/interaction-01d33e2b062b… | 200 | — | 168 ms |
| 19:43:39.422 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/5581-e096874da8baa32a486… | 200 | — | 169 ms |
| 19:43:39.422 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/7164-e790f7049f5c9398b5b… | 200 | — | 174 ms |
| 19:43:39.422 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/customer-journal-8ff849b… | 200 | — | 175 ms |
| 19:43:39.440 | GET | https://www.bestbuy.com/services/conversation/web/api/v2/unified-chat/configuration | 200 | — | 281 ms |
| 19:43:39.549 | GET | https://www.bestbuy.com/services/conversation/web/api/v2/unified-chat/configuration | 200 | — | 172 ms |
| 19:43:39.580 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/@bestbuy/bby-debug/dist/client/bby-debug-85… | 200 | — | 104 ms |
| 19:43:39.640 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/cj-digital-schema1-2faec… | 200 | — | 85 ms |
| 19:43:39.647 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/css/0798139c037041… | 200 | — | 107 ms |
| 19:43:39.647 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/css/970b0624cd5955… | 200 | — | 107 ms |
| 19:43:39.647 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/557ea5cb.d3… | 200 | — | 107 ms |
| 19:43:39.647 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/f2b77ed6.d4… | 200 | — | 130 ms |
| 19:43:39.647 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/ea05c48a.b9… | 200 | — | 130 ms |
| 19:43:39.647 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/2f9fc831.a0… | 200 | — | 130 ms |
| 19:43:39.647 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/9920.6ce91b… | 200 | — | 179 ms |
| 19:43:39.648 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/1072.8ba950… | 200 | — | 162 ms |
| 19:43:39.648 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/8236.57805e… | 200 | — | 162 ms |
| 19:43:39.648 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/4718.b3fe60… | 200 | — | 174 ms |
| 19:43:39.648 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/9818.968956… | 200 | — | 180 ms |
| 19:43:39.670 | GET | blob:https://www.bestbuy.com/385d6137-c1a8-4220-9de8-152bc5935a40 | -1 | — | <1 ms |
| 19:43:39.672 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:39.704 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 287 ms |
| 19:43:39.914 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/6654-99d231c40e8f6bb6430… | 200 | — | 95 ms |
| 19:43:39.914 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/2616-4d93e48dc493d12beaf… | 200 | — | 101 ms |
| 19:43:39.914 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/4913-c8e91779834f0890658… | 200 | — | 100 ms |
| 19:43:39.914 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/gtagConversion-5ce7d21df… | 200 | — | 97 ms |
| 19:43:39.914 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/1384-821307b85d1b86f13a2… | 200 | — | 100 ms |
| 19:43:39.914 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/adobeInit-651b3bd355e6e2… | 200 | — | 103 ms |
| 19:43:39.914 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/6133-e679f02537ff34e13b2… | 200 | — | 131 ms |
| 19:43:39.914 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/5874-4c0bbc15c0a4c11f7c1… | 200 | — | 131 ms |
| 19:43:40.363 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:40.363 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/css/eb0e8eb7a28693… | 200 | — | 84 ms |
| 19:43:40.363 | GET | https://securepubads.g.doubleclick.net/tag/js/gpt.js | 200 | — | 158 ms |
| 19:43:40.363 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/upa-visitor… | 200 | — | 128 ms |
| 19:43:40.364 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/css/9b17c4945ab0f7… | 200 | — | 136 ms |
| 19:43:40.364 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/7567.56f612… | 200 | — | 117 ms |
| 19:43:40.364 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/8673.552e0a… | 200 | — | 118 ms |
| 19:43:40.364 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/8872.5387fc… | 200 | — | 135 ms |
| 19:43:40.364 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/2274.418149… | 200 | — | 139 ms |
| 19:43:40.364 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_-2D1653_sn_A1JDCPTI74ISRKR34IA… | 200 | — | 244 ms |
| 19:43:40.369 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_-2D1653_sn_A1JDCPTI74ISRKR34IA… | 200 | — | 58 ms |
| 19:43:40.409 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/287.650837a… | 200 | — | 121 ms |
| 19:43:40.409 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_-2D1653_sn_A1JDCPTI74ISRKR34IA… | 200 | — | 106 ms |
| 19:43:40.463 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/platformContainer.11.10.1.js | 200 | — | 167 ms |
| 19:43:40.464 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:40.465 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:40.597 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/cj-page-visits | 200 | — | 530 ms |
| 19:43:40.599 | GET | https://www.gstatic.com/recaptcha/releases/Br0hYqpfWeFzYCAXLD4UuCIV/recaptcha__en.js | 200 | — | 310 ms |
| 19:43:40.605 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 888 ms |
| 19:43:40.627 | GET | https://pisces.bbystatic.com/image2/BestBuy_US/dam/5770989-ghp1-appls-mds-956288fa-6790-4… | 200 | — | 96 ms |
| 19:43:40.704 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:40.705 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:40.767 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/mtSpan-55de0c5e2415359b1… | 200 | — | 189 ms |
| 19:43:40.768 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/confirmIt-245d713c1a9c5a… | 200 | — | 142 ms |
| 19:43:40.770 | GET | https://www.googletagmanager.com/gtag/js?id=DC-4448269 | 200 | — | 326 ms |
| 19:43:40.772 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/gtagATC-424022c58f369c9b… | 200 | — | 139 ms |
| 19:43:40.795 | GET | https://dpm.demdex.net/id?d_visid_ver=4.4.0&d_fieldgroup=MC&d_rtbd=json&d_ver=2&d_verify=… | 302 | — | 352 ms |
| 19:43:40.795 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/aq-init-bc608c12c08cd157… | 200 | — | 117 ms |
| 19:43:40.812 | GET | https://securepubads.g.doubleclick.net/pagead/managed/js/gpt/m202605130101/pubads_impl.js… | 200 | — | 162 ms |
| 19:43:40.854 | GET | https://www.bestbuy.com/~assets/bby/_img/int/plsvgdef-frontend/svg/Question_Line_Sm.svg | 200 | — | 130 ms |
| 19:43:40.854 | GET | https://www.bestbuy.com/~assets/bby/_img/int/plsvgdef-frontend/svg/Shipping_Line_Sm.svg | 200 | — | 130 ms |
| 19:43:40.854 | GET | https://www.bestbuy.com/~assets/bby/_img/int/plsvgdef-frontend/svg/Delivery_Line_Sm.svg | 200 | — | 130 ms |
| 19:43:40.854 | GET | https://www.bestbuy.com/~assets/bby/_img/int/plsvgdef-frontend/svg/ReturnPolicy_Line_Sm.s… | 200 | — | 130 ms |
| 19:43:40.854 | GET | https://www.bestbuy.com/~assets/bby/_img/int/plsvgdef-frontend/svg/PriceMatchGuarantee_Li… | 200 | — | 130 ms |
| 19:43:40.854 | GET | https://www.bestbuy.com/~assets/bby/_img/int/plsvgdef-frontend/svg/MobileApp_Line_Sm.svg | 200 | — | 131 ms |
| 19:43:40.869 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 509 ms |
| 19:43:40.871 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 436 ms |
| 19:43:40.873 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 604 ms |
| 19:43:40.876 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 446 ms |
| 19:43:40.878 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 447 ms |
| 19:43:40.882 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 501 ms |
| 19:43:40.883 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 471 ms |
| 19:43:40.902 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-vendors-_yarn_cache_gvp-lib-ac… | 200 | — | 118 ms |
| 19:43:40.991 | GET | https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6LeP0dgrAAAAAFn_1X2rBkI8vJKKsU0… | 200 | — | 194 ms |
| 19:43:41.014 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:41.036 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:41.068 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 257 ms |
| 19:43:41.082 | GET | https://dpm.demdex.net/id/rd?d_visid_ver=4.4.0&d_fieldgroup=MC&d_rtbd=json&d_ver=2&d_veri… | 200 | — | 64 ms |
| 19:43:41.082 | GET | https://www.bestbuy.com/streams/v1/SEARCH_TERM?limit=25 | 200 | — | 182 ms |
| 19:43:41.091 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 64 ms |
| 19:43:41.094 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 68 ms |
| 19:43:41.096 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 66 ms |
| 19:43:41.174 | GET | blob:https://www.bestbuy.com/0de5d13f-4009-433a-bc5c-9f91d0fffb79 | -1 | — | <1 ms |
| 19:43:41.198 | GET | https://bestbuy.demdex.net/dest5.html?d_nsid=undefined | 200 | — | 239 ms |
| 19:43:41.221 | GET | https://www.googletagmanager.com/gtag/js?id=AW-1066288264&cx=c&gtm=4e65d0 | 200 | — | 143 ms |
| 19:43:41.221 | POST | https://ad.doubleclick.net/activity;src=4448269;type=bbycom;cat=BBY-S0;rcb=4;ord=61276243… | 302 | — | 335 ms |
| 19:43:41.224 | GET | https://4448269.fls.doubleclick.net/activityi;src=4448269;type=bbycom;cat=BBY-S0;rcb=4;or… | 302 | — | 199 ms |
| 19:43:41.225 | POST | https://www.google.com/ccm/collect?rcb=4&frm=0&en=page_view&dl=https%3A%2F%2Fwww.bestbuy.… | 200 | — | 41 ms |
| 19:43:41.229 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/cjc-page-requests | 200 | — | 313 ms |
| 19:43:41.351 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:41.360 | GET | https://www.bestbuy.com/site/canopy/component/pricing/price-change-notification/v1?device… | 200 | — | 401 ms |
| 19:43:41.365 | GET | https://www.bestbuy.com/site/canopy/component/shop/account-menu/v1?businessName=%24(csi.u… | 200 | — | 367 ms |
| 19:43:41.369 | GET | https://www.gstatic.com/recaptcha/releases/Br0hYqpfWeFzYCAXLD4UuCIV/styles__ltr.css | 200 | — | 341 ms |
| 19:43:41.369 | GET | https://www.gstatic.com/recaptcha/releases/Br0hYqpfWeFzYCAXLD4UuCIV/recaptcha__en.js | 200 | — | 221 ms |
| 19:43:41.370 | GET | https://www.bestbuy.com/site/canopy/component/shop/stips/v1?deviceClass=l&placement=header | 200 | — | 754 ms |
| 19:43:41.390 | GET | https://4448269.fls.doubleclick.net/activityi;dc_pre=CKyxmc6KwZQDFd7MdQkdd_8vCg;src=44482… | 200 | — | 45 ms |
| 19:43:41.458 | POST | https://www.google.com/ccm/collect?rcb=15&frm=0&en=page_view&dl=https%3A%2F%2Fwww.bestbuy… | 200 | — | 44 ms |
| 19:43:41.458 | POST | https://www.google.com/rmkt/collect/1066288264/?random=1779047021388&cv=11&fst=1779047021… | 200 | — | 52 ms |
| 19:43:41.458 | GET | https://www.googleadservices.com/pagead/conversion/1066288264/?random=1779047021454&cv=11… | 200 | — | 145 ms |
| 19:43:41.458 | GET | https://www.googleadservices.com/pagead/conversion/1066288264/?random=1779047021450&cv=11… | 200 | — | 61 ms |
| 19:43:41.458 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/1066288264/?random=17790… | 200 | — | 951 ms |
| 19:43:41.471 | GET | https://securepubads.g.doubleclick.net/pagead/managed/dict/m202605140101/gpt | 200 | — | 127 ms |
| 19:43:41.473 | GET | https://www.bestbuy.com/site/canopy/component/evoc/talk-to-us/v1?deviceClass=l&isBot=fals… | 200 | — | 259 ms |
| 19:43:41.474 | GET | https://www.bestbuy.com/site/canopy/component/evoc/talk-to-us/v1?deviceClass=l&isBot=fals… | 200 | — | 343 ms |
| 19:43:41.477 | GET | https://www.bestbuy.com/site/canopy/component/shop/stips/v1?_lazyHydrate=false&deviceClas… | 200 | — | 679 ms |
| 19:43:41.504 | GET | https://ad.doubleclick.net/activity;dc_pre=CK68l86KwZQDFQLclAkdn84x9A;src=4448269;type=bb… | 302 | — | 39 ms |
| 19:43:41.506 | GET | https://www.google.com/gmp/conversion/_dc_unique_id=16226654067353149372;_dc_ptd=ChAI8M6l… | 200 | — | 105 ms |
| 19:43:41.568 | POST | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/1066288264/?random=15676… | 302 | — | 951 ms |
| 19:43:41.588 | POST | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/1066288264/?random=16341… | 302 | — | 930 ms |
| 19:43:41.611 | GET | https://adservice.google.com/ddm/fls/z/dc_pre=CKyxmc6KwZQDFd7MdQkdd_8vCg;src=4448269;type… | 200 | — | 161 ms |
| 19:43:41.611 | GET | https://www.googleadservices.com/pagead/conversion.js | 200 | — | 194 ms |
| 19:43:41.628 | GET | https://aa.agkn.com/adscores/g.pixel?sid=9211132908&aam=038866850698240301129958344831760… | 302 | — | 205 ms |
| 19:43:41.659 | GET | https://www.bestbuy.com/site/canopy/component/shop/interruptions-manager/v1 | 200 | — | 523 ms |
| 19:43:41.672 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 48 ms |
| 19:43:41.745 | GET | https://idsync.rlcdn.com/365868.gif?partner_uid=03886685069824030112995834483176007842 | 307 | — | 190 ms |
| 19:43:41.748 | GET | https://assets.bbystatic.com/shop/account-menu/dist/client/client-6046ee5d99fb6d1f20129a4… | 200 | — | 166 ms |
| 19:43:41.749 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/3818-f8a2f130f510dc5… | 200 | — | 136 ms |
| 19:43:41.755 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-vendors-_yarn_cache_gvp-lib-in… | 200 | — | 187 ms |
| 19:43:41.755 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-vendors-_yarn_cache_symbol-obs… | 200 | — | 187 ms |
| 19:43:41.756 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-vendors-_yarn_cache_redux-npm-… | 200 | — | 187 ms |
| 19:43:41.774 | GET | https://assets.bbystatic.com/pricing/price-change-notification/dist/client/client-2bffc37… | 200 | — | 348 ms |
| 19:43:41.800 | GET | https://dpm.demdex.net/ibs:dpid=21&dpuuid=213450605615016451778 | 200 | — | 77 ms |
| 19:43:41.815 | GET | https://www.googleadservices.com/pagead/conversion/11160642801/?random=1779047021807&cv=9… | 200 | — | 52 ms |
| 19:43:41.824 | GET | https://www.googleadservices.com/pagead/conversion/700350863/?random=1779047021813&cv=9&f… | 200 | — | 56 ms |
| 19:43:41.824 | GET | https://www.googleadservices.com/pagead/conversion/10786703110/?random=1779047021822&cv=9… | 200 | — | 52 ms |
| 19:43:41.824 | GET | https://www.googleadservices.com/pagead/conversion/780394176/?random=1779047021819&cv=9&f… | 200 | — | 63 ms |
| 19:43:41.826 | GET | https://www.google.com/recaptcha/enterprise/webworker.js?hl=en&v=Br0hYqpfWeFzYCAXLD4UuCIV | 200 | — | 220 ms |
| 19:43:41.834 | GET | https://www.googleadservices.com/pagead/conversion/731773981/?random=1779047021830&cv=9&f… | 200 | — | 55 ms |
| 19:43:41.834 | GET | https://www.googleadservices.com/pagead/conversion/796518160/?random=1779047021831&cv=9&f… | 200 | — | 54 ms |
| 19:43:41.834 | GET | https://www.googleadservices.com/pagead/conversion/10805093356/?random=1779047021827&cv=9… | 200 | — | 57 ms |
| 19:43:41.834 | GET | https://www.googleadservices.com/pagead/conversion/796554574/?random=1779047021829&cv=9&f… | 200 | — | 56 ms |
| 19:43:41.834 | GET | https://www.googleadservices.com/pagead/conversion/299548407/?random=1779047021825&cv=9&f… | 200 | — | 58 ms |
| 19:43:41.834 | GET | https://www.googleadservices.com/pagead/conversion/467818232/?random=1779047021827&cv=9&f… | 200 | — | 62 ms |
| 19:43:41.834 | GET | https://www.googleadservices.com/pagead/conversion/800420529/?random=1779047021832&cv=9&f… | 200 | — | 53 ms |
| 19:43:41.834 | GET | https://www.googleadservices.com/pagead/conversion/797195902/?random=1779047021833&cv=9&f… | 200 | — | 53 ms |
| 19:43:41.835 | GET | https://www.googleadservices.com/pagead/conversion/797191494/?random=1779047021834&cv=9&f… | 200 | — | 55 ms |
| 19:43:41.847 | GET | https://token.rubiconproject.com/token?pid=6404&puid=038866850698240301129958344831760078… | 204 No Content | — | 417 ms |
| 19:43:41.865 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/kDGYzLOQ/d2YKXBFXew4/TD/gwXSZsbmQt | 200 | — | 307 ms |
| 19:43:41.876 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/11160642801/?random=2034… | 302 | — | 194 ms |
| 19:43:41.882 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/10786703110/?random=8497… | 302 | — | 78 ms |
| 19:43:41.882 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/700350863/?random=147300… | 302 | — | 78 ms |
| 19:43:41.890 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/780394176/?random=752613… | 302 | — | 73 ms |
| 19:43:41.897 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/evoc-talk_to_us-v1-0… | 200 | — | 114 ms |
| 19:43:41.902 | GET | https://idsync.rlcdn.com/1000.gif?memo=CKyqFhIxCi0IARCYEhomMDM4ODY2ODUwNjk4MjQwMzAxMTI5OT… | 307 | — | 65 ms |
| 19:43:41.903 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/731773981/?random=169392… | 302 | — | 80 ms |
| 19:43:41.904 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/797191494/?random=179321… | 302 | — | 74 ms |
| 19:43:41.905 | GET | https://www.gstatic.com/recaptcha/releases/Br0hYqpfWeFzYCAXLD4UuCIV/recaptcha__en.js | 200 | — | 11 ms |
| 19:43:41.906 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/10805093356/?random=6190… | 302 | — | 248 ms |
| 19:43:41.906 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/796518160/?random=378794… | 302 | — | 251 ms |
| 19:43:41.907 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/796554574/?random=205249… | 302 | — | 254 ms |
| 19:43:41.908 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/467818232/?random=169253… | 302 | — | 221 ms |
| 19:43:41.908 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/299548407/?random=152401… | 302 | — | 246 ms |
| 19:43:41.909 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/800420529/?random=100703… | 302 | — | 221 ms |
| 19:43:41.912 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/797195902/?random=137173… | 302 | — | 232 ms |
| 19:43:41.953 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/137-6046ee5d99fb6d… | 200 | — | 169 ms |
| 19:43:41.953 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/232-6046ee5d99fb6d… | 200 | — | 172 ms |
| 19:43:41.953 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/platformContainer.2022.11.10.1.js | 200 | — | 182 ms |
| 19:43:41.962 | GET | https://x.dlx.addthis.com/e/demdex_sync?na_exid=03886685069824030112995834483176007842&ru… | -1 | — | <1 ms |
| 19:43:41.970 | GET | https://dpm.demdex.net/ibs:dpid=477&dpuuid=b2b42df6b5acb9ee1d1167bcb661ef557f13d1a065c06e… | 200 | — | 51 ms |
| 19:43:42.011 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/8216-ceb7eb6f1a3c8c7… | 200 | — | 111 ms |
| 19:43:42.027 | GET | https://www.google.com/pagead/1p-conversion/11160642801/?random=2034097123&cv=9&fst=17790… | 200 | — | 48 ms |
| 19:43:42.029 | GET | https://www.google.com/pagead/1p-conversion/780394176/?random=75261372&cv=9&fst=177904702… | 200 | — | 47 ms |
| 19:43:42.029 | GET | https://www.google.com/pagead/1p-conversion/797191494/?random=1793218572&cv=9&fst=1779047… | 200 | — | 49 ms |
| 19:43:42.030 | GET | https://www.google.com/pagead/1p-conversion/10786703110/?random=849784305&cv=9&fst=177904… | 200 | — | 53 ms |
| 19:43:42.030 | GET | https://www.google.com/pagead/1p-conversion/700350863/?random=1473004095&cv=9&fst=1779047… | 200 | — | 54 ms |
| 19:43:42.034 | GET | https://www.google.com/pagead/1p-conversion/731773981/?random=1693928416&cv=9&fst=1779047… | 200 | — | 48 ms |
| 19:43:42.051 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-vendors-_yarn___virtual___redu… | 200 | — | 109 ms |
| 19:43:42.051 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-vendors-_yarn_cache_prop-types… | 200 | — | 121 ms |
| 19:43:42.051 | GET | https://www.bestbuy.com/~assets/bby/_com/pricing/price-change-notification/dist/client/55… | 200 | — | 133 ms |
| 19:43:42.051 | GET | https://www.bestbuy.com/~assets/bby/_com/pricing/price-change-notification/dist/client/55… | 200 | — | 168 ms |
| 19:43:42.051 | GET | https://www.bestbuy.com/~assets/bby/_com/pricing/price-change-notification/dist/client/12… | 200 | — | 203 ms |
| 19:43:42.052 | GET | https://www.bestbuy.com/~assets/bby/_com/brix/7.11.35/js/6082.js | 200 | — | 109 ms |
| 19:43:42.052 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-vendors-_yarn_cache_gvp-lib-fa… | 200 | — | 120 ms |
| 19:43:42.052 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-vendors-_yarn_cache_lodash-npm… | 200 | — | 121 ms |
| 19:43:42.052 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-vendors-_yarn_cache_falcor-npm… | 200 | — | 121 ms |
| 19:43:42.052 | GET | https://www.bestbuy.com/~assets/bby/_com/brix/7.11.35/js/8809.js | 200 | — | 131 ms |
| 19:43:42.068 | GET | https://cm.g.doubleclick.net/pixel?google_nid=adobe_dmp&google_cm&gdpr=0&gdpr_consent=&go… | 302 | — | 226 ms |
| 19:43:42.132 | GET | https://www.google.com/pagead/1p-conversion/467818232/?random=1692530201&cv=9&fst=1779047… | 200 | — | 65 ms |
| 19:43:42.133 | GET | https://www.google.com/pagead/1p-conversion/800420529/?random=100703085&cv=9&fst=17790470… | 200 | — | 68 ms |
| 19:43:42.133 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/9495-ceb7eb6f1a3c8c7… | 200 | — | 143 ms |
| 19:43:42.133 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/3696-ceb7eb6f1a3c8c7… | 200 | — | 142 ms |
| 19:43:42.134 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/333-ceb7eb6f1a3c8c77… | 200 | — | 130 ms |
| 19:43:42.134 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/7243-ceb7eb6f1a3c8c7… | 200 | — | 130 ms |
| 19:43:42.134 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/8325-ceb7eb6f1a3c8c7… | 200 | — | 142 ms |
| 19:43:42.134 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/8441-ceb7eb6f1a3c8c7… | 200 | — | 188 ms |
| 19:43:42.134 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/1830-ceb7eb6f1a3c8c7… | 200 | — | 188 ms |
| 19:43:42.134 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/stips/dist/client/client-8d41dfb3ae61238f1c… | 200 | — | 187 ms |
| 19:43:42.147 | GET | https://www.google.com/pagead/1p-conversion/797195902/?random=1371733927&cv=9&fst=1779047… | 200 | — | 96 ms |
| 19:43:42.157 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-2022-vendors-_yarn_cache_react… | 200 | — | 165 ms |
| 19:43:42.157 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-2022-vendors-_yarn___virtual__… | 200 | — | 166 ms |
| 19:43:42.157 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-2022-vendors-_yarn___virtual__… | 200 | — | 167 ms |
| 19:43:42.166 | GET | https://www.google.com/pagead/1p-conversion/10805093356/?random=619029845&cv=9&fst=177904… | 200 | — | 84 ms |
| 19:43:42.166 | GET | https://www.google.com/pagead/1p-conversion/299548407/?random=1524018008&cv=9&fst=1779047… | 200 | — | 85 ms |
| 19:43:42.167 | GET | https://www.google.com/pagead/1p-conversion/796518160/?random=37879475&cv=9&fst=177904702… | 200 | — | 86 ms |
| 19:43:42.168 | GET | https://www.google.com/pagead/1p-conversion/796554574/?random=2052494787&cv=9&fst=1779047… | 200 | — | 83 ms |
| 19:43:42.168 | GET | https://c.bing.com/c.gif?uid=03886685069824030112995834483176007842&Red3=MSAdobe_pd&gdpr=… | 302 | — | 388 ms |
| 19:43:42.188 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/interruptions-manager/dist/client/client-0e… | 200 | — | 131 ms |
| 19:43:42.247 | GET | https://dpm.demdex.net/ibs:dpid=771&dpuuid=CAESELnDq7XA9jk6YPmqvSVGgzQ&google_cver=1?gdpr… | 200 | — | 44 ms |
| 19:43:42.283 | GET | https://ums.acuityplatform.com/tum?umid=41&uid=03886685069824030112995834483176007842&rur… | 204 | — | 213 ms |
| 19:43:42.362 | GET | https://www.google.com/pagead/1p-user-list/1066288264/?random=1779047021388&cv=11&fst=177… | 200 | — | 52 ms |
| 19:43:42.377 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/stips/dist/client/109-8d41dfb3ae61238f1c871… | 200 | — | 92 ms |
| 19:43:42.397 | GET | https://fei.pro-market.net/engine?site=141472;size=1x1;mimetype=img;du=67;csync=038866850… | 200 | — | 287 ms |
| 19:43:42.448 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/interruptions-manager/dist/client/791-0e092… | 200 | — | 176 ms |
| 19:43:42.449 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/interruptions-manager/dist/client/542-0e092… | 200 | — | 123 ms |
| 19:43:42.456 | GET | https://dpm.demdex.net/ibs:dpid=1957&dpuuid=132B6F3AE6FC6E430C137866E7516FB0 | 200 | — | 49 ms |
| 19:43:42.491 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/882-6046ee5d99fb6d… | 200 | — | 156 ms |
| 19:43:42.491 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/831-6046ee5d99fb6d… | 200 | — | 158 ms |
| 19:43:42.491 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/client-button.css | 200 | — | 179 ms |
| 19:43:42.491 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/251-6046ee5d99fb6d… | 200 | — | 180 ms |
| 19:43:42.491 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-vendors-_yarn_cache_react-npm-… | 200 | — | 181 ms |
| 19:43:42.491 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/client-button-6046… | 200 | — | 180 ms |
| 19:43:42.491 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-lib-appear_dist_main_umd_js-26… | 200 | — | 181 ms |
| 19:43:42.491 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-vendors-_yarn_cache_object-ass… | 200 | — | 180 ms |
| 19:43:42.491 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/684-6046ee5d99fb6d… | 200 | — | 182 ms |
| 19:43:42.491 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-_yarn___virtual___gvp-lib-embe… | 200 | — | 185 ms |
| 19:43:42.501 | GET | https://px.owneriq.net/eucm/p/adpq?redir=https%3A%2F%2Fdpm.demdex.net%2Fibs%3Adpid%3D5319… | 200 | — | 314 ms |
| 19:43:42.517 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/5090-ceb7eb6f1a3c8c7… | 200 | — | 158 ms |
| 19:43:42.517 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/3945-ceb7eb6f1a3c8c7… | 200 | — | 160 ms |
| 19:43:42.518 | GET | https://www.google.com/pagead/1p-conversion/1066288264/?random=1634160124&cv=11&fst=17790… | 200 | — | 45 ms |
| 19:43:42.518 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/814-ceb7eb6f1a3c8c77… | 200 | — | 159 ms |
| 19:43:42.518 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/7754-ceb7eb6f1a3c8c7… | 200 | — | 166 ms |
| 19:43:42.519 | GET | https://www.google.com/pagead/1p-conversion/1066288264/?random=1567638124&cv=11&fst=17790… | 200 | — | 59 ms |
| 19:43:42.524 | GET | https://www.bestbuy.com/pcn-api/basket?context=header&vt=11d61959-64a5-4174-a3ae-470acdd2… | 200 | — | 336 ms |
| 19:43:42.573 | GET | https://www.bestbuy.com/api/tcfb/model.json?paths=%5B%5B%22shop%22%2C%22scds%22%2C%22v2%2… | 200 | — | 288 ms |
| 19:43:42.581 | POST | https://www.google.com/recaptcha/enterprise/reload?k=6LeP0dgrAAAAAFn_1X2rBkI8vJKKsU0-LOJO… | 200 | — | 85 ms |
| 19:43:42.610 | GET | https://sync.crwdcntrl.net/map/c=9828/tp=ADBE/gdpr=0/gdpr_consent=/tpid=03886685069824030… | 302 | — | 271 ms |
| 19:43:42.698 | POST | https://www.bestbuy.com/cj-recaptcha/v1/submit | 204 | — | 282 ms |
| 19:43:42.815 | GET | https://sync.crwdcntrl.net/map/ct=y/c=9828/tp=ADBE/gdpr=0/gdpr_consent=/tpid=038866850698… | 302 | — | 60 ms |
| 19:43:42.850 | POST | https://www.google.com/recaptcha/enterprise/clr?k=6LeP0dgrAAAAAFn_1X2rBkI8vJKKsU0-LOJOsczw | 200 | — | 128 ms |
| 19:43:42.976 | GET | https://dpm.demdex.net/ibs:dpid=121998&dpuuid=750a8493552fa81adadc1dc5b7ef7b9d | 200 | — | 49 ms |
| 19:43:43.066 | GET | https://www.bestbuy.com/site/searchpage.jsp?st=playstation+5+console | 200 | — | 1.99 s |
| 19:43:43.067 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 205 ms |
| 19:43:43.602 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/deptCatLanding-9257f42ee… | 200 | — | 124 ms |
| 19:43:43.602 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/merchandising-61910f1a9b… | 200 | — | 125 ms |
| 19:43:45.020 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | -1 | — | <1 ms |
| 19:43:45.036 | GET | https://pisces.bbystatic.com/image2/BestBuy_US/images/products/e44a0a67-7842-4cd6-8b23-16… | 200 | — | 175 ms |
| 19:43:45.036 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/css/e7e52b1732971f92.css | 200 | — | 174 ms |
| 19:43:45.037 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/css/60b898ebfc453365.css | 200 | — | 171 ms |
| 19:43:45.037 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/css/14f1addfbe0af0ce.css | 200 | — | 171 ms |
| 19:43:45.037 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/css/5069eaf783e4b831.css | 200 | — | 171 ms |
| 19:43:45.037 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/css/602b022506552160.css | 200 | — | 171 ms |
| 19:43:45.037 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/css/3cbd1c0f897b3ec6.css | 200 | — | 190 ms |
| 19:43:45.037 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/css/542f9c4ec131aac5.css | 200 | — | 193 ms |
| 19:43:45.037 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/css/646e7858ce2746dd.css | 200 | — | 191 ms |
| 19:43:45.037 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/css/4d6a2f4f25eb05c9.css | 200 | — | 192 ms |
| 19:43:45.037 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/css/6c1027c8529cde10.css | 200 | — | 193 ms |
| 19:43:45.037 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/css/ef6a8b2112e1c474.css | 200 | — | 215 ms |
| 19:43:45.037 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/css/055dde9e603d27e8.css | 200 | — | 230 ms |
| 19:43:45.037 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/css/4027c5a810ae50cf.css | 200 | — | 230 ms |
| 19:43:45.037 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/webpack-75e1ed25a5f… | 200 | — | 461 ms |
| 19:43:45.037 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/618f8807-dcda685ac1… | 200 | — | 472 ms |
| 19:43:45.037 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/2364-302376caa88aa8… | 200 | — | 568 ms |
| 19:43:45.037 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/main-app-04e28c8fe9… | 200 | — | 567 ms |
| 19:43:45.037 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/f67032f2-19f3c9d238… | 200 | — | 575 ms |
| 19:43:45.037 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/718d2ac6-31bbed22b1… | 200 | — | 575 ms |
| 19:43:45.037 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/572fddda-9df44d6e0c… | 200 | — | 602 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/eda182e7-19dd47f0db… | 200 | — | 569 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/7fe79fa1-9787db03a4… | 200 | — | 579 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/b8dcfb4b-49ffb3360a… | 200 | — | 582 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/68a889a2-f4d11f411f… | 200 | — | 599 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/1e87141b-ac770961ac… | 200 | — | 598 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/498a1a03-b15d642bfe… | 200 | — | 599 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/0baf4cd7-6f756cc5eb… | 200 | — | 600 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/0ccdef0f-48c6f0e0b8… | 200 | — | 600 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/f0aae170-bb79640937… | 200 | — | 601 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/ef21e0a5-7c14d4308f… | 200 | — | 604 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/8bb2492a-8c8e54b9b7… | 200 | — | 607 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/2833-ee9f36f6d02571… | 200 | — | 606 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/bff65990-438e75e760… | 200 | — | 608 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/aae65a39-50ca5acd87… | 200 | — | 605 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/c4e3855d-6ce241408a… | 200 | — | 608 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/9aaa00de-1177042660… | 200 | — | 607 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/3640-f1de94efa8e1ba… | 200 | — | 610 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/2690-5dfb5e380d0cf9… | 200 | — | 625 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/9199-6f09a5a4d044e6… | 200 | — | 652 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/8225-57101d7d600e41… | 200 | — | 650 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/1078-b38bdaa8ac5164… | 200 | — | 649 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/9114-74c3aa1b37dc0e… | 200 | — | 653 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/2635-7114cd3f9df048… | 200 | — | 662 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/2912-fce7b0d777071a… | 200 | — | 662 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/5784-6b444e80267015… | 200 | — | 664 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/1105-86be0e27226c64… | 200 | — | 647 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/app/productlist/sea… | 200 | — | 687 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/8662-195308428d21d0… | 200 | — | 689 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/9fe71e49-106d1cb1d2… | 200 | — | 690 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/c07e5374-00d9295997… | 200 | — | 693 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/8994-fb302718870eba… | 200 | — | 694 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/app/productlist/lay… | 200 | — | 704 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/3605-603b69eae8b928… | 200 | — | 705 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/app/layout-69e4f5b8… | 200 | — | 705 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/6699-7fd3842fcc69f0… | 200 | — | 720 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/1571-00689cabcd7f92… | 200 | — | 702 ms |
| 19:43:45.038 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/7005-24c502152e764e… | 200 | — | 722 ms |
| 19:43:45.039 | GET | https://www.google.com/recaptcha/enterprise.js?render=6LeP0dgrAAAAAFn_1X2rBkI8vJKKsU0-LOJ… | 200 | — | 20 ms |
| 19:43:45.039 | GET | https://www.bestbuy.com/~assets/bby/_com/deo-client-script.js | 200 | — | 20 ms |
| 19:43:45.039 | GET | https://www.bestbuy.com/~assets/bby/_com/libs/goteam/v26.16.2.js | 200 | — | 21 ms |
| 19:43:45.039 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/fonts/164de2c41958523c.wof… | 200 | — | 219 ms |
| 19:43:45.039 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/fonts/ff935616cc06e2b0.wof… | 200 | — | 227 ms |
| 19:43:45.039 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/fonts/e034ae9741bc6156.wof… | 200 | — | 227 ms |
| 19:43:45.039 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/app/error-5c542b2c5… | 200 | — | 706 ms |
| 19:43:45.039 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/app/not-found-542db… | 200 | — | 707 ms |
| 19:43:45.044 | GET | https://www.bestbuy.com/~assets/bby/_com/deo-lss-activation.js | 200 | — | 11 ms |
| 19:43:45.044 | GET | https://nexus.ensighten.com/bestbuy/privacy_init/Bootstrap.js | 200 | — | 74 ms |
| 19:43:45.044 | GET | https://www.bestbuy.com/~assets/bby/_js/ext/bbydyn/dyn_digital_plp.js | 200 | — | 710 ms |
| 19:43:45.044 | GET | https://www.bestbuy.com/akam/13/270d3632 | 200 | — | 707 ms |
| 19:43:45.045 | GET | https://www.bestbuy.com/~assets/bby/_com/gvp/lib-config-service/2.3.3/dist/main.js | 200 | — | 10 ms |
| 19:43:45.045 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/lib-mf-assets/2.1.2/dist/main.js | 200 | — | 10 ms |
| 19:43:45.045 | GET | https://www.bestbuy.com/~assets/bby/_com/setup-event-manager.8.9.11.js | 200 | — | 268 ms |
| 19:43:45.045 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-q/6.0.4/dist/analyticsQ.bundle.js | 200 | — | 268 ms |
| 19:43:45.045 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/platformContainerOrchestrationProxy.1… | 200 | — | 268 ms |
| 19:43:45.045 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/lib-eventmanager/3.1.0/dist/event-manager.js | 200 | — | 268 ms |
| 19:43:45.045 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/@bestbuy/bby-debug/dist/client/auto-loader-… | 200 | — | 268 ms |
| 19:43:45.045 | GET | https://www.bestbuy.com/~assets/bby/_com/brix/7.11.35/js/brixRemoteEntry.js | 200 | — | 268 ms |
| 19:43:45.045 | GET | https://www.bestbuy.com/~assets/bby/_com/@ds/unified-chat/dist/javascript/unified-chat-in… | 200 | — | 268 ms |
| 19:43:45.045 | GET | https://www.bestbuy.com/lux.js | 200 | — | 268 ms |
| 19:43:45.056 | GET | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 200 | — | 200 ms |
| 19:43:45.056 | GET | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/kDGYzLOQ/d2YKXBFXew4/TD/gwXSZsbmQt?v… | 200 | — | 701 ms |
| 19:43:45.297 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:45.343 | GET | https://nexus.ensighten.com/bestbuy/privacy_prod/Bootstrap.js | 200 | — | 128 ms |
| 19:43:45.343 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 548 ms |
| 19:43:45.401 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/fonts/d088a1bc70979b2b.wof… | 200 | — | 273 ms |
| 19:43:45.401 | GET | https://pisces.bbystatic.com/image2/BestBuy_US/images/products/8585e5db-aaa3-47d4-94c6-fd… | 200 | — | 348 ms |
| 19:43:45.401 | GET | https://pisces.bbystatic.com/image2/BestBuy_US/images/products/26c4a888-1a2d-4e44-ab95-bf… | 200 | — | 354 ms |
| 19:43:45.401 | GET | https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6523/6523167_sd.jpg;maxHei… | 200 | — | 354 ms |
| 19:43:45.602 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/6884-8473bcd8b57cc8b1d5c… | 200 | — | 16 ms |
| 19:43:45.602 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/2286-f4563db0fdf951734eb… | 200 | — | 16 ms |
| 19:43:45.602 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/2163-ab6cfceaf386ebcfe52… | 200 | — | 14 ms |
| 19:43:45.602 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/2378-ebef7a4d3d8251107ee… | 200 | — | 15 ms |
| 19:43:45.649 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/interaction-01d33e2b062b… | 200 | — | 2 ms |
| 19:43:45.652 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/5581-e096874da8baa32a486… | 200 | — | 1 ms |
| 19:43:45.653 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/7164-e790f7049f5c9398b5b… | 200 | — | 4 ms |
| 19:43:45.653 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/customer-journal-8ff849b… | 200 | — | 4 ms |
| 19:43:45.694 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/cj-digital-schema1-2faec… | 200 | — | 1 ms |
| 19:43:45.895 | GET | https://www.bestbuy.com/~assets/bby/_com/@ds/unified-chat/dist/javascript/unified-chat-in… | 200 | — | 2 ms |
| 19:43:45.896 | GET | https://www.bestbuy.com/~assets/bby/_com/@ds/unified-chat/dist/javascript/unified-chat-in… | 200 | — | 1 ms |
| 19:43:45.896 | GET | https://www.bestbuy.com/~assets/bby/_com/@ds/unified-chat/dist/javascript/unified-chat-in… | 200 | — | 1 ms |
| 19:43:45.896 | GET | https://www.bestbuy.com/~assets/bby/_com/@ds/unified-chat/dist/javascript/unified-chat-in… | 200 | — | <1 ms |
| 19:43:45.936 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=0&c=2493&i=5fvhov&p=privacy_prod&… | 204 | — | 53 ms |
| 19:43:46.553 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/1015.7e0a8fd7948e04… | 200 | — | 106 ms |
| 19:43:46.581 | POST | https://www.bestbuy.com/akam/13/pixel_270d3632 | 200 | — | 134 ms |
| 19:43:46.590 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:46.626 | GET | https://www.bestbuy.com/services/conversation/web/api/v2/unified-chat/configuration | 200 | — | 2 ms |
| 19:43:46.844 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/4913-c8e91779834f0890658… | 200 | — | 2 ms |
| 19:43:46.844 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/2616-4d93e48dc493d12beaf… | 200 | — | 1 ms |
| 19:43:46.844 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/6654-99d231c40e8f6bb6430… | 200 | — | 1 ms |
| 19:43:46.848 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/6133-e679f02537ff34e13b2… | 200 | — | 1 ms |
| 19:43:46.848 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/5874-4c0bbc15c0a4c11f7c1… | 200 | — | 2 ms |
| 19:43:46.848 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/gtagConversion-5ce7d21df… | 200 | — | 5 ms |
| 19:43:46.848 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/adobeInit-651b3bd355e6e2… | 200 | — | 2 ms |
| 19:43:46.863 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/css/e4e909a12e79fb12.css | 200 | — | 202 ms |
| 19:43:46.864 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/5233.951c6af17150e7… | 200 | — | 200 ms |
| 19:43:46.864 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/d1478af2.c1dc7c09f2… | 200 | — | 201 ms |
| 19:43:46.864 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/4685.b0da228b5667cb… | 200 | — | 201 ms |
| 19:43:46.864 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/7980.092d3ba9e694ef… | 200 | — | 217 ms |
| 19:43:46.865 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/2892.2e070f3a1b6448… | 200 | — | 233 ms |
| 19:43:46.865 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/4156.d7b1679d6dc56c… | 200 | — | 234 ms |
| 19:43:46.900 | GET | blob:https://www.bestbuy.com/2b994b7a-85eb-42ac-ac88-1b1499646674 | -1 | — | <1 ms |
| 19:43:46.901 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:46.909 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/confirmIt-245d713c1a9c5a… | 200 | — | 2 ms |
| 19:43:46.910 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/mtSpan-55de0c5e2415359b1… | 200 | — | 1 ms |
| 19:43:46.912 | GET | https://www.googletagmanager.com/gtag/js?id=DC-4448269 | 200 | — | 2 ms |
| 19:43:46.926 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 85 ms |
| 19:43:47.067 | GET | https://www.googletagmanager.com/gtag/js?id=AW-1066288264&cx=c&gtm=4e65d0 | 200 | — | 7 ms |
| 19:43:47.067 | POST | https://ad.doubleclick.net/activity;src=4448269;type=bbycom;cat=BBY-S0;rcb=6;ord=77353840… | 302 | — | 313 ms |
| 19:43:47.069 | GET | https://4448269.fls.doubleclick.net/activityi;src=4448269;type=bbycom;cat=BBY-S0;rcb=6;or… | 302 | — | 42 ms |
| 19:43:47.069 | POST | https://www.google.com/ccm/collect?rcb=6&frm=0&en=page_view&dl=https%3A%2F%2Fwww.bestbuy.… | 200 | — | 37 ms |
| 19:43:47.105 | GET | blob:https://www.bestbuy.com/c2ccae44-859f-4d7f-b147-1acf20c30251 | -1 | — | <1 ms |
| 19:43:47.113 | GET | https://4448269.fls.doubleclick.net/activityi;dc_pre=COjd9tCKwZQDFRHhKAUdSYQ5Ow;src=44482… | 200 | — | 843 ms |
| 19:43:47.131 | POST | https://www.google.com/rmkt/collect/1066288264/?random=1779047027114&cv=11&fst=1779047027… | 200 | — | 39 ms |
| 19:43:47.131 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/1066288264/?random=17790… | 200 | — | 698 ms |
| 19:43:47.132 | POST | https://www.google.com/ccm/collect?rcb=7&frm=0&en=page_view&dl=https%3A%2F%2Fwww.bestbuy.… | 200 | — | 38 ms |
| 19:43:47.132 | GET | https://www.googleadservices.com/pagead/conversion/1066288264/?random=1779047027125&cv=11… | 200 | — | 43 ms |
| 19:43:47.132 | GET | https://www.googleadservices.com/pagead/conversion/1066288264/?random=1779047027128&cv=11… | 200 | — | 44 ms |
| 19:43:47.229 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 335 ms |
| 19:43:47.244 | POST | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/1066288264/?random=57945… | 302 | — | 136 ms |
| 19:43:47.244 | POST | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/1066288264/?random=26785… | 302 | — | 3.66 s |
| 19:43:47.380 | GET | https://www.google.com/pagead/1p-conversion/1066288264/?random=579457874&cv=11&fst=177904… | 200 | — | 51 ms |
| 19:43:47.381 | GET | https://ad.doubleclick.net/activity;dc_pre=CI-z9tCKwZQDFYjx4wcdsB4tzg;src=4448269;type=bb… | 302 | — | 114 ms |
| 19:43:47.387 | GET | https://www.google.com/gmp/conversion/_dc_unique_id=13720370323106689186;_dc_ptd=ChAI8M6l… | 200 | — | 154 ms |
| 19:43:47.472 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:47.869 | GET | https://www.bestbuy.com/suggest/v1/fragment/suggest/www?query=playstation%205%20console&c… | 200 | — | 250 ms |
| 19:43:47.870 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/css/f0e0b43a381b1735.css | 200 | — | 140 ms |
| 19:43:47.870 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/upa-visitor-optimiz… | 200 | — | 141 ms |
| 19:43:47.870 | GET | https://www.bestbuy.com/streams/v1/SEARCH_TERM?limit=25 | 200 | — | 260 ms |
| 19:43:47.871 | GET | https://securepubads.g.doubleclick.net/tag/js/gpt.js | 200 | — | 3 ms |
| 19:43:47.871 | GET | https://www.google.com/adsense/search/async-ads.js | 200 | — | 59 ms |
| 19:43:47.871 | GET | https://cdn.adsafeprotected.com/iasPET.1.js | 200 OK | — | 159 ms |
| 19:43:47.871 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/4971.aad8affa4e55a9… | 200 | — | 108 ms |
| 19:43:48.179 | GET | https://www.googleadservices.com/pagead/conversion.js | 200 | — | 3 ms |
| 19:43:48.180 | GET | https://adservice.google.com/ddm/fls/z/dc_pre=COjd9tCKwZQDFRHhKAUdSYQ5Ow;src=4448269;type… | 200 | — | 50 ms |
| 19:43:48.204 | GET | https://www.googleadservices.com/pagead/conversion/11160642801/?random=1779047028196&cv=9… | 200 | — | 47 ms |
| 19:43:48.215 | GET | https://www.googleadservices.com/pagead/conversion/700350863/?random=1779047028204&cv=9&f… | 200 | — | 48 ms |
| 19:43:48.216 | GET | https://www.googleadservices.com/pagead/conversion/780394176/?random=1779047028208&cv=9&f… | 200 | — | 50 ms |
| 19:43:48.216 | GET | https://www.googleadservices.com/pagead/conversion/299548407/?random=1779047028213&cv=9&f… | 200 | — | 46 ms |
| 19:43:48.216 | GET | https://www.googleadservices.com/pagead/conversion/10786703110/?random=1779047028211&cv=9… | 200 | — | 49 ms |
| 19:43:48.226 | GET | https://www.googleadservices.com/pagead/conversion/467818232/?random=1779047028215&cv=9&f… | 200 | — | 47 ms |
| 19:43:48.226 | GET | https://www.googleadservices.com/pagead/conversion/796554574/?random=1779047028220&cv=9&f… | 200 | — | 46 ms |
| 19:43:48.226 | GET | https://www.googleadservices.com/pagead/conversion/731773981/?random=1779047028222&cv=9&f… | 200 | — | 46 ms |
| 19:43:48.226 | GET | https://www.googleadservices.com/pagead/conversion/10805093356/?random=1779047028218&cv=9… | 200 | — | 54 ms |
| 19:43:48.226 | GET | https://www.googleadservices.com/pagead/conversion/796518160/?random=1779047028223&cv=9&f… | 200 | — | 50 ms |
| 19:43:48.226 | GET | https://www.googleadservices.com/pagead/conversion/800420529/?random=1779047028224&cv=9&f… | 200 | — | 49 ms |
| 19:43:48.229 | GET | https://www.googleadservices.com/pagead/conversion/797195902/?random=1779047028226&cv=9&f… | 200 | — | 53 ms |
| 19:43:48.229 | GET | https://www.googleadservices.com/pagead/conversion/797191494/?random=1779047028228&cv=9&f… | 200 | — | 52 ms |
| 19:43:48.252 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/11160642801/?random=4573… | 302 | — | 78 ms |
| 19:43:48.256 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/700350863/?random=137393… | 302 | — | 74 ms |
| 19:43:48.262 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/780394176/?random=200276… | 302 | — | 91 ms |
| 19:43:48.263 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/299548407/?random=147434… | 302 | — | 90 ms |
| 19:43:48.264 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/10786703110/?random=9982… | 302 | — | 89 ms |
| 19:43:48.268 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/467818232/?random=412227… | 302 | — | 86 ms |
| 19:43:48.271 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/731773981/?random=956366… | 302 | — | 82 ms |
| 19:43:48.271 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/796554574/?random=120749… | 302 | — | 84 ms |
| 19:43:48.276 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/10805093356/?random=1723… | 302 | — | 78 ms |
| 19:43:48.278 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/796518160/?random=555597… | 302 | — | 77 ms |
| 19:43:48.279 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/800420529/?random=998560… | 302 | — | 76 ms |
| 19:43:48.282 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/797195902/?random=212974… | 302 | — | 73 ms |
| 19:43:48.283 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/797191494/?random=195728… | 302 | — | 72 ms |
| 19:43:48.307 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/4928.937e47db528934… | 200 | — | 103 ms |
| 19:43:48.307 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/2575.6be82f1c7adcf3… | 200 | — | 104 ms |
| 19:43:48.330 | GET | https://www.google.com/pagead/1p-conversion/11160642801/?random=457349389&cv=9&fst=177904… | 200 | — | 44 ms |
| 19:43:48.331 | GET | https://www.google.com/pagead/1p-conversion/700350863/?random=1373937320&cv=9&fst=1779047… | 200 | — | 42 ms |
| 19:43:48.354 | GET | https://www.google.com/pagead/1p-conversion/10786703110/?random=998201951&cv=9&fst=177904… | 200 | — | 45 ms |
| 19:43:48.354 | GET | https://www.google.com/pagead/1p-conversion/731773981/?random=956366290&cv=9&fst=17790470… | 200 | — | 58 ms |
| 19:43:48.355 | GET | https://www.google.com/pagead/1p-conversion/780394176/?random=2002769224&cv=9&fst=1779047… | 200 | — | 49 ms |
| 19:43:48.356 | GET | https://www.google.com/pagead/1p-conversion/467818232/?random=412227391&cv=9&fst=17790470… | 200 | — | 57 ms |
| 19:43:48.356 | GET | https://www.google.com/pagead/1p-conversion/299548407/?random=1474344831&cv=9&fst=1779047… | 200 | — | 57 ms |
| 19:43:48.357 | GET | https://www.google.com/pagead/1p-conversion/796554574/?random=1207491542&cv=9&fst=1779047… | 200 | — | 65 ms |
| 19:43:48.357 | GET | https://www.google.com/pagead/1p-conversion/10805093356/?random=1723390121&cv=9&fst=17790… | 200 | — | 65 ms |
| 19:43:48.358 | GET | https://www.google.com/pagead/1p-conversion/796518160/?random=555597146&cv=9&fst=17790470… | 200 | — | 65 ms |
| 19:43:48.358 | GET | https://www.google.com/pagead/1p-conversion/797195902/?random=2129741444&cv=9&fst=1779047… | 200 | — | 67 ms |
| 19:43:48.358 | GET | https://www.google.com/pagead/1p-conversion/800420529/?random=998560925&cv=9&fst=17790470… | 200 | — | 69 ms |
| 19:43:48.359 | GET | https://www.google.com/pagead/1p-conversion/797191494/?random=195728776&cv=9&fst=17790470… | 200 | — | 65 ms |
| 19:43:50.712 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/css/a89de48840cb568f.css | 200 | — | 131 ms |
| 19:43:50.712 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/3229.6e5bd8800289a7… | 200 | — | 131 ms |
| 19:43:50.713 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/3704.888003a7ac2b83… | 200 | — | 132 ms |
| 19:43:50.713 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 60 ms |
| 19:43:50.856 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/platformContainer.11.10.1.js | 200 | — | 2 ms |
| 19:43:50.867 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:50.868 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:50.904 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/cj-page-visits | 200 | — | 191 ms |
| 19:43:50.905 | GET | https://www.gstatic.com/recaptcha/releases/Br0hYqpfWeFzYCAXLD4UuCIV/recaptcha__en.js | 200 | — | 3 ms |
| 19:43:50.909 | GET | https://www.google.com/pagead/1p-conversion/1066288264/?random=267857649&cv=11&fst=177904… | 200 | — | 48 ms |
| 19:43:51.037 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/9150.c6972606fbab3a… | 200 | — | 118 ms |
| 19:43:51.037 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/7357.ebe3d346a36c0a… | 200 | — | 118 ms |
| 19:43:51.287 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 80 ms |
| 19:43:51.292 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 75 ms |
| 19:43:51.348 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/4727.0ae14d175201a9… | 200 | — | 128 ms |
| 19:43:51.450 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 54 ms |
| 19:43:51.452 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 52 ms |
| 19:43:51.455 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 52 ms |
| 19:43:51.481 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 49 ms |
| 19:43:51.483 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:51.484 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:51.525 | GET | https://securepubads.g.doubleclick.net/pagead/managed/js/gpt/m202605130101/pubads_impl.js… | 200 | — | 2 ms |
| 19:43:51.533 | GET | https://ep1.adtrafficquality.google/getconfig/sodar?sv=200&tid=afs&tv=1234567890&st=env&s… | 200 | — | 225 ms |
| 19:43:51.541 | GET | https://www.google.com/pagead/1p-user-list/1066288264/?random=1779047027114&cv=11&fst=177… | 200 | — | 44 ms |
| 19:43:51.564 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 241 ms |
| 19:43:51.567 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 344 ms |
| 19:43:51.570 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 306 ms |
| 19:43:51.572 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 296 ms |
| 19:43:51.587 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-vendors-_yarn_cache_gvp-lib-ac… | 200 | — | 1 ms |
| 19:43:51.642 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/8100.1a0b1a045e899a… | 200 | — | 137 ms |
| 19:43:51.734 | GET | https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6LeP0dgrAAAAAFn_1X2rBkI8vJKKsU0… | 200 | — | 73 ms |
| 19:43:51.778 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:51.790 | GET | https://ep2.adtrafficquality.google/sodar/sodar2.js | 200 | — | 177 ms |
| 19:43:51.855 | GET | https://www.bestbuy.com/suggest/v1/fragment/suggest/www?query=playstation%205%20console&c… | 200 | — | 1 ms |
| 19:43:51.855 | GET | https://www.bestbuy.com/suggest/v1/fragment/products/www?skuids=6646419,6646420,6601524,6… | 200 | — | 200 ms |
| 19:43:51.858 | POST | https://csp.withgoogle.com/csp/frame-ancestors/38fac9d5b82543fc4729580d18ff2d3d | -1 | — | <1 ms |
| 19:43:51.864 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/cjc-page-requests | 200 | — | 247 ms |
| 19:43:51.885 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:51.897 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:51.928 | GET | https://www.gstatic.com/recaptcha/releases/Br0hYqpfWeFzYCAXLD4UuCIV/styles__ltr.css | 200 | — | 1 ms |
| 19:43:51.928 | GET | https://www.gstatic.com/recaptcha/releases/Br0hYqpfWeFzYCAXLD4UuCIV/recaptcha__en.js | 200 | — | 4 ms |
| 19:43:51.963 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 289 ms |
| 19:43:52.086 | GET | https://www.google.com/recaptcha/enterprise/webworker.js?hl=en&v=Br0hYqpfWeFzYCAXLD4UuCIV | 200 | — | 123 ms |
| 19:43:52.107 | GET | https://www.gstatic.com/recaptcha/releases/Br0hYqpfWeFzYCAXLD4UuCIV/recaptcha__en.js | 200 | — | 8 ms |
| 19:43:52.124 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:52.219 | POST | https://www.bestbuy.com/streams/v1/consume | 200 | — | 201 ms |
| 19:43:52.238 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 64 ms |
| 19:43:52.240 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 62 ms |
| 19:43:52.243 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 60 ms |
| 19:43:52.245 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 59 ms |
| 19:43:52.248 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 59 ms |
| 19:43:52.252 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 62 ms |
| 19:43:52.255 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 59 ms |
| 19:43:52.296 | GET | https://ep2.adtrafficquality.google/sodar/sodar2/254/runner.html | 200 | — | 161 ms |
| 19:43:52.342 | GET | https://www.bestbuy.com/suggest/v1/fragment/products/www?skuids=6646419,6646420,6601524,6… | 200 | — | 2 ms |
| 19:43:52.536 | POST | https://www.google.com/pagead/form-data/1066288264?gtm=45be65d0v893760023za200zb917936992… | 200 | — | 35 ms |
| 19:43:52.537 | GET | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/1066288264/?random=17790… | 200 | — | 72 ms |
| 19:43:52.537 | POST | https://www.google.com/ccm/form-data/1066288264?gtm=45be65d0v893760023za200zb9179369925zd… | 204 | — | 33 ms |
| 19:43:52.537 | POST | https://www.google.com/ccm/collect?rcb=7&frm=0&en=page_view&dl=https%3A%2F%2Fwww.bestbuy.… | 200 | — | 53 ms |
| 19:43:52.537 | POST | https://www.google.com/rmkt/collect/1066288264/?random=1779047032453&cv=11&fst=1779047032… | 200 | — | 55 ms |
| 19:43:52.537 | GET | https://www.googleadservices.com/pagead/conversion/1066288264/?random=1779047032470&cv=11… | 200 | — | 120 ms |
| 19:43:52.537 | GET | https://www.googleadservices.com/pagead/conversion/1066288264/?random=1779047032473&cv=11… | 200 | — | 119 ms |
| 19:43:52.552 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:52.589 | GET | https://www.google.com/pagead/1p-user-list/1066288264/?random=1779047032453&cv=11&fst=177… | 200 | — | 41 ms |
| 19:43:52.625 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/kDGYzLOQ/d2YKXBFXew4/TD/gwXSZsbmQt | 200 | — | 179 ms |
| 19:43:52.628 | POST | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/1066288264/?random=16026… | 302 | — | 170 ms |
| 19:43:52.628 | POST | https://googleads.g.doubleclick.net/pagead/viewthroughconversion/1066288264/?random=97820… | 302 | — | 1.15 s |
| 19:43:52.647 | GET | https://pagead2.googlesyndication.com/bg/3tA5tCN6kTJSWaFXSefdotmpF1l_dXhQQZ8UmpcdThI.js | 200 | — | 193 ms |
| 19:43:52.754 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:52.799 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:52.800 | GET | https://www.google.com/pagead/1p-conversion/1066288264/?random=1602661847&cv=11&fst=17790… | 200 | — | 50 ms |
| 19:43:52.846 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:52.875 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 65 ms |
| 19:43:52.885 | GET | https://ep2.adtrafficquality.google/generate_204?hxNjkQ | 204 | — | 46 ms |
| 19:43:52.894 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:52.909 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:52.939 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:52.964 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:53.043 | POST | https://www.google.com/recaptcha/enterprise/reload?k=6LeP0dgrAAAAAFn_1X2rBkI8vJKKsU0-LOJO… | 200 | — | 102 ms |
| 19:43:53.147 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 55 ms |
| 19:43:53.199 | POST | https://www.bestbuy.com/cj-recaptcha/v1/submit | 204 | — | 309 ms |
| 19:43:53.217 | POST | https://www.google.com/recaptcha/enterprise/clr?k=6LeP0dgrAAAAAFn_1X2rBkI8vJKKsU0-LOJOsczw | 200 | — | 57 ms |
| 19:43:53.239 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:53.249 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:53.274 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:53.286 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 59 ms |
| 19:43:53.286 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:53.297 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:53.306 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:53.317 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:53.325 | GET | https://www.bestbuy.com/site/canopy/component/pricing/price-change-notification/v1?device… | 200 | — | 345 ms |
| 19:43:53.349 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 53 ms |
| 19:43:53.358 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 50 ms |
| 19:43:53.368 | GET | https://www.bestbuy.com/site/canopy/component/shop/account-menu/v1?businessName=%24(csi.u… | 200 | — | 301 ms |
| 19:43:53.394 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 52 ms |
| 19:43:53.415 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 51 ms |
| 19:43:53.452 | GET | https://ep1.adtrafficquality.google/pagead/sodar?id=sodar2&v=254&t=2&li=afs_1234567890&jk… | 204 | — | 147 ms |
| 19:43:53.459 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 46 ms |
| 19:43:53.484 | GET | https://www.bestbuy.com/site/canopy/component/shop/stips/v1?deviceClass=l&placement=header | 200 | — | 254 ms |
| 19:43:53.525 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 54 ms |
| 19:43:53.582 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 50 ms |
| 19:43:53.599 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:53.603 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:53.611 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:53.618 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 61 ms |
| 19:43:53.618 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:53.624 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:53.639 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:53.650 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:53.653 | GET | https://securepubads.g.doubleclick.net/pagead/managed/dict/m202605140101/gpt | 200 | — | 1 ms |
| 19:43:53.667 | GET | https://assets.bbystatic.com/pricing/price-change-notification/dist/client/client-2bffc37… | 200 | — | <1 ms |
| 19:43:53.668 | GET | https://assets.bbystatic.com/shop/account-menu/dist/client/client-6046ee5d99fb6d1f20129a4… | 200 | — | <1 ms |
| 19:43:53.679 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-vendors-_yarn_cache_gvp-lib-in… | 200 | — | 1 ms |
| 19:43:53.679 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-vendors-_yarn_cache_symbol-obs… | 200 | — | 1 ms |
| 19:43:53.679 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-vendors-_yarn_cache_redux-npm-… | 200 | — | 1 ms |
| 19:43:53.701 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/137-6046ee5d99fb6d… | 200 | — | 2 ms |
| 19:43:53.701 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/platformContainer.2022.11.10.1.js | 200 | — | 2 ms |
| 19:43:53.701 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/232-6046ee5d99fb6d… | 200 | — | 3 ms |
| 19:43:53.723 | GET | https://www.bestbuy.com/~assets/bby/_com/pricing/price-change-notification/dist/client/12… | 200 | — | 2 ms |
| 19:43:53.724 | GET | https://www.bestbuy.com/~assets/bby/_com/pricing/price-change-notification/dist/client/55… | 200 | — | 1 ms |
| 19:43:53.724 | GET | https://www.bestbuy.com/~assets/bby/_com/pricing/price-change-notification/dist/client/55… | 200 | — | 2 ms |
| 19:43:53.724 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-vendors-_yarn___virtual___redu… | 200 | — | 2 ms |
| 19:43:53.724 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-vendors-_yarn_cache_prop-types… | 200 | — | 1 ms |
| 19:43:53.724 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-vendors-_yarn_cache_gvp-lib-fa… | 200 | — | 2 ms |
| 19:43:53.724 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-vendors-_yarn_cache_falcor-npm… | 200 | — | 2 ms |
| 19:43:53.724 | GET | https://www.bestbuy.com/~assets/bby/_com/brix/7.11.35/js/6082.js | 200 | — | 1 ms |
| 19:43:53.724 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-vendors-_yarn_cache_lodash-npm… | 200 | — | 2 ms |
| 19:43:53.724 | GET | https://www.bestbuy.com/~assets/bby/_com/brix/7.11.35/js/8809.js | 200 | — | 2 ms |
| 19:43:53.736 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 57 ms |
| 19:43:53.744 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-2022-vendors-_yarn_cache_react… | 200 | — | 1 ms |
| 19:43:53.744 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-2022-vendors-_yarn___virtual__… | 200 | — | 2 ms |
| 19:43:53.744 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-2022-vendors-_yarn___virtual__… | 200 | — | 2 ms |
| 19:43:53.775 | GET | https://www.google.com/pagead/1p-conversion/1066288264/?random=978209080&cv=11&fst=177904… | 200 | — | 41 ms |
| 19:43:53.809 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/stips/dist/client/client-8d41dfb3ae61238f1c… | 200 | — | 1 ms |
| 19:43:53.830 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/client-button.css | 200 | — | 4 ms |
| 19:43:53.830 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/251-6046ee5d99fb6d… | 200 | — | 4 ms |
| 19:43:53.830 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/684-6046ee5d99fb6d… | 200 | — | 5 ms |
| 19:43:53.830 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-vendors-_yarn_cache_object-ass… | 200 | — | 5 ms |
| 19:43:53.830 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-vendors-_yarn_cache_react-npm-… | 200 | — | 4 ms |
| 19:43:53.830 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/client-button-6046… | 200 | — | 5 ms |
| 19:43:53.830 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/882-6046ee5d99fb6d… | 200 | — | 9 ms |
| 19:43:53.830 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/831-6046ee5d99fb6d… | 200 | — | 10 ms |
| 19:43:53.831 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-lib-appear_dist_main_umd_js-26… | 200 | — | 4 ms |
| 19:43:53.831 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-_yarn___virtual___gvp-lib-embe… | 200 | — | 5 ms |
| 19:43:53.853 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/stips/dist/client/109-8d41dfb3ae61238f1c871… | 200 | — | 1 ms |
| 19:43:53.972 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 54 ms |
| 19:43:54.032 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 248 ms |
| 19:43:54.033 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 51 ms |
| 19:43:54.037 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 51 ms |
| 19:43:54.038 | POST | https://www.bestbuy.com/cart/api/v1/addToCart | 200 | — | 724 ms |
| 19:43:54.062 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=1&c=2493&i=5fvhov&p=privacy_prod&… | 204 | — | 57 ms |
| 19:43:54.127 | GET | https://www.bestbuy.com/api/tcfb/model.json?paths=%5B%5B%22shop%22%2C%22scds%22%2C%22v2%2… | 200 | — | 1 ms |
| 19:43:54.148 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 64 ms |
| 19:43:54.222 | POST | https://www.google.com/recaptcha/enterprise/reload?k=6LeP0dgrAAAAAFn_1X2rBkI8vJKKsU0-LOJO… | 200 | — | 119 ms |
| 19:43:54.265 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 60 ms |
| 19:43:54.366 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 51 ms |
| 19:43:54.369 | POST | https://www.bestbuy.com/cj-recaptcha/v1/submit | 204 | — | 260 ms |
| 19:43:54.380 | POST | https://www.google.com/recaptcha/enterprise/clr?k=6LeP0dgrAAAAAFn_1X2rBkI8vJKKsU0-LOJOsczw | 200 | — | 51 ms |
| 19:43:54.385 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:54.393 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:54.399 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:54.405 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 70 ms |
| 19:43:54.405 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:54.412 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:54.423 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:54.479 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 50 ms |
| 19:43:54.513 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 47 ms |
| 19:43:54.540 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 57 ms |
| 19:43:54.553 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 57 ms |
| 19:43:54.553 | GET | https://www.bestbuy.com/site/canopy/component/shop/interruptions-manager/v1 | 200 | — | 199 ms |
| 19:43:54.585 | GET | https://pisces.bbystatic.com/BestBuy_US/Gallery/bby_image_coming_soon-144342.jpg;maxHeigh… | 200 | — | 110 ms |
| 19:43:54.598 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 50 ms |
| 19:43:54.601 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 56 ms |
| 19:43:54.605 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 58 ms |
| 19:43:54.607 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 62 ms |
| 19:43:54.664 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:54.758 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/interruptions-manager/dist/client/client-0e… | 200 | — | 1 ms |
| 19:43:54.788 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 228 ms |
| 19:43:54.817 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:54.818 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/interruptions-manager/dist/client/791-0e092… | 200 | — | 2 ms |
| 19:43:54.818 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/interruptions-manager/dist/client/542-0e092… | 200 | — | 1 ms |
| 19:43:54.838 | POST | https://www.bestbuy.com/streams/v1/consume | 200 | — | 276 ms |
| 19:43:54.902 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 61 ms |
| 19:43:55.005 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:55.015 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:55.021 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:55.162 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 249 ms |
| 19:43:55.213 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 56 ms |
| 19:43:55.240 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:55.250 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:55.392 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 48 ms |
| 19:43:55.404 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 51 ms |
| 19:43:55.405 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 57 ms |
| 19:43:55.430 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:43:55.438 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 356 ms |
| 19:43:55.458 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 70 ms |
| 19:43:55.459 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 71 ms |
| 19:43:55.531 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/kDGYzLOQ/d2YKXBFXew4/TD/gwXSZsbmQt | 200 | — | 130 ms |
| 19:43:56.843 | POST | https://www.bestbuy.com/services/conversation/web/api/v1/unified-chat/logger?appVersion=2… | 200 | — | 330 ms |
| 19:43:58.986 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 592 ms |
| 19:43:58.994 | GET | https://www.bestbuy.com/cart | 200 | — | 984 ms |
| 19:43:59.000 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 355 ms |
| 19:43:59.071 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=2&c=2493&i=5fvhov&p=privacy_prod&… | 204 | — | 55 ms |
| 19:43:59.992 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | -1 | — | <1 ms |
| 19:44:00.009 | GET | https://www.bestbuy.com/~assets/bby/_com/bestbuy/lib-mf-assets/2.1.2/dist/main.js | 200 | — | 1 ms |
| 19:44:00.009 | GET | https://nexus.ensighten.com/bestbuy/privacy_init/Bootstrap.js | 200 | — | 45 ms |
| 19:44:00.009 | GET | https://www.bestbuy.com/~assets/bby/_com/brix-styles/1.76.7/brix-styles-brix-web.css | 200 | — | 94 ms |
| 19:44:00.009 | GET | https://www.bestbuy.com/~assets/bby/_com/lodash-v4/4.17.21/dist/lodash.min.js | 200 | — | 108 ms |
| 19:44:00.009 | GET | https://www.bestbuy.com/~assets/bby/_com/lodash/3.6.0/dist/lodash.min.js | 200 | — | 107 ms |
| 19:44:00.009 | GET | https://www.bestbuy.com/~assets/bby/_com/cacheable-gvp-11be6403c8a50adefb4a68bdb5bdf1ba.m… | 200 | — | 108 ms |
| 19:44:00.009 | GET | https://www.bestbuy.com/~assets/bby/_com/legacy-80e96c542168b4a82a78e485b2a038a2.min.js | 200 | — | 114 ms |
| 19:44:00.009 | GET | https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js | 200 | — | 121 ms |
| 19:44:00.009 | GET | https://www.bestbuy.com/~assets/bby/_com/staging-fad56d9ad0f78ba1e7124a8ba5213507.min.js | 200 | — | 140 ms |
| 19:44:00.010 | GET | https://www.bestbuy.com/~assets/bby/_com/deo-client-script.js | 200 | — | 1 ms |
| 19:44:00.010 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/3818-f8a2f130f510dc5… | 200 | — | 1 ms |
| 19:44:00.010 | GET | https://www.bestbuy.com/~assets/bby/_com/runtime.cart.bundle-8b9ce07d8fcbb3fdf636142ecd89… | 200 | — | 129 ms |
| 19:44:00.010 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/platformContainerOrchestrationProxy.1… | 200 | — | 140 ms |
| 19:44:00.010 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/header/dist/client/client-e53783978238fb45c… | 200 | — | 153 ms |
| 19:44:00.010 | GET | https://www.bestbuy.com/~assets/bby/_com/main.cart.bundle-8b9ce07d8fcbb3fdf636142ecd896ad… | 200 | — | 153 ms |
| 19:44:00.010 | GET | https://www.bestbuy.com/~assets/bby/_com/brix/7.5.0/js/brixRemoteEntry.js | 200 | — | 153 ms |
| 19:44:00.010 | GET | https://www.bestbuy.com/~assets/bby/_com/vendors.cart.bundle-8b9ce07d8fcbb3fdf636142ecd89… | 200 | — | 154 ms |
| 19:44:00.010 | GET | https://www.bestbuy.com/~assets/bby/_com/shared-core.cart.bundle-0364067adf36a97cc87f8156… | 200 | — | 180 ms |
| 19:44:00.011 | GET | https://assets.bbystatic.com/shop/account-menu/dist/client/client-6046ee5d99fb6d1f20129a4… | 200 | — | 1 ms |
| 19:44:00.011 | GET | https://assets.bbystatic.com/pricing/price-change-notification/dist/client/client-2bffc37… | 200 | — | 1 ms |
| 19:44:00.011 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/interruptions-manager/dist/client/client-0e… | 200 | — | 1 ms |
| 19:44:00.011 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/evoc-talk_to_us-v1-0… | 200 | — | 169 ms |
| 19:44:00.012 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/stips/dist/client/client-8d41dfb3ae61238f1c… | 200 | — | 1 ms |
| 19:44:00.012 | GET | https://www.bestbuy.com/~assets/bby/_com/@ds/unified-chat/dist/javascript/unified-chat-in… | 200 | — | 1 ms |
| 19:44:00.012 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/footer/dist/client/client-bd8b196f8ef2633b0… | 200 | — | 133 ms |
| 19:44:00.012 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/location-persistence/dist/client/client-a9d… | 200 | — | 179 ms |
| 19:44:00.012 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/lib-dai/dist/client/client-089bbe3cbb4e8848… | 200 | — | 180 ms |
| 19:44:00.012 | GET | https://assets.bbystatic.com/deo-lss-activation.js | 200 | — | 180 ms |
| 19:44:00.012 | GET | https://www.bestbuy.com/~assets/bby/_com/cret/appgrowth-smartbanner/dist/client/client-98… | 200 | — | 199 ms |
| 19:44:00.012 | GET | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 200 | — | 205 ms |
| 19:44:00.012 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/header/dist/client/client-a28fb014640ca3fd1… | 200 | — | 258 ms |
| 19:44:00.012 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/footer/dist/client/client-b33d35535b0df758b… | 200 | — | 268 ms |
| 19:44:00.013 | GET | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/kDGYzLOQ/d2YKXBFXew4/TD/gwXSZsbmQt?v… | 200 | — | 356 ms |
| 19:44:00.102 | GET | https://nexus.ensighten.com/bestbuy/privacy_prod_cm_copy/Bootstrap.js | 200 | — | 118 ms |
| 19:44:00.176 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/platformContainer.11.3.3.js | 200 | — | 188 ms |
| 19:44:00.191 | GET | https://www.bestbuy.com/~assets/bby/_com/brix-styles/1.76.7/2831c370bcd5d8865105.woff2 | 200 | — | 172 ms |
| 19:44:00.191 | GET | https://www.bestbuy.com/~assets/bby/_com/brix-styles/1.76.7/37f8017947c264b8389f.woff2 | 200 | — | 201 ms |
| 19:44:00.191 | GET | https://www.bestbuy.com/~assets/bby/_com/brix-styles/1.76.7/60fb346d82490233081f.woff2 | 200 | — | 202 ms |
| 19:44:00.214 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/deo-experiment-activations | 200 | — | 569 ms |
| 19:44:00.250 | GET | https://pisces.bbystatic.com/image2/vector/BestBuy_US/dam/X-bd003ff5-a027-4542-9c98-1d568… | 200 | — | 107 ms |
| 19:44:00.250 | GET | https://pisces.bbystatic.com/image2/vector/BestBuy_US/dam/AppYouTube-c823f6d3-8dcb-4964-9… | 200 | — | 107 ms |
| 19:44:00.250 | GET | https://pisces.bbystatic.com/image2/vector/BestBuy_US/dam/AppInstagram-ea334c57-1040-4c6a… | 200 | — | 108 ms |
| 19:44:00.250 | GET | https://pisces.bbystatic.com/image2/vector/BestBuy_US/dam/AppTikTok-4ad73591-e0c4-4848-a7… | 200 | — | 108 ms |
| 19:44:00.250 | GET | https://pisces.bbystatic.com/image2/vector/BestBuy_US/dam/AppPinterest-8bc14c43-a0c9-415f… | 200 | — | 136 ms |
| 19:44:00.250 | GET | https://pisces.bbystatic.com/image2/vector/BestBuy_US/dam/AppFacebook-6587dc59-5c2c-41f5-… | 200 | — | 181 ms |
| 19:44:00.299 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 333 ms |
| 19:44:00.302 | GET | https://www.bestbuy.com/~assets/bby/_com/@ds/unified-chat/dist/javascript/unified-chat-in… | 200 | — | 2 ms |
| 19:44:00.303 | GET | https://www.bestbuy.com/~assets/bby/_com/@ds/unified-chat/dist/javascript/unified-chat-in… | 200 | — | 2 ms |
| 19:44:00.303 | GET | https://www.bestbuy.com/~assets/bby/_com/@ds/unified-chat/dist/javascript/unified-chat-in… | 200 | — | 3 ms |
| 19:44:00.304 | GET | https://www.bestbuy.com/~assets/bby/_com/@ds/unified-chat/dist/javascript/unified-chat-in… | 200 | — | 2 ms |
| 19:44:00.357 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/cj-page-visits | 200 | — | 346 ms |
| 19:44:00.403 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/232-6046ee5d99fb6d… | 200 | — | 1 ms |
| 19:44:00.403 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/8216-ceb7eb6f1a3c8c7… | 200 | — | 1 ms |
| 19:44:00.404 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/137-6046ee5d99fb6d… | 200 | — | 1 ms |
| 19:44:00.404 | GET | https://www.bestbuy.com/~assets/bby/_com/pricing/price-change-notification/dist/client/12… | 200 | — | 1 ms |
| 19:44:00.404 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/platformContainer.2022.11.3.3.js | 200 | — | 99 ms |
| 19:44:00.405 | GET | https://www.bestbuy.com/~assets/bby/_com/pricing/price-change-notification/dist/client/55… | 200 | — | 1 ms |
| 19:44:00.405 | GET | https://www.bestbuy.com/~assets/bby/_com/pricing/price-change-notification/dist/client/55… | 200 | — | 1 ms |
| 19:44:00.405 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/interruptions-manager/dist/client/791-0e092… | 200 | — | 1 ms |
| 19:44:00.405 | GET | https://www.bestbuy.com/~assets/bby/_com/brix/7.5.0/js/2509.js | 200 | — | 139 ms |
| 19:44:00.405 | GET | https://www.bestbuy.com/~assets/bby/_com/brix/7.5.0/js/1778.js | 200 | — | 152 ms |
| 19:44:00.406 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/interruptions-manager/dist/client/542-0e092… | 200 | — | 1 ms |
| 19:44:00.406 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/stips/dist/client/109-8d41dfb3ae61238f1c871… | 200 | — | 1 ms |
| 19:44:00.406 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/header/dist/client/9691-a28fb014640ca3fd163… | 200 | — | 145 ms |
| 19:44:00.406 | GET | https://www.bestbuy.com/~assets/bby/_com/date-fns.cart.bundle-e210fa3838437ba42cc98dddbe2… | 200 | — | 136 ms |
| 19:44:00.406 | GET | https://www.bestbuy.com/~assets/bby/_com/brix-styles.cart.bundle-a8b65e8059d6a28c9a4441b3… | 200 | — | 149 ms |
| 19:44:00.406 | GET | https://www.bestbuy.com/~assets/bby/_com/brix-icons.cart.bundle-1aaa9f2bfe5e45e3f4822ca5c… | 200 | — | 139 ms |
| 19:44:00.406 | GET | https://www.bestbuy.com/~assets/bby/_com/cret/appgrowth-smartbanner/dist/client/983-982fe… | 200 | — | 173 ms |
| 19:44:00.406 | GET | https://www.bestbuy.com/~assets/bby/_com/graphql.cart.bundle-3c662449af45155a6283eb9a0a59… | 200 | — | 157 ms |
| 19:44:00.406 | GET | https://www.bestbuy.com/~assets/bby/_com/membership-platform.cart.bundle-c6d19cc6f36f3c37… | 200 | — | 188 ms |
| 19:44:00.407 | GET | https://www.bestbuy.com/~assets/bby/_com/vendors-node_modules_bestbuy_brix_dist_esm_icon-… | 200 | — | 150 ms |
| 19:44:00.407 | GET | https://www.bestbuy.com/~assets/bby/_com/ugc-web.cart.bundle-18240671b8c1262de0cb41980403… | 200 | — | 155 ms |
| 19:44:00.407 | GET | https://www.bestbuy.com/~assets/bby/_com/vendors-node_modules_bestbuy_brix_dist_esm_divid… | 200 | — | 150 ms |
| 19:44:00.407 | GET | https://www.bestbuy.com/~assets/bby/_com/vendors-node_modules_bestbuy_brix_dist_esm_butto… | 200 | — | 150 ms |
| 19:44:00.407 | GET | https://www.bestbuy.com/~assets/bby/_com/vendors-node_modules_bestbuy_brix_dist_esm_icon_… | 200 | — | 172 ms |
| 19:44:00.407 | GET | https://www.bestbuy.com/~assets/bby/_com/vendors-node_modules_bestbuy_brix_dist_esm_statu… | 200 | — | 173 ms |
| 19:44:00.407 | GET | https://www.bestbuy.com/~assets/bby/_com/vendors-node_modules_usehooks-ts_dist_esm_index_… | 200 | — | 172 ms |
| 19:44:00.407 | GET | https://www.bestbuy.com/~assets/bby/_com/vendors-node_modules_bestbuy_brix_dist_esm_modal… | 200 | — | 197 ms |
| 19:44:00.407 | GET | https://www.bestbuy.com/~assets/bby/_com/vendors-node_modules_bestbuy_brix_dist_esm_text-… | 200 | — | 198 ms |
| 19:44:00.408 | GET | https://www.bestbuy.com/~assets/bby/_com/vendors-node_modules_bestbuy_brix_dist_esm_radio… | 200 | — | 176 ms |
| 19:44:00.408 | GET | https://www.bestbuy.com/~assets/bby/_com/vendors-node_modules_bestbuy_brix_dist_esm_skele… | 200 | — | 174 ms |
| 19:44:00.408 | GET | https://www.bestbuy.com/~assets/bby/_com/vendors-node_modules_styled-components_dist_styl… | 200 | — | 174 ms |
| 19:44:00.408 | GET | https://www.bestbuy.com/~assets/bby/_com/vendors-node_modules_bestbuy_buy-now-pay-later_d… | 200 | — | 176 ms |
| 19:44:00.408 | GET | https://www.bestbuy.com/~assets/bby/_com/vendors-node_modules_bestbuy_brix_dist_esm_alert… | 200 | — | 178 ms |
| 19:44:00.408 | GET | https://www.bestbuy.com/~assets/bby/_com/vendors-node_modules_apollo_client_dev_index_js.… | 200 | — | 176 ms |
| 19:44:00.408 | GET | https://www.bestbuy.com/~assets/bby/_com/vendors-node_modules_bestbuy_brix_dist_esm_check… | 200 | — | 175 ms |
| 19:44:00.408 | GET | https://www.bestbuy.com/~assets/bby/_com/vendors-node_modules_bestbuy_brix_dist_esm_image… | 200 | — | 176 ms |
| 19:44:00.408 | GET | https://www.bestbuy.com/~assets/bby/_com/vendors-node_modules_bestbuy_brix_dist_esm_selec… | 200 | — | 198 ms |
| 19:44:00.409 | GET | https://www.bestbuy.com/~assets/bby/_com/src_my-bby-membership_helpers_analytics_js-src_m… | 200 | — | 198 ms |
| 19:44:00.409 | GET | https://www.bestbuy.com/~assets/bby/_com/node_modules_bestbuy_brix-icons_react_sync_recur… | 200 | — | 199 ms |
| 19:44:00.409 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/location-persistence/dist/client/476-a9d4fc… | 200 | — | 198 ms |
| 19:44:00.409 | GET | https://www.bestbuy.com/~assets/bby/_com/vendors-node_modules_best-buy_currency-helpers_l… | 200 | — | 203 ms |
| 19:44:00.409 | GET | https://www.bestbuy.com/~assets/bby/_com/vendors-node_modules_bestbuy_analytics-actions_e… | 200 | — | 204 ms |
| 19:44:00.409 | GET | https://www.bestbuy.com/~assets/bby/_com/vendors-node_modules_bby_dry_dist_dry_es_js-node… | 200 | — | 258 ms |
| 19:44:00.409 | GET | https://www.bestbuy.com/~assets/bby/_com/vendors-node_modules_best-buy_trade-in-calculati… | 200 | — | 339 ms |
| 19:44:00.409 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/lib-dai/dist/client/323-089bbe3cbb4e88488ee… | 200 | — | 333 ms |
| 19:44:00.409 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/footer/dist/client/650-b33d35535b0df758bb44… | 200 | — | 331 ms |
| 19:44:00.409 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/lib-dai/dist/client/826-089bbe3cbb4e88488ee… | 200 | — | 335 ms |
| 19:44:00.409 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/footer/dist/client/407-b33d35535b0df758bb44… | 200 | — | 339 ms |
| 19:44:00.482 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=0&c=2493&i=4ykco5&p=privacy_prod_… | 204 | — | 104 ms |
| 19:44:00.484 | GET | https://a4091a3a2309.cdn4.forter.com/sn/a4091a3a2309/script.js | 200 | — | 426 ms |
| 19:44:00.504 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/9495-ceb7eb6f1a3c8c7… | 200 | — | 2 ms |
| 19:44:00.504 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/3696-ceb7eb6f1a3c8c7… | 200 | — | 1 ms |
| 19:44:00.504 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/1830-ceb7eb6f1a3c8c7… | 200 | — | 1 ms |
| 19:44:00.504 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/333-ceb7eb6f1a3c8c77… | 200 | — | 2 ms |
| 19:44:00.504 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/8441-ceb7eb6f1a3c8c7… | 200 | — | 2 ms |
| 19:44:00.504 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/7243-ceb7eb6f1a3c8c7… | 200 | — | 2 ms |
| 19:44:00.504 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/8325-ceb7eb6f1a3c8c7… | 200 | — | 1 ms |
| 19:44:00.517 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-2022-vendors-_yarn_cache_react… | 200 | — | 1 ms |
| 19:44:00.517 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-2022-vendors-_yarn___virtual__… | 200 | — | 1 ms |
| 19:44:00.517 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-2022-vendors-_yarn___virtual__… | 200 | — | 1 ms |
| 19:44:00.519 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/cjc-page-requests | 200 | — | 262 ms |
| 19:44:00.563 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/882-6046ee5d99fb6d… | 200 | — | 1 ms |
| 19:44:00.563 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/831-6046ee5d99fb6d… | 200 | — | 1 ms |
| 19:44:00.564 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/251-6046ee5d99fb6d… | 200 | — | 1 ms |
| 19:44:00.564 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/684-6046ee5d99fb6d… | 200 | — | 1 ms |
| 19:44:00.564 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/client-button.css | 200 | — | 1 ms |
| 19:44:00.564 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/account-menu/dist/client/client-button-6046… | 200 | — | 1 ms |
| 19:44:00.677 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/5090-ceb7eb6f1a3c8c7… | 200 | — | 13 ms |
| 19:44:00.677 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/3945-ceb7eb6f1a3c8c7… | 200 | — | 14 ms |
| 19:44:00.678 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/814-ceb7eb6f1a3c8c77… | 200 | — | 13 ms |
| 19:44:00.679 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/7754-ceb7eb6f1a3c8c7… | 200 | — | 13 ms |
| 19:44:00.698 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/header/dist/client/client-lv-a28fb014640ca3… | 200 | — | 127 ms |
| 19:44:00.698 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/header/dist/client/8639-a28fb014640ca3fd163… | 200 | — | 157 ms |
| 19:44:00.760 | GET | https://www.bestbuy.com/api/tcfb/model.json?paths=%5B%5B%22shop%22%2C%22scds%22%2C%22v2%2… | 200 | — | 6 ms |
| 19:44:01.516 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 62 ms |
| 19:44:01.517 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/@bestbuy/bby-debug/dist/client/bby-debug-fe… | 200 | — | <1 ms |
| 19:44:01.517 | GET | https://www.bestbuy.com/pcn-api/basket?context=CART&vt=11d61959-64a5-4174-a3ae-470acdd293… | 200 | — | 399 ms |
| 19:44:01.539 | GET | https://www.bestbuy.com/~assets/bby/_com/2b3b9afcb5b5002401e901472f949ea8.woff2 | 200 | — | 142 ms |
| 19:44:01.539 | GET | https://www.bestbuy.com/~assets/bby/_com/49847924d9a100547f19e151a55043c3.woff2 | 200 | — | 143 ms |
| 19:44:01.539 | GET | https://www.bestbuy.com/~assets/bby/_com/07d84cac00134ce2f4b0727e3f0486b8.woff2 | 200 | — | 147 ms |
| 19:44:01.748 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:44:01.748 | GET | https://www.bestbuy.com/site/canopy/component/shop/blue-assist/v1 | 200 | — | 175 ms |
| 19:44:01.749 | GET | https://www.bestbuy.com/cart/json?isDeviceApplePayEligible=false | 200 | — | 1.15 s |
| 19:44:02.053 | GET | blob:https://www.bestbuy.com/6f421eb7-ca0b-4122-8b00-8dfe391a4327 | 200 OK | — | 124 ms |
| 19:44:02.144 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/@bestbuy/bby-debug/dist/client/bby-debug-85… | 200 | — | 2 ms |
| 19:44:02.173 | GET | https://www.bestbuy.com/site/canopy/component/shop/location-persistence/v1?_lazyHydrate=f… | 200 | — | 430 ms |
| 19:44:02.667 | GET | https://www.bestbuy.com/~assets/bby/_img/int/plsvgdef-frontend/svg/Question_Line_Sm.svg | 200 | — | 2 ms |
| 19:44:02.667 | GET | https://www.bestbuy.com/~assets/bby/_img/int/plsvgdef-frontend/svg/Shipping_Line_Sm.svg | 200 | — | 3 ms |
| 19:44:02.667 | GET | https://www.bestbuy.com/~assets/bby/_img/int/plsvgdef-frontend/svg/Delivery_Line_Sm.svg | 200 | — | 3 ms |
| 19:44:02.667 | GET | https://www.bestbuy.com/~assets/bby/_img/int/plsvgdef-frontend/svg/ReturnPolicy_Line_Sm.s… | 200 | — | 3 ms |
| 19:44:02.668 | GET | https://www.bestbuy.com/~assets/bby/_img/int/plsvgdef-frontend/svg/PriceMatchGuarantee_Li… | 200 | — | 3 ms |
| 19:44:02.668 | GET | https://www.bestbuy.com/~assets/bby/_img/int/plsvgdef-frontend/svg/MobileApp_Line_Sm.svg | 200 | — | 3 ms |
| 19:44:02.716 | GET | blob:https://www.bestbuy.com/881f0a35-5f28-449b-b3a6-0a684d7b1384 | 200 OK | — | 53 ms |
| 19:44:02.735 | GET | blob:https://www.bestbuy.com/eb39c463-abb7-4efc-b435-34f5613c609d | 200 OK | — | 104 ms |
| 19:44:02.744 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/blue-assist/dist/client/client-1868d6d83328… | 200 | — | 135 ms |
| 19:44:02.752 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/blue-assist/dist/client/client-ba310cf51233… | 200 | — | 127 ms |
| 19:44:02.799 | GET | blob:https://www.bestbuy.com/3ef11fc0-d341-4e26-b25c-14d94b0ea678 | -1 | — | <1 ms |
| 19:44:02.805 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/header/dist/client/9167-a28fb014640ca3fd163… | 200 | — | 111 ms |
| 19:44:02.805 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/header/dist/client/5863-a28fb014640ca3fd163… | 200 | — | 137 ms |
| 19:44:02.809 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:44:02.811 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:44:02.814 | GET | https://cdn0.forter.com/a4091a3a2309/b36b7e0314ba4bb5a2979e1b72285963/prop.json?_=1779047… | 200 OK | — | 329 ms |
| 19:44:02.841 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/analyticsInit-aa713fca754a9e167… | 200 | — | 133 ms |
| 19:44:02.867 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=2&c=2493&i=4ykco5&p=privacy_prod_… | 204 | — | 58 ms |
| 19:44:02.867 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=1&c=2493&i=4ykco5&p=privacy_prod_… | 204 | — | 61 ms |
| 19:44:02.867 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=3&c=2493&i=4ykco5&p=privacy_prod_… | 204 | — | 66 ms |
| 19:44:02.894 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/blue-assist/dist/client/8580-1868d6d8332841… | 200 | — | 136 ms |
| 19:44:02.894 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/blue-assist/dist/client/7163-1868d6d8332841… | 200 | — | 139 ms |
| 19:44:02.899 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/header/dist/client/2192-a28fb014640ca3fd163… | 200 | — | 93 ms |
| 19:44:02.899 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/header/dist/client/7448-a28fb014640ca3fd163… | 200 | — | 135 ms |
| 19:44:02.900 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/header/dist/client/2526-a28fb014640ca3fd163… | 200 | — | 137 ms |
| 19:44:02.900 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/header/dist/client/3773-a28fb014640ca3fd163… | 200 | — | 138 ms |
| 19:44:02.900 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/header/dist/client/393-a28fb014640ca3fd163c… | 200 | — | 141 ms |
| 19:44:02.900 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/header/dist/client/upa-visitor-optimization… | 200 | — | 169 ms |
| 19:44:03.022 | GET | https://www.bestbuy.com/lux.js | 200 | — | 1 ms |
| 19:44:03.022 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 49 ms |
| 19:44:03.022 | GET | https://www.bestbuy.com/~assets/bby/_js/ext/bbydyn/dyn_digital.js | 200 | — | 139 ms |
| 19:44:03.022 | GET | https://tmx.bestbuy.com/lwnkmfadp8b0yeu1.js?1iyeh8u1a3541ndr=ummqowa2&mcmxmhoqxffrgkk3=2d… | 200 OK | — | 490 ms |
| 19:44:03.023 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 57 ms |
| 19:44:03.023 | GET | https://www.bestbuy.com/~assets/bby/_img/int/plsvgdef-frontend/svg/TradeIn_Line_Sm.svg | 200 | — | 132 ms |
| 19:44:03.023 | GET | https://www.bestbuy.com/~assets/bby/_img/int/plsvgdef-frontend/svg/Cart_Filled_Line_Sm.svg | 200 | — | 132 ms |
| 19:44:03.023 | GET | https://www.bestbuy.com/priceview/v1/price/content?configurationOnly | 200 | — | 252 ms |
| 19:44:03.023 | GET | https://www.bestbuy.com/site/canopy/component/shop/ninja/v1?locale=en-US&pageType=cart | 200 | — | 324 ms |
| 19:44:03.023 | GET | https://www.bestbuy.com/site/canopy/component/pricing/price/v1?context=cart-geek-squad-pr… | 200 | — | 468 ms |
| 19:44:03.023 | GET | https://www.bestbuy.com/site/canopy/component/shop/your-activity-in-cart/v1?deviceClass=l | 200 | — | 608 ms |
| 19:44:03.049 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 55 ms |
| 19:44:03.050 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:44:03.050 | GET | https://www.bestbuy.com/~assets/bby/_img/int/plsvgdef-frontend/svg/GiftIdeas_Line_Sm.svg | 200 | — | 124 ms |
| 19:44:03.051 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 60 ms |
| 19:44:03.052 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 59 ms |
| 19:44:03.084 | GET | https://www.bestbuy.com/~assets/bby/_com/brix-styles/1.76.7/bcd69da2f04aa7a01998.svg | 200 | — | 208 ms |
| 19:44:03.084 | GET | https://www.bestbuy.com/~assets/bby/_com/9d3c7ff709ea1bdc72062421bbbffc8c.woff2 | 200 | — | 206 ms |
| 19:44:03.084 | GET | https://pisces.bbystatic.com/image2//BestBuy_US/images/products/e44a0a67-7842-4cd6-8b23-1… | 200 | — | 207 ms |
| 19:44:03.084 | GET | https://www.bestbuy.com/~assets/bby/_com/822180b5b8d972bef6d0d730fface1e3.woff2 | 200 | — | 260 ms |
| 19:44:03.100 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 54 ms |
| 19:44:03.116 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 361 ms |
| 19:44:03.125 | GET | https://www.bestbuy.com/pricing/v1/price/item?salesChannel=LargeView&visitorId=11d61959-6… | 200 | — | 600 ms |
| 19:44:03.125 | GET | https://www.bestbuy.com/pricing/v1/price/item?salesChannel=LargeView&visitorId=11d61959-6… | 200 | — | 686 ms |
| 19:44:03.162 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/81-2c54adfeb00efd510480.… | 200 | — | 133 ms |
| 19:44:03.162 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/9557-e656009191eb0108a30… | 200 | — | 134 ms |
| 19:44:03.267 | GET | https://cdn0.forter.com/a4091a3a2309/b36b7e0314ba4bb5a2979e1b72285963/prop.json?_=1779047… | 200 OK | — | 129 ms |
| 19:44:03.282 | GET | https://www.bestbuy.com/api/tcfb/model.json?paths=%5B%5B%22shop%22%2C%22magellan%22%2C%22… | 200 | — | 762 ms |
| 19:44:03.284 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:44:03.292 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 54 ms |
| 19:44:03.294 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 51 ms |
| 19:44:03.295 | POST | https://b36b7e0314ba4bb5a2979e1b72285963-a4091a3a2309.cdn.forter.com/prop.json | 200 OK | — | 532 ms |
| 19:44:03.304 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:44:03.309 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 50 ms |
| 19:44:03.324 | GET | https://www.bestbuy.com/offers/completeTheOffer?skuId=6646419&maxSkus=12&maxOffers=2&cust… | 200 | — | 555 ms |
| 19:44:03.355 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/sandbox-index-26.16.2.html?pare… | 200 | — | 331 ms |
| 19:44:03.363 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/customer-journal-d87e751… | 200 | — | 119 ms |
| 19:44:03.432 | GET | https://www.bestbuy.com/api/tcfb/model.json?paths=%5B%5B%22shop%22%2C%22magellan%22%2C%22… | 200 | — | 620 ms |
| 19:44:03.433 | GET | https://assets.bbystatic.com/shop/ninja/dist/client/shop-ninja-v1-1_1_126_remote_entry.js | 200 | — | 211 ms |
| 19:44:03.433 | GET | https://www.bestbuy.com/~assets/bby/_com/popup-ad.js | 200 | — | 253 ms |
| 19:44:03.434 | GET | https://cdn0.forter.com/a4091a3a2309/b36b7e0314ba4bb5a2979e1b72285963/prop.json?_=1779047… | 200 OK | — | 151 ms |
| 19:44:03.457 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:44:03.500 | GET | https://assets.bbystatic.com/pricing/price/dist/client/client-28cf7995cce8475efca5412f998… | 200 | — | 277 ms |
| 19:44:03.506 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/cj-digital-schema1-2faec… | 200 | — | 1 ms |
| 19:44:03.516 | GET | https://assets.bbystatic.com/pricing/price/dist/client/client-2565c4d4b2cd87997213338fd34… | 200 | — | 132 ms |
| 19:44:03.518 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 59 ms |
| 19:44:03.544 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 372 ms |
| 19:44:03.567 | GET | https://www.bestbuy.com/site/canopy/component/shop/location-tooltip/v1?deviceClass=l&shou… | 200 | — | 719 ms |
| 19:44:03.587 | POST | https://cdn0.forter.com/a4091a3a2309/b36b7e0314ba4bb5a2979e1b72285963/wpt.json | 200 OK | — | 97 ms |
| 19:44:03.619 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/your-activity-in-cart/dist/client/shop-your… | 200 | — | 122 ms |
| 19:44:03.622 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 52 ms |
| 19:44:03.650 | GET | https://assets.bbystatic.com/shop/ninja/dist/client/216-f74cf1689b8658af3ff6ce82df2e52d9.… | 200 | — | 91 ms |
| 19:44:03.659 | POST | https://www.bestbuy.com/log-events | 200 | — | 379 ms |
| 19:44:03.692 | GET | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 200 | — | 211 ms |
| 19:44:03.692 | GET | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/kDGYzLOQ/d2YKXBFXew4/TD/gwXSZsbmQt?v… | 200 | — | 213 ms |
| 19:44:03.751 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/ninja/dist/client/884-f74cf1689b8658af3ff6c… | 200 | — | 159 ms |
| 19:44:03.752 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/ninja/dist/client/688-f74cf1689b8658af3ff6c… | 200 | — | 217 ms |
| 19:44:03.752 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/ninja/dist/client/714-f74cf1689b8658af3ff6c… | 200 | — | 217 ms |
| 19:44:03.752 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/ninja/dist/client/441-f74cf1689b8658af3ff6c… | 200 | — | 269 ms |
| 19:44:03.752 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/ninja/dist/client/801-f74cf1689b8658af3ff6c… | 200 | — | 272 ms |
| 19:44:03.754 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/your-activity-in-cart/dist/client/716-23137… | 200 | — | 270 ms |
| 19:44:03.763 | POST | https://cdn6.forter.com/a4091a3a2309/b36b7e0314ba4bb5a2979e1b72285963/prop.json | 200 | — | 205 ms |
| 19:44:03.763 | POST | https://b36b7e0314ba4bb5a2979e1b72285963-a4091a3a2309.cdn.forter.com/prop.json | 200 OK | — | 235 ms |
| 19:44:03.781 | GET | https://www.bestbuy.com/~assets/bby/_com/pricing/price/dist/client/6304-28cf7995cce8475ef… | 200 | — | 257 ms |
| 19:44:03.781 | GET | https://www.bestbuy.com/~assets/bby/_com/pricing/price/dist/client/8264-28cf7995cce8475ef… | 200 | — | 270 ms |
| 19:44:03.893 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 54 ms |
| 19:44:03.893 | GET | https://www.bestbuy.com/offerview/v1/offer/links?offerIds=852754 | 200 | — | 199 ms |
| 19:44:03.894 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 60 ms |
| 19:44:03.894 | GET | https://www.bestbuy.com/pricing/v1/price/item?cartTimestamp=1779047043086&catalog=bby&con… | 200 | — | 325 ms |
| 19:44:03.894 | GET | https://www.bestbuy.com/pricing/v1/price/item?cartTimestamp=1779047043086&catalog=bby&con… | 200 | — | 487 ms |
| 19:44:03.894 | GET | https://www.bestbuy.com/pricing/v1/price/item?cartTimestamp=1779047043086&catalog=bby&con… | 200 | — | 572 ms |
| 19:44:03.976 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 302 ms |
| 19:44:03.977 | GET | https://www.bestbuy.com/api/tcfb/model.json?paths=%5B%5B%22shop%22%2C%22magellan%22%2C%22… | 200 | — | 301 ms |
| 19:44:04.022 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/initChildPipeline-688a87c4a5f75… | 200 | — | 141 ms |
| 19:44:04.062 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/your-activity-in-cart/dist/client/191-0f851… | 200 | — | 155 ms |
| 19:44:04.062 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/your-activity-in-cart/dist/client/735-23137… | 200 | — | 120 ms |
| 19:44:04.062 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/your-activity-in-cart/dist/client/225-23137… | 200 | — | 162 ms |
| 19:44:04.062 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/your-activity-in-cart/dist/client/788-23137… | 200 | — | 161 ms |
| 19:44:04.062 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/your-activity-in-cart/dist/client/996-23137… | 200 | — | 162 ms |
| 19:44:04.062 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/your-activity-in-cart/dist/client/216-23137… | 200 | — | 162 ms |
| 19:44:04.062 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/your-activity-in-cart/dist/client/191-23137… | 200 | — | 163 ms |
| 19:44:04.062 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/your-activity-in-cart/dist/client/891-23137… | 200 | — | 164 ms |
| 19:44:04.062 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/your-activity-in-cart/dist/client/916-23137… | 200 | — | 165 ms |
| 19:44:04.263 | GET | https://securepubads.g.doubleclick.net/tag/js/gpt.js | 200 | — | 2 ms |
| 19:44:04.263 | GET | https://dynamic.criteo.com/js/ld/ld.js?a=41829 | 200 | — | 290 ms |
| 19:44:04.263 | POST | https://www.bestbuy.com/awacs-ingestor/api/cload | 200 | — | 203 ms |
| 19:44:04.264 | POST | https://www.bestbuy.com/awacs-ingestor/api/airport | 200 | — | 358 ms |
| 19:44:04.317 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:44:04.322 | POST | https://b36b7e0314ba4bb5a2979e1b72285963-a4091a3a2309.cdn.forter.com/prop.json | 200 OK | — | 241 ms |
| 19:44:04.432 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:44:04.449 | GET | https://securepubads.g.doubleclick.net/pagead/managed/js/gpt/m202605130101/pubads_impl.js… | 200 | — | 4 ms |
| 19:44:04.475 | GET | https://www.bestbuy.com/~assets/bby/_com/pricing/price/dist/client/3511-28cf7995cce8475ef… | 200 | — | 147 ms |
| 19:44:04.476 | GET | https://www.bestbuy.com/~assets/bby/_com/pricing/price/dist/client/4242-28cf7995cce8475ef… | 200 | — | 184 ms |
| 19:44:04.478 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/location-tooltip/dist/client/client-9359d17… | 200 | — | 144 ms |
| 19:44:04.525 | GET | blob:https://www.bestbuy.com/ed735791-7e9a-4436-9e02-f02ad2744327 | -1 | — | <1 ms |
| 19:44:04.539 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/location-tooltip/dist/client/client-fd88b03… | 200 | — | 174 ms |
| 19:44:04.545 | GET | https://www.bestbuy.com/~assets/bby/_img/int/plsvgdef-frontend/svg/Caret_Down_Line_Sm.svg | 200 | — | 169 ms |
| 19:44:04.545 | GET | https://www.bestbuy.com/list-api/rest/v1/list/saveditems | 200 | — | 323 ms |
| 19:44:04.613 | GET | https://d.criteo.com/Delivery/ClientPaths/Library/rm.js?a=41829&808685478 | 200 | — | 250 ms |
| 19:44:04.614 | GET | https://cdn.id5-sync.com/api/1.0/id5-api.js | 200 | — | 230 ms |
| 19:44:04.614 | POST | https://cdn3.forter.com/events | 200 | — | 283 ms |
| 19:44:04.615 | GET | https://gum.criteo.com/syncframe?topUrl=www.bestbuy.com&origin=onetag | 200 | — | 229 ms |
| 19:44:04.617 | GET | https://securepubads.g.doubleclick.net/pagead/managed/dict/m202605140101/gpt | 200 | — | 2 ms |
| 19:44:04.628 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/location-tooltip/dist/client/9550-9359d177e… | 200 | — | 146 ms |
| 19:44:04.628 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/location-tooltip/dist/client/1890-9359d177e… | 200 | — | 147 ms |
| 19:44:04.885 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:44:05.058 | GET | https://gum.criteo.com/sid/json?origin=onetag&domain=bestbuy.com&sn=ChromeSyncframe&so=un… | 200 | — | 44 ms |
| 19:44:05.149 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/location-tooltip/dist/client/1468-9359d177e… | 200 | — | 148 ms |
| 19:44:05.157 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:44:05.158 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:44:05.270 | GET | https://sslwidget.criteo.com/event?a=41829&v=5.46.0&p0=e%3Dexd%26rvi%3D11d61959-64a5-4174… | 200 | — | 273 ms |
| 19:44:05.465 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=4&c=2493&i=4ykco5&p=privacy_prod_… | 204 | — | 59 ms |
| 19:44:05.466 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=5&c=2493&i=4ykco5&p=privacy_prod_… | 204 | — | 59 ms |
| 19:44:05.466 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=6&c=2493&i=4ykco5&p=privacy_prod_… | 204 | — | 60 ms |
| 19:44:05.469 | GET | https://www.bestbuy.com/list-api/rest/v1/list/saveditems | 200 | — | 284 ms |
| 19:44:05.555 | GET | blob:https://www.bestbuy.com/19561ea5-3f22-4447-84c6-eddd5baa5083 | -1 | — | <1 ms |
| 19:44:05.625 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/confirmIt-245d713c1a9c5a… | 200 | — | 3 ms |
| 19:44:05.625 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/5874-9a107908d934684f83e… | 200 | — | 134 ms |
| 19:44:05.625 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/adobeInit-a2318ff1a8645e… | 200 | — | 146 ms |
| 19:44:05.630 | GET | https://tmx.bestbuy.com/zMCvS1t0EO7mWUAW?2945f4dbd29082b5=l1fSKQFoWxIElHu_MBKnEB_FQVnMlIv… | 200 OK | — | 650 ms |
| 19:44:05.632 | GET | https://tmx.bestbuy.com/_9W3D8FDfyxloaba?931b197c658c0b11=zQtNMZ-u6YvLeTiTIbt5WOrJy-4Q36F… | 200 OK | — | 384 ms |
| 19:44:05.642 | GET | https://cm.g.doubleclick.net/pixel?google_nid=cjp&google_sc&google_ula=913071&CriteoUserI… | 302 | — | 162 ms |
| 19:44:05.642 | GET | https://partner.mediawallahscript.com/?account_id=1043&partner_id=1048&uid=k-QptSWIVOpaHQ… | 302 | — | 242 ms |
| 19:44:05.642 | GET | https://x.bidswitch.net/sync?dsp_id=46&user_id=k-Vc6UsoVOpaHQtNTWMmEnrTsszGYb61V6_jOYug&e… | 302 | — | 254 ms |
| 19:44:05.642 | GET | https://ib.adnxs.com/getuid?https://dis.criteo.com/dis/rtb/appnexus/cookiematch.aspx?appn… | 307 | — | 358 ms |
| 19:44:05.643 | GET | https://gum.criteo.com/sync?c=8&r=1&a=1&u=https%3A%2F%2Fdpm.demdex.net%2Fibs%3Adpid%3D286… | 302 | — | 216 ms |
| 19:44:05.643 | GET | https://cs.media.net/cksync.php?cs=3&type=crt&ovsid=k-YHcnr4VOpaHQtNTWMmEnrTsszGarwz4AkDI… | 200 | — | 231 ms |
| 19:44:05.643 | GET | https://r.casalemedia.com/rum?cm_dsp_id=20&external_user_id=k-UctZtYVOpaHQtNTWMmEnrTsszGZ… | 302 | — | 279 ms |
| 19:44:05.643 | GET | https://simage4.pubmatic.com/AdServer/SPug?partnerID=167352&partnerUID=uid:k-yZiQ5YVOpaHQ… | 200 | — | 389 ms |
| 19:44:05.643 | GET | https://ad.360yield.com/match?publisher_dsp_id=38&external_user_id=k-OJ0XXYVOpaHQtNTWMmEn… | 302 | — | 452 ms |
| 19:44:05.643 | GET | https://i.liadm.com/s/28292?bidder_id=71340&bidder_uuid=k--X2SjoVOpaHQtNTWMmEnrTsszGawf-O… | 303 See Other | — | 538 ms |
| 19:44:05.643 | GET | https://exchange.mediavine.com/usersync/push?partner=criteo&partnerId=k-La04r4VOpaHQtNTWM… | 200 | — | 538 ms |
| 19:44:05.643 | GET | https://c.bing.com/c.gif?Red3=CTOMS_pd&cbid=k-MjUgIYVOpaHQtNTWMmEnrTsszGZfSjJBUew7Dw | 200 | — | 573 ms |
| 19:44:05.643 | GET | https://sync.outbrain.com/cookie-sync?p=criteo&uid=k-AZcGWIVOpaHQtNTWMmEnrTsszGa_b2AGVYTL… | 200 OK | — | 570 ms |
| 19:44:05.643 | GET | https://trends.revcontent.com/cm/pixel_sync?bidder=151&bidder_uid=k-3qAaXYVOpaHQtNTWMmEnr… | -1 | — | <1 ms |
| 19:44:05.643 | GET | https://jadserve.postrelease.com/suid/1017?vk=k-W2V3TIVOpaHQtNTWMmEnrTsszGZ7QY-Dw0ru3Q | 200 | — | 691 ms |
| 19:44:05.643 | GET | https://simage2.pubmatic.com/AdServer/Pug?vcode=bz0yJnR5cGU9MSZjb2RlPTE5MjgmdGw9NDMyMDA=&… | 200 | — | 700 ms |
| 19:44:05.643 | GET | https://pixel.rubiconproject.com/tap.php?v=6434&nid=2149&put=k-6yPgCYVOpaHQtNTWMmEnrTsszG… | 200 OK | — | 896 ms |
| 19:44:05.644 | GET | https://rtb-csync.smartadserver.com/redir/?partnerid=79&partneruserid=k-Jh9RI4VOpaHQtNTWM… | 200 | — | 722 ms |
| 19:44:05.644 | GET | https://tapestry.tapad.com/tapestry/1?ta_partner_id=2052&ta_partner_did=k-RoodIIVOpaHQtNT… | 200 | — | 714 ms |
| 19:44:05.644 | GET | https://eb2.3lift.com/xuid?mid=2711&xuid=k-pxrK5YVOpaHQtNTWMmEnrTsszGZaZeRX7_mqkA&dongle=… | 302 | — | 1.21 s |
| 19:44:05.644 | GET | https://sync.1rx.io/usersync/criteodsp/k-JOyeeYVOpaHQtNTWMmEnrTsszGaLeSiEMy-EYQ | 302 | — | 1.50 s |
| 19:44:05.644 | GET | https://ad.tpmn.co.kr/pixelCt.tpmn?tpmn_nid=26a681017b4fdc02f3aef3aa921ede3e&tpmn_buid=k-… | 302 | — | 1.50 s |
| 19:44:05.644 | GET | https://criteo-sync.teads.tv/um?eid=80&uid=k-YqI5NoVOpaHQtNTWMmEnrTsszGaF3sFtQIcSUw | 200 | — | 795 ms |
| 19:44:05.644 | GET | https://sync-t1.taboola.com/sg/criteortb-network/1/rtb-h/?taboola_hm=k-rbkInIVOpaHQtNTWMm… | 200 | — | 866 ms |
| 19:44:05.644 | GET | https://criteo-partners.tremorhub.com/sync?UICR=k-MOU6jYVOpaHQtNTWMmEnrTsszGY6C0Ylyt5ysw | 200 | — | 860 ms |
| 19:44:05.644 | GET | https://ade.clmbtech.com/uid/sync.htm?pid=13079&cuid=k-RblHyYVOpaHQtNTWMmEnrTsszGYeNo7NBY… | 200 OK | — | 1.46 s |
| 19:44:05.651 | GET | https://tmx.bestbuy.com/xbQ6uimf1nUhoMQv?f1ca8bf00c334d87=xtEMTBIJd7qBLJOa6B6a6LFBmp9ckka… | 200 OK | — | 843 ms |
| 19:44:05.772 | GET | https://dis.criteo.com/dis/rtb/google/cookiematch.aspx?id=&CriteoUserId=k-QptSWIVOpaHQtNT… | 200 | — | 43 ms |
| 19:44:05.806 | GET | https://dpm.demdex.net/ibs:dpid=28645&dpuuid=uCz7T18lMkJMYUxWa25Kb1ZkSXlqJTJCTHJTU09IWEkz… | 200 | — | 67 ms |
| 19:44:05.806 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 357 ms |
| 19:44:05.828 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/aq-init-6e37ecd8fe344c27… | 200 | — | 133 ms |
| 19:44:05.829 | GET | https://partner.mediawallahscript.com/?account_id=1043&partner_id=1048&uid=k-QptSWIVOpaHQ… | 302 | — | 56 ms |
| 19:44:05.830 | GET | https://x.bidswitch.net/ul_cb/sync?dsp_id=46&user_id=k-Vc6UsoVOpaHQtNTWMmEnrTsszGYb61V6_j… | 200 | — | 61 ms |
| 19:44:05.844 | GET | blob:https://www.bestbuy.com/9b39c1e7-9acc-49e7-aa0a-2f840d8cf96d | -1 | — | <1 ms |
| 19:44:05.860 | GET | https://r.casalemedia.com/rum?cm_dsp_id=20&external_user_id=k-UctZtYVOpaHQtNTWMmEnrTsszGZ… | 200 | — | 89 ms |
| 19:44:05.886 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/kDGYzLOQ/d2YKXBFXew4/TD/gwXSZsbmQt | 200 | — | 232 ms |
| 19:44:05.887 | GET | https://gum.criteo.com/sync?c=9&r=1&a=1&u=https%3A%2F%2Faa.agkn.com%2Fadscores%2Fg.pixel%… | 302 | — | 55 ms |
| 19:44:05.887 | GET | https://secure.adnxs.com/getuid?https://partner.mediawallahscript.com/?account_id=2016&pa… | 307 | — | 59 ms |
| 19:44:05.937 | GET | https://lbs.eu-1-id5-sync.com/lbs/v1 | 200 | — | 626 ms |
| 19:44:05.937 | GET | https://id5-sync.com/bounce | 200 | — | 669 ms |
| 19:44:05.938 | GET | https://lb.eu-1-id5-sync.com/lb/v1 | 200 | — | 657 ms |
| 19:44:05.942 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:44:05.944 | GET | https://aa.agkn.com/adscores/g.pixel?sid=9212273938&ct=MQa3JV8lMkJMYUxWa25Kb1ZkSXlqJTJCTH… | 200 | — | 202 ms |
| 19:44:05.945 | GET | https://ib.adnxs.com/bounce?%2Fgetuid%3Fhttps%3A%2F%2Fdis.criteo.com%2Fdis%2Frtb%2Fappnex… | 302 | — | 107 ms |
| 19:44:05.946 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:44:05.951 | GET | https://www.bestbuy.com/streams/v1/SEARCH_TERM?limit=25 | 200 | — | 219 ms |
| 19:44:05.968 | POST | https://www.bestbuy.com/streams/v1/consume | 200 | — | 192 ms |
| 19:44:05.971 | GET | https://secure.adnxs.com/bounce?%2Fgetuid%3Fhttps%3A%2F%2Fpartner.mediawallahscript.com%2… | 302 | — | 80 ms |
| 19:44:06.038 | GET | https://ad.360yield.com/ul_cb/match?publisher_dsp_id=38&external_user_id=k-OJ0XXYVOpaHQtN… | 200 | — | 61 ms |
| 19:44:06.051 | GET | https://dis.criteo.com/dis/rtb/appnexus/cookiematch.aspx?appnxsid=1768278208481637259 | 200 | — | 60 ms |
| 19:44:06.052 | GET | https://partner.mediawallahscript.com/?account_id=2016&partner_id=2087&uid=39927451946425… | 302 | — | 45 ms |
| 19:44:06.071 | GET | https://i.liadm.com/s/28292?bidder_id=71340&bidder_uuid=k--X2SjoVOpaHQtNTWMmEnrTsszGawf-O… | 303 See Other | — | 52 ms |
| 19:44:06.097 | GET | https://sync.crwdcntrl.net/map/c=14717/tp=MWSP/tpid=c3da5030-5228-11f1-8d24-fd19a179a640?… | 302 | — | 269 ms |
| 19:44:06.123 | GET | https://thrtle.com/sync?vxii_pid=7006&vxii_pdid=0a66f1d8-b778-4640-9a01-7a213931c360&us_p… | 302 | — | 237 ms |
| 19:44:06.124 | GET | https://ib.adnxs.com/setuid?entity=52&code=k-dAGHE4VOpaHQtNTWMmEnrTsszGYTtjLAzm5pwQ | 200 | — | 62 ms |
| 19:44:06.274 | GET | https://tmx.bestbuy.com/fp/clear.png | 200 OK | — | 398 ms |
| 19:44:06.274 | GET | https://tmx.bestbuy.com/G2kiRT1r952v9uqn?b2220ab98570fed9=xpSrH7N4LWRQcjrhdvKEDuPrUfbyxay… | 204 204 | — | 323 ms |
| 19:44:06.276 | GET | https://tmx.bestbuy.com/37TzKqEt5S8zUNCq?7698d01cf7e3670f=GJakMSQJglKkT9f4oVcNpa10lUX7JF0… | 200 OK | — | 112 ms |
| 19:44:06.286 | GET | https://tmx.bestbuy.com/G2kiRT1r952v9uqn?b2220ab98570fed9=xpSrH7N4LWRQcjrhdvKEDuPrUfbyxay… | 200 OK | — | 259 ms |
| 19:44:06.286 | GET | https://tmx.bestbuy.com/v7xadt9yb94a19R4?dc532946eb1491d3=Qvnr5qOv2GuA6Bf4rHjgHYRPQf3EDvn… | 200 OK | — | 508 ms |
| 19:44:06.292 | GET | https://tmx.bestbuy.com/cbEel_62AD8CRMf-?a182a8107ae174c6=yhCuYw0JT4uwQ-T1_yDAnkrHkVcDG_c… | 200 OK | — | 199 ms |
| 19:44:06.294 | GET | https://ummqowa26fhed77vwlje5clagyrpliga7pj2b4gv665f7d8d85c3d862sac.d.aa.online-metrix.ne… | 200 OK | — | 1.16 s |
| 19:44:06.294 | GET | https://h64.online-metrix.net/NcaAYJ2FTzIwHK59?0032a47a8b97ac92=K2QfDmb7fiEYle9xL-9NvduKE… | 200 OK | — | 949 ms |
| 19:44:06.305 | GET | https://thrtle.com/sync?_reach=1&vxii_pdid=0a66f1d8-b778-4640-9a01-7a213931c360&vxii_pid=… | 302 | — | 100 ms |
| 19:44:06.310 | GET | https://partner.mediawallahscript.com/?account_id=2023&partner_id=2118&uid=750a8493552fa8… | 302 | — | 91 ms |
| 19:44:06.325 | GET | https://tmx.bestbuy.com/fXupl4zt5TakLeFH?fccc6f14ef1c435c=OukvPiLl0L05xkomeZaHLa8Dc7kp9mX… | 204 204 | — | 461 ms |
| 19:44:06.402 | GET | https://bh.contextweb.com/bh/rtset?daaqp=1&ev=bff75fa5-7a2b-431a-b81b-0716f8ac85c3&pid=56… | 302 | — | 768 ms |
| 19:44:06.404 | GET | https://match.adsrvr.org/track/cmf/generic?ttd_pid=vxsrv3i&ttd_tpi=1 | 302 | — | 780 ms |
| 19:44:06.795 | GET | https://eb2.3lift.com/xuid?ld=1&mid=2711&xuid=k-pxrK5YVOpaHQtNTWMmEnrTsszGZaZeRX7_mqkA&do… | 200 | — | 57 ms |
| 19:44:07.096 | GET | https://sync.1rx.io/usersync/criteodsp/k-JOyeeYVOpaHQtNTWMmEnrTsszGaLeSiEMy-EYQ?zcc=1&cb=… | 302 | — | 51 ms |
| 19:44:07.097 | GET | https://ad.tpmn.io/pixelct.tpmn?tpmn_nid=26a681017b4fdc02f3aef3aa921ede3e&tpmn_buid=k-f9e… | 200 | — | 616 ms |
| 19:44:07.098 | GET | https://match.adsrvr.org/track/cmb/generic?ttd_pid=vxsrv3i&ttd_tpi=1 | 302 | — | 95 ms |
| 19:44:07.099 | GET | https://thrtle.com/sync?vxii_pid=5053&vxii_pdid=hBLklGLWPZUA&vxii_ts=1&_t=1779047046&_rea… | 302 | — | 49 ms |
| 19:44:07.147 | GET | https://d.turn.com/r/dd/id/L2NzaWQvMS9jaWQvMTc1MDYwNzE3Ni90LzA/dpuid/bff75fa5-7a2b-431a-b… | 302 | — | 665 ms |
| 19:44:07.147 | GET | https://sync.targeting.unrulymedia.com/csync/RX-c7a25765-12da-43bb-8d91-6a1a39b72edc-005 | 200 | — | 504 ms |
| 19:44:07.192 | GET | https://partner.mediawallahscript.com/?account_id=2027&partner_id=2051&uid=898e2ddc-7fa7-… | 302 | — | 222 ms |
| 19:44:07.415 | GET | https://obgpm76tt0a0sgogzhdfe.redinuid.imrworldwide.com/mwal?url=https://partner.mediawal… | 302 | — | 398 ms |
| 19:44:07.558 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/gtagATC-7cfc8330b65e6ea1… | 200 | — | 78 ms |
| 19:44:07.559 | GET | https://tmx.bestbuy.com/fXupl4zt5TakLeFH?fccc6f14ef1c435c=OukvPiLl0L05xkomeZaHLa8Dc7kp9mX… | 204 204 | — | 96 ms |
| 19:44:07.570 | GET | https://tmx.bestbuy.com/6hW5qpXAo4mzeQSb?1c12f57ae9fddf97=jfnlvCDanp6ilkN0Xz3Gf1mOmd8ReNv… | 200 OK | — | 97 ms |
| 19:44:07.570 | GET | https://tmx.bestbuy.com/YGGDlN9ZPPFuUozR?e22bd37f28526cbf=XyOTTjP7aEfFoPjiMjjrL5h-iGvOKYi… | 200 OK | — | 99 ms |
| 19:44:07.581 | GET | https://tmx.bestbuy.com/G2kiRT1r952v9uqn?b2220ab98570fed9=xpSrH7N4LWRQcjrhdvKEDuPrUfbyxay… | 200 OK | — | 98 ms |
| 19:44:07.581 | GET | https://tmx.bestbuy.com/fXupl4zt5TakLeFH?fccc6f14ef1c435c=OukvPiLl0L05xkomeZaHLa8Dc7kp9mX… | 204 204 | — | 102 ms |
| 19:44:07.765 | GET | https://thrtle.com/sync?vxii_pid=5046&vxii_pdid=3796399831675714228&t=1531451857 | 302 | — | 114 ms |
| 19:44:07.766 | GET | https://partner.mediawallahscript.com/?account_id=2006&partner_id=2131&custom=&tag_format… | 302 | — | 114 ms |
| 19:44:07.777 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/flashtalkingCart-7126247… | 200 | — | 108 ms |
| 19:44:07.785 | POST | https://id5-sync.com/gm/v3 | 200 | — | 164 ms |
| 19:44:07.880 | GET | https://cms.analytics.yahoo.com/cms?partner_id=THROTLE | 302 | — | 277 ms |
| 19:44:07.880 | GET | https://ap.lijit.com/pixel?redir=https%3A%2F%2Fpartner.mediawallahscript.com%2F%3Faccount… | 307 | — | 368 ms |
| 19:44:07.922 | GET | https://servedby.flashtalking.com/container/7922;86519;8908;iframe/?spotName=Product_Cart… | 200 OK | — | 604 ms |
| 19:44:07.974 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/kDGYzLOQ/d2YKXBFXew4/TD/gwXSZsbmQt | 200 | — | 155 ms |
| 19:44:07.980 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=7&c=2493&i=4ykco5&p=privacy_prod_… | 204 | — | 65 ms |
| 19:44:07.981 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=8&c=2493&i=4ykco5&p=privacy_prod_… | 204 | — | 68 ms |
| 19:44:07.981 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=9&c=2493&i=4ykco5&p=privacy_prod_… | 204 | — | 69 ms |
| 19:44:08.017 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 290 ms |
| 19:44:08.103 | POST | https://www.bestbuy.com/cart/checkout | 200 | — | 1.06 s |
| 19:44:08.110 | GET | https://ups.analytics.yahoo.com/ups/58691/cms?partner_id=THROTLE | 302 | — | 60 ms |
| 19:44:08.114 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 317 ms |
| 19:44:08.119 | GET | https://tmx.bestbuy.com/fXupl4zt5TakLeFH?fccc6f14ef1c435c=OukvPiLl0L05xkomeZaHLa8Dc7kp9mX… | 204 204 | — | 104 ms |
| 19:44:08.125 | GET | https://smetrics.bestbuy.com/id?d_visid_ver=4.4.0&d_fieldgroup=A&mcorgid=F6301253512D2BDB… | 200 | — | 745 ms |
| 19:44:08.153 | GET | https://tmx.bestbuy.com/fXupl4zt5TakLeFH?fccc6f14ef1c435c=OukvPiLl0L05xkomeZaHLa8Dc7kp9mX… | 204 204 | — | 108 ms |
| 19:44:08.192 | GET | https://bb.lijit.com/pixel?redir=https%3A%2F%2Fpartner.mediawallahscript.com%2F%3Faccount… | 307 | — | 592 ms |
| 19:44:08.447 | GET | https://ups.analytics.yahoo.com/ups/58691/cms?partner_id=THROTLE&verify=true | 302 | — | 77 ms |
| 19:44:08.467 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/cart-83b1cc9215d35e3949b… | 200 | — | 109 ms |
| 19:44:08.526 | GET | https://thrtle.com/sync?vxii_pid=5038&vxii_pdid=y-zd3u4fVE2oS7.4Qci2xeaQU8TFsQkTxEImOrYg-… | 200 | — | 50 ms |
| 19:44:08.629 | GET | https://tmx.bestbuy.com/G2kiRT1r952v9uqn?b2220ab98570fed9=xpSrH7N4LWRQcjrhdvKEDuPrUfbyxay… | 200 OK | — | 112 ms |
| 19:44:08.725 | GET | https://partner.mediawallahscript.com/?account_id=1009&partner_id=c182f930&uid=MrsgALZHOD… | 302 | — | 48 ms |
| 19:44:08.771 | GET | https://servedby.flashtalking.com/spot/8/7922;86519;8908/?spotName=Product_Cart&U1=C&U2=C… | 200 OK | — | 101 ms |
| 19:44:08.773 | GET | https://image6.pubmatic.com/AdServer/UCookieSetPug?rd=https%3A%2F%2Fpartner.mediawallahsc… | 302 | — | 288 ms |
| 19:44:08.774 | GET | https://fdz.flashtalking.com/services/bestbuy/dynamicpixel/?u1=c&u2=Cart%20-%20Index&u3=%… | 200 | — | 398 ms |
| 19:44:08.919 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 65 ms |
| 19:44:09.005 | GET | https://partner.mediawallahscript.com/?account_id=2030&partner_id=2147&uid=71C1C11A-3E7D-… | 302 | — | 51 ms |
| 19:44:09.056 | GET | https://sync.mathtag.com/sync/img?mt_exid=10103&redirect=https://partner.mediawallahscrip… | 302 Moved Temporarily | — | 275 ms |
| 19:44:09.143 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 277 ms |
| 19:44:09.205 | GET | https://www.bestbuy.com/identity/signin?token=tid%3Ac5b15a3a-5228-11f1-8b3c-12e464dd83f7 | 200 | — | 340 ms |
| 19:44:09.206 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 116 ms |
| 19:44:09.206 | POST | https://tmx.bestbuy.com/fMVLsv7XLpIOyX2F?09a5600da6e22749=8YP59xu5ZUTd35bRVVzE3fGkq2UE8Oo… | 200 OK | — | 110 ms |
| 19:44:09.220 | GET | https://www.bestbuy.com/pricing/v1/price/item?cartTimestamp=1779047049357&catalog=bby&con… | -1 | — | <1 ms |
| 19:44:09.220 | GET | https://www.bestbuy.com/pricing/v1/price/item?cartTimestamp=1779047049357&catalog=bby&con… | -1 | — | <1 ms |
| 19:44:09.220 | GET | https://www.bestbuy.com/pricing/v1/price/item?cartTimestamp=1779047049357&catalog=bby&con… | -1 | — | <1 ms |
| 19:44:09.275 | GET | https://partner.mediawallahscript.com/?account_id=2036&partner_id=2149&uid=c0746a0a-1a89-… | 302 | — | 41 ms |
| 19:44:09.317 | GET | https://match.prod.bidr.io/cookie-sync/mediawallah?dif=1 | -1 | — | <1 ms |
| 19:44:09.579 | POST | https://tmx.bestbuy.com/fXupl4zt5TakLeFH?fccc6f14ef1c435c=OukvPiLl0L05xkomeZaHLa8Dc7kp9mX… | -1 | — | <1 ms |
| 19:44:09.579 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | -1 | — | <1 ms |
| 19:44:09.580 | POST | https://fel-api.prod.browse.bestbuy.com/exception | -1 | — | <1 ms |
| 19:44:09.581 | POST | https://fel-api.prod.browse.bestbuy.com/exception | -1 | — | <1 ms |
| 19:44:09.588 | GET | https://nexus.ensighten.com/bestbuy/privacy_init/Bootstrap.js | 200 | — | 42 ms |
| 19:44:09.588 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/federation/platformContainerOrchestration… | 200 | — | 121 ms |
| 19:44:09.588 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/bestbuy/lib-mf-assets/2.1.2/dist/main.js | 200 | — | 121 ms |
| 19:44:09.588 | GET | https://www.bestbuy.com/~assets/bby/_js/ext/bbydyn/dyn_digital_idnty.js | 200 | — | 123 ms |
| 19:44:09.588 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/react/16.8.6/dist/react.production.min.js | 200 | — | 135 ms |
| 19:44:09.588 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/react-dom/16.8.6/dist/react-dom.productio… | 200 | — | 151 ms |
| 19:44:09.590 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/lodash-v4/4.17.21/dist/lodash.min.js | 200 | — | 149 ms |
| 19:44:09.590 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/optimizely/optimizely-sdk/4.10.0/dist/opt… | 200 | — | 153 ms |
| 19:44:09.590 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/redux/3.7.2/dist/redux.min.js | 200 | — | 159 ms |
| 19:44:09.590 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/react-redux/5.1.1/dist/react-redux.min.js | 200 | — | 159 ms |
| 19:44:09.590 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/redux-thunk/2.3.0/dist/redux-thunk.min.js | 200 | — | 166 ms |
| 19:44:09.590 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/prop-types/15.8.1/dist/prop-types.min.js | 200 | — | 168 ms |
| 19:44:09.590 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/optimizely/1.4.1-bbycustom/dist/optimizel… | 200 | — | 177 ms |
| 19:44:09.591 | GET | https://www.bestbuy.com/~assets/bby/_com/deo-client-script.js | 200 | — | 1 ms |
| 19:44:09.591 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/jquery/3.7.1/dist/jquery.min.js | 200 | — | 178 ms |
| 19:44:09.591 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/analytics-q/6.0.10/dist/analyticsQ.bundle… | 200 | — | 229 ms |
| 19:44:09.591 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/gvp/lib-action-log/3.0.42/dist/main.js | 200 | — | 229 ms |
| 19:44:09.591 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/gvp/lib-config-service/2.3.3/dist/main.js | 200 | — | 231 ms |
| 19:44:09.591 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/i18next/8.4.2/dist/i18next.min.js | 200 | — | 228 ms |
| 19:44:09.591 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/gvp/lib-falcor-model/7.0.28/dist/client.js | 200 | — | 232 ms |
| 19:44:09.591 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/react-i18next/4.8.0/dist/react-i18next.mi… | 200 | — | 234 ms |
| 19:44:09.591 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/gvp/lib-initializer/2.1.9/dist/initialize… | 200 | — | 234 ms |
| 19:44:09.591 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/backbone/1.1.2/dist/backbone-min.js | 200 | — | 235 ms |
| 19:44:09.591 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/shop/lib-eventmanager/3.1.0/dist/event-ma… | 200 | — | 240 ms |
| 19:44:09.591 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/gvp/lib-fetch/4.0.12/dist/client.js | 200 | — | 240 ms |
| 19:44:09.591 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/gvp/lib-appear/5.0.19/dist/main.umd.js | 200 | — | 239 ms |
| 19:44:09.591 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/brix-web/7.11.32/css/brix.css | 200 | — | 240 ms |
| 19:44:09.591 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/falcor/2.3.2/dist/falcor.browser.min.js | 200 | — | 254 ms |
| 19:44:09.591 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/gvp/lib-embedded-component-renderer/5.2.1… | 200 | — | 253 ms |
| 19:44:09.591 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/bestbuy/window-log/1.1.23/dist/window-log… | 200 | — | 282 ms |
| 19:44:09.591 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/gvp/cookie-gatekeeper/1.2.41/dist/main.js | 200 | — | 285 ms |
| 19:44:09.591 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/brix-web/7.11.32/js/brix.js | 200 | — | 287 ms |
| 19:44:09.592 | GET | https://www.bestbuy.com/~assets/bby/_com/sc-react-sign-on/dist/vendors-mini-header-footer… | 200 | — | 248 ms |
| 19:44:09.592 | GET | https://www.bestbuy.com/~assets/bby/_com/sc-react-sign-on/dist/sign-on/sign-on-bundle-52c… | 200 | — | 269 ms |
| 19:44:09.592 | GET | https://www.bestbuy.com/~assets/bby/_com/sc-react-sign-on/dist/vendors-standard-theme/ven… | 200 | — | 271 ms |
| 19:44:09.592 | GET | https://www.bestbuy.com/~assets/bby/_com/sign-on/less/themes/bestBuy-82f9b4be7e8f5cc49cc1… | 200 | — | 284 ms |
| 19:44:09.592 | GET | https://www.bestbuy.com/~assets/bby/_com/sc-react-sign-on/dist/vendors/vendors-standard-t… | 200 | — | 285 ms |
| 19:44:09.592 | GET | https://www.bestbuy.com/~assets/bby/_com/sc-react-sign-on/dist/vendors-common/vendors-com… | 200 | — | 286 ms |
| 19:44:09.592 | GET | https://www.bestbuy.com/~assets/bby/_com/sc-react-sign-on/dist/vendors/vendors-mini-heade… | 200 | — | 287 ms |
| 19:44:09.592 | GET | https://www.bestbuy.com/~assets/bby/_com/sc-bby-libraries/externals/moment/2.13.0/moment.… | 200 | — | 285 ms |
| 19:44:09.592 | GET | https://www.bestbuy.com/~assets/bby/_com/sc-react-sign-on/dist/vendors/vendors-core-31d45… | 200 | — | 292 ms |
| 19:44:09.592 | GET | https://www.bestbuy.com/~assets/bby/_com/sc-react-sign-on/dist/vendors/vendors-common-963… | 200 | — | 293 ms |
| 19:44:09.593 | GET | https://www.bestbuy.com/~assets/bby/_com/@ds/unified-chat/dist/javascript/unified-chat-in… | 200 | — | 1 ms |
| 19:44:09.593 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/lib-dai/dist/client/client-089bbe3cbb4e8848… | 200 | — | 21 ms |
| 19:44:09.593 | GET | https://www.bestbuy.com/~assets/bby/_com/sc-react-sign-on/dist/vendors/vendors-sign-on-4e… | 200 | — | 313 ms |
| 19:44:09.593 | GET | https://www.bestbuy.com/~assets/bby/_com/sc-react-sign-on/dist/sign-on/sign-on-bundle-499… | 200 | — | 315 ms |
| 19:44:09.593 | GET | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 200 | — | 324 ms |
| 19:44:09.593 | GET | https://img.bbystatic.com/BestBuy_US/js/tracking/brightTag-min.js | 200 | — | 592 ms |
| 19:44:09.628 | GET | https://nexus.ensighten.com/bestbuy/privacy_prod/Bootstrap.js | 200 | — | 320 ms |
| 19:44:09.729 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/federation/platformContainer.11.9.0.js | 200 | — | 272 ms |
| 19:44:09.910 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/cj-page-visits | 200 | — | 304 ms |
| 19:44:10.032 | GET | https://accounts.google.com/gsi/client | 200 | — | 543 ms |
| 19:44:10.033 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/brix-web/7.11.32/60fb346d82490233081f.wof… | 200 | — | 103 ms |
| 19:44:10.033 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/brix-web/7.11.32/37f8017947c264b8389f.wof… | 200 | — | 108 ms |
| 19:44:10.033 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/brix-web/7.11.32/3322.7e65e0e62532d57fdc0… | 200 | — | 118 ms |
| 19:44:10.033 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/brix-web/7.11.32/2357.86dec6e0458eafbc1bc… | 200 | — | 147 ms |
| 19:44:10.033 | GET | https://www.bestbuy.com/~assets/bby/_img/int/plsvgdef-frontend/svg/bestbuy-logo-light.svg | 200 | — | 116 ms |
| 19:44:10.033 | GET | https://tmx.bestbuy.com/wcvoccgalfzi583t.js?wqmvo23sm43v466m=ummqowa2&6g5sbu72xvzgaa17=2d… | 200 OK | — | 193 ms |
| 19:44:10.033 | GET | https://appleid.cdn-apple.com/appleauth/static/jsapi/appleid/1/en_US/appleid.auth.js | 200 OK | — | 652 ms |
| 19:44:10.050 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/brix-web/7.11.32/3599.be9b67a1d4ae1f376a7… | 200 | — | 116 ms |
| 19:44:10.227 | GET | https://www.bestbuy.com/api/csiservice/v2/key/cia-grid | 200 | — | 230 ms |
| 19:44:10.227 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/cjc-page-requests | 200 | — | 302 ms |
| 19:44:10.229 | GET | https://www.bestbuy.com/~assets/bby/_com//@ds/unified-chat/dist/javascript/unified-chat-i… | 200 | — | 137 ms |
| 19:44:10.229 | GET | https://www.bestbuy.com/~assets/bby/_com//@ds/unified-chat/dist/javascript/unified-chat-i… | 200 | — | 139 ms |
| 19:44:10.229 | GET | https://www.bestbuy.com/~assets/bby/_com//@ds/unified-chat/dist/javascript/unified-chat-i… | 200 | — | 139 ms |
| 19:44:10.229 | GET | https://www.bestbuy.com/~assets/bby/_com//@ds/unified-chat/dist/javascript/unified-chat-i… | 200 | — | 146 ms |
| 19:44:10.230 | GET | https://nexus.ensighten.com/bestbuy/prod/Bootstrap.js | 200 | — | 48 ms |
| 19:44:10.230 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 352 ms |
| 19:44:10.408 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=0&c=2493&i=61xh5d&p=privacy_prod&… | 204 | — | 71 ms |
| 19:44:10.408 | GET | https://www.bestbuy.com/~assets/bby/_com//shop/lib-dai/dist/client/323-089bbe3cbb4e88488e… | 200 | — | 134 ms |
| 19:44:10.408 | GET | https://www.bestbuy.com/~assets/bby/_com//shop/lib-dai/dist/client/826-089bbe3cbb4e88488e… | 200 | — | 133 ms |
| 19:44:10.450 | GET | https://accounts.google.com/gsi/style | 200 | — | 58 ms |
| 19:44:10.453 | GET | https://accounts.google.com/gsi/button?type=button&size=large&width=345&logo_alignment=ce… | 200 | — | 338 ms |
| 19:44:10.454 | GET | https://accounts.google.com/gsi/fedcm.json | 200 | — | 354 ms |
| 19:44:10.454 | GET | https://google.com/.well-known/web-identity | 200 | — | 541 ms |
| 19:44:10.592 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/analyticsInit-aa713fca754a9e167… | 200 | — | 3 ms |
| 19:44:10.649 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/81-2c54adfeb00efd510480.… | 200 | — | 3 ms |
| 19:44:10.649 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/9557-e656009191eb0108a30… | 200 | — | 3 ms |
| 19:44:10.672 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/sandbox-index-26.16.2.html?pare… | 200 | — | <1 ms |
| 19:44:10.675 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/customer-journal-d87e751… | 200 | — | <1 ms |
| 19:44:10.679 | GET | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 200 | — | 101 ms |
| 19:44:10.679 | GET | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/kDGYzLOQ/d2YKXBFXew4/TD/gwXSZsbmQt?v… | 200 | — | 107 ms |
| 19:44:10.682 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/cj-digital-schema1-2faec… | 200 | — | <1 ms |
| 19:44:10.685 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 568 ms |
| 19:44:10.729 | GET | https://nexus.ensighten.com/bestbuy/prod/serverComponent.php?namespace=Bootstrapper&stati… | 200 | — | 58 ms |
| 19:44:10.793 | GET | https://nexus.ensighten.com/bestbuy/prod/code/bf002b521a2fdaa08ec33b8a718a5c96.js?conditi… | 200 | — | 28 ms |
| 19:44:10.824 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 255 ms |
| 19:44:10.883 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/initChildPipeline-688a87c4a5f75… | 200 | — | 2 ms |
| 19:44:10.910 | GET | https://tmx.bestbuy.com/dvjLXcQ1tEQbqROr?14e7139775997804=K9-JETsNW-JiecpLY4S2a_n_fCAeLUp… | 200 OK | — | 380 ms |
| 19:44:10.915 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/confirmIt-245d713c1a9c5a… | 200 | — | 1 ms |
| 19:44:10.915 | GET | https://tmx.bestbuy.com/zuWo2prgSc3PIDkB?e3fe4fc8bfa5e297=9vYZxFTfY3SMOhpJ0X4-rTK9fxORnf4… | 200 OK | — | 100 ms |
| 19:44:10.916 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/5874-9a107908d934684f83e… | 200 | — | 1 ms |
| 19:44:10.916 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/adobeInit-a2318ff1a8645e… | 200 | — | 1 ms |
| 19:44:10.921 | GET | https://tmx.bestbuy.com/4Q6OwU9Z7M8OcRWj?66a1a270847ac27b=t3ObNp08eLQqkgCxenBtZmtEX5VKaLB… | 200 OK | — | 90 ms |
| 19:44:10.929 | GET | https://fonts.gstatic.com/s/googlesans/v62/4UaRrENHsxJlGDuGo1OIlJfC6l_24rlCK1Yo_Iq2vgCI.w… | 200 | — | 284 ms |
| 19:44:10.941 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/aq-init-6e37ecd8fe344c27… | 200 | — | 1 ms |
| 19:44:10.995 | GET | https://accounts.google.com/gsi/fedcm/listaccounts | 200 | — | 216 ms |
| 19:44:11.051 | GET | blob:https://www.bestbuy.com/4ddc1f29-eec2-433f-abda-6f08252d3b81 | -1 | — | <1 ms |
| 19:44:11.229 | GET | blob:https://www.bestbuy.com/46c20c7c-e568-4390-ab09-4f0e1f20dc01 | -1 | — | <1 ms |
| 19:44:11.262 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 270 ms |
| 19:44:11.316 | GET | https://tmx.bestbuy.com/fp/clear.png | 200 OK | — | 376 ms |
| 19:44:11.317 | GET | https://tmx.bestbuy.com/MWTruk3x6_Q-rIRI?b0e1e6531797f334=Rip6VrwQsXykcmYb89QiX1xLIZaqZzb… | 204 204 | — | 398 ms |
| 19:44:11.319 | GET | https://tmx.bestbuy.com/65sXN0S8mWYWeb1c?1e221962b9976950=w13j711x_rnSLrk7BqX7S5HDW64yblO… | 200 OK | — | 198 ms |
| 19:44:11.324 | GET | https://tmx.bestbuy.com/MWTruk3x6_Q-rIRI?b0e1e6531797f334=Rip6VrwQsXykcmYb89QiX1xLIZaqZzb… | 200 OK | — | 96 ms |
| 19:44:11.324 | GET | https://tmx.bestbuy.com/nqXYdbZ21lCgiAlX?aa7265cf7889f5f6=b5lZpNS60435qEKlXm_p8aGLG1ePYay… | 200 OK | — | 105 ms |
| 19:44:11.325 | GET | https://h64.online-metrix.net/YyU96ZfGI1VbXR-V?6a66a1b3667dc709=3tfd_C2Zi9KgZyEKN_S-TStgh… | 200 OK | — | 380 ms |
| 19:44:11.325 | GET | https://ummqowa26fhed77vwlje5clagyrpliga7pj2b4gvc2bd7e303259b3f6sac.d.aa.online-metrix.ne… | 200 OK | — | 547 ms |
| 19:44:11.325 | GET | https://tmx.bestbuy.com/y2wgAQG1tUI-sAoK?bc729a07b82df967=J0IKF3HpincPUpJhA8sX22nH5Y5QwFb… | 200 OK | — | 198 ms |
| 19:44:11.332 | GET | https://tmx.bestbuy.com/EcBgL_BujtkBGRgJ?6b15ccb08f61b724=7R4LT_znQystUKLnBoYdgQymErB_Dms… | 204 204 | — | 371 ms |
| 19:44:11.819 | GET | https://tmx.bestbuy.com/EcBgL_BujtkBGRgJ?6b15ccb08f61b724=7R4LT_znQystUKLnBoYdgQymErB_Dms… | 204 204 | — | 116 ms |
| 19:44:11.826 | GET | https://tmx.bestbuy.com/B0CODl6X8cjmB030?1eee9ee8ffed689e=g1LzNlQu_WGd5OM_LoWQKCC1XaKbx3n… | 200 OK | — | 111 ms |
| 19:44:11.826 | GET | https://tmx.bestbuy.com/he4MxtWoqBG2d2l2?c0382e3b6c1f28c5=4Q_7DKCVh14oRnd-L_dOl49UrCVPlhe… | 200 OK | — | 114 ms |
| 19:44:11.902 | GET | https://tmx.bestbuy.com/MWTruk3x6_Q-rIRI?b0e1e6531797f334=Rip6VrwQsXykcmYb89QiX1xLIZaqZzb… | 200 OK | — | 99 ms |
| 19:44:11.903 | GET | https://tmx.bestbuy.com/EcBgL_BujtkBGRgJ?6b15ccb08f61b724=7R4LT_znQystUKLnBoYdgQymErB_Dms… | 204 204 | — | 108 ms |
| 19:44:11.975 | GET | blob:https://www.bestbuy.com/0e3f5759-09a9-419e-8006-e1a8727b3e13 | -1 | — | <1 ms |
| 19:44:12.034 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 427 ms |
| 19:44:12.059 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/kDGYzLOQ/d2YKXBFXew4/TD/gwXSZsbmQt | 200 | — | 191 ms |
| 19:44:12.405 | GET | https://tmx.bestbuy.com/MWTruk3x6_Q-rIRI?b0e1e6531797f334=Rip6VrwQsXykcmYb89QiX1xLIZaqZzb… | 200 OK | — | 107 ms |
| 19:44:12.568 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=1&c=2493&i=61xh5d&p=privacy_prod&… | 204 | — | 61 ms |
| 19:44:13.460 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/checkoutSignIn-26db5d0eb… | 200 | — | 111 ms |
| 19:44:13.636 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 304 ms |
| 19:44:13.641 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 285 ms |
| 19:44:13.647 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 339 ms |
| 19:44:13.765 | GET | https://www.bestbuy.com/identity/guest?token=tid%3Ac5b15a3a-5228-11f1-8b3c-12e464dd83f7 | 302 | — | 216 ms |
| 19:44:13.765 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 55 ms |
| 19:44:13.765 | POST | https://tmx.bestbuy.com/jhyeNeyv6FW6vZd8?9d4ab284db00b8a0=lifHxK3wcxcwnCAk02ggi2BdPpvWHMJ… | 200 OK | — | 98 ms |
| 19:44:13.981 | GET | https://www.bestbuy.com/checkout/r/fast-track | 200 | — | 1.03 s |
| 19:44:15.026 | POST | https://tmx.bestbuy.com/EcBgL_BujtkBGRgJ?6b15ccb08f61b724=7R4LT_znQystUKLnBoYdgQymErB_Dms… | -1 | — | <1 ms |
| 19:44:15.026 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | -1 | — | <1 ms |
| 19:44:15.032 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/lodash-v4/4.17.21/dist/lodash.min.js | 200 | — | 1 ms |
| 19:44:15.032 | GET | https://nexus.ensighten.com/bestbuy/privacy_init/Bootstrap.js | 200 | — | 49 ms |
| 19:44:15.032 | GET | https://www.bestbuy.com/~assets/bby/_com/brix/7.5.0/css/brix.css | 200 | — | 169 ms |
| 19:44:15.032 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/lodash/3.6.0/dist/lodash.min.js | 200 | — | 169 ms |
| 19:44:15.032 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/cacheable-gvp-11be6403c8a50adefb4a68bdb5b… | 200 | — | 178 ms |
| 19:44:15.032 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.… | 200 | — | 234 ms |
| 19:44:15.033 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/bestbuy/lib-mf-assets/2.1.2/dist/main.js | 200 | — | 1 ms |
| 19:44:15.033 | GET | https://www.bestbuy.com/~assets/bby/_com/deo-client-script.js | 200 | — | 1 ms |
| 19:44:15.033 | GET | https://www.bestbuy.com/~assets/bby/_com/@ds/unified-chat/dist/javascript/unified-chat-in… | 200 | — | 1 ms |
| 19:44:15.033 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/lib-dai/dist/client/client-089bbe3cbb4e8848… | 200 | — | 1 ms |
| 19:44:15.033 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/3818-f8a2f130f510dc5… | 200 | — | 5 ms |
| 19:44:15.033 | GET | https://www.bestbuy.com/~assets/bby/_com/brix/7.5.0/js/brixRemoteEntry.js | 200 | — | 5 ms |
| 19:44:15.033 | GET | https://img.bbystatic.com/BestBuy_US/store/js/olstmxstatic.js | 200 | — | 134 ms |
| 19:44:15.033 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/legacy-80e96c542168b4a82a78e485b2a038a2.m… | 200 | — | 178 ms |
| 19:44:15.033 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/federation/platformContainerOrchestration… | 200 | — | 233 ms |
| 19:44:15.033 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/staging-fad56d9ad0f78ba1e7124a8ba5213507.… | 200 | — | 235 ms |
| 19:44:15.033 | GET | https://www.bestbuy.com/~assets/bby/_com/runtime.bundle-afcedf9013d3b28b9aed1690e608fdb7.… | 200 | — | 237 ms |
| 19:44:15.033 | GET | https://www.bestbuy.com/~assets/bby/_com/brix/7.5.0/js/brix.js | 200 | — | 237 ms |
| 19:44:15.033 | GET | https://www.bestbuy.com/~assets/bby/_com/optimized.bundle-afcedf9013d3b28b9aed1690e608fdb… | 200 | — | 246 ms |
| 19:44:15.033 | GET | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 200 | — | 260 ms |
| 19:44:15.033 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/evoc-talk_to_us-v1-0… | 200 | — | 286 ms |
| 19:44:15.033 | GET | https://www.bestbuy.com/~assets/bby/_com/Vendors.bundle-afcedf9013d3b28b9aed1690e608fdb7.… | 200 | — | 253 ms |
| 19:44:15.033 | GET | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/kDGYzLOQ/d2YKXBFXew4/TD/gwXSZsbmQt?v… | 200 | — | 431 ms |
| 19:44:15.214 | GET | https://nexus.ensighten.com/bestbuy/privacy_prod_cm_copy/Bootstrap.js | 200 | — | 138 ms |
| 19:44:15.314 | GET | https://www.bestbuy.com/~assets/bby/_com/vendor/federation/platformContainer.11.10.1.js | 200 | — | 101 ms |
| 19:44:15.314 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/cj-page-visits | 200 | — | 644 ms |
| 19:44:15.488 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 53 ms |
| 19:44:15.502 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 51 ms |
| 19:44:15.511 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 52 ms |
| 19:44:15.516 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 57 ms |
| 19:44:15.710 | GET | https://www.bestbuy.com/~assets/bby/_com/brix/7.5.0/5572.dd622a1c59d0870391f1.js | 200 | — | 91 ms |
| 19:44:15.710 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 55 ms |
| 19:44:15.711 | GET | https://www.bestbuy.com/lux.js | 200 | — | 2 ms |
| 19:44:15.711 | GET | https://www.bestbuy.com/~assets/bby/_com/brix/7.5.0/60fb346d82490233081f.woff2 | 200 | — | 147 ms |
| 19:44:15.711 | GET | https://www.bestbuy.com/~assets/bby/_com/brix/7.5.0/2831c370bcd5d8865105.woff2 | 200 | — | 147 ms |
| 19:44:15.711 | GET | https://www.bestbuy.com/~assets/bby/_com/brix/7.5.0/bcd69da2f04aa7a01998.svg | 200 | — | 181 ms |
| 19:44:15.711 | GET | https://www.bestbuy.com/~assets/bby/_com/brix/7.5.0/66a2c9e698c0cda40c44.woff2 | 200 | — | 146 ms |
| 19:44:15.711 | GET | https://www.bestbuy.com/~assets/bby/_img/int/plsvgdef-frontend/svg/GiftIdeas_Line_Sm.svg | 200 | — | 2 ms |
| 19:44:15.711 | GET | https://www.bestbuy.com/~assets/bby/_img/int/plsvgdef-frontend/svg/Caret_Down_Line_Sm.svg | 200 | — | 2 ms |
| 19:44:15.711 | GET | https://www.bestbuy.com/~assets/bby/_img/int/plsvgdef-frontend/svg/Clock_Line_Sm.svg | 200 | — | 117 ms |
| 19:44:15.711 | GET | https://www.bestbuy.com/~assets/bby/_js/ext/bbydyn/dyn_digital_chk.js | 200 | — | 158 ms |
| 19:44:15.711 | GET | https://www.bestbuy.com/~assets/bby/_com/brix/7.5.0/37f8017947c264b8389f.woff2 | 200 | — | 511 ms |
| 19:44:15.711 | GET | https://www.bestbuy.com/site/canopy/component/shop/blue-assist/v1 | 200 | — | 547 ms |
| 19:44:15.712 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/@bestbuy/bby-debug/dist/client/bby-debug-fe… | 200 | — | 2 ms |
| 19:44:15.712 | GET | https://pisces.bbystatic.com/image2/BestBuy_US/images/products/e44a0a67-7842-4cd6-8b23-16… | 200 | — | 128 ms |
| 19:44:15.712 | POST | https://fel-api.prod.browse.bestbuy.com/exception | 200 | — | 66 ms |
| 19:44:15.712 | GET | https://www.bestbuy.com/~assets/bby/_com/3e672dbe85a8af7b903e98bc89131b36.js | 200 | — | 130 ms |
| 19:44:15.782 | GET | https://tmx.bestbuy.com/2xta1w8xm0nxm939.js?xbbb53383ab6yyrv=ummqowa2&9lin7ftcrnxmgix8=2d… | 200 OK | — | 205 ms |
| 19:44:15.805 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 430 ms |
| 19:44:15.831 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/cjc-page-requests | 200 | — | 300 ms |
| 19:44:15.837 | GET | https://www.bestbuy.com/~assets/bby/_com/@ds/unified-chat/dist/javascript/unified-chat-in… | 200 | — | 4 ms |
| 19:44:15.837 | GET | https://www.bestbuy.com/~assets/bby/_com/@ds/unified-chat/dist/javascript/unified-chat-in… | 200 | — | 4 ms |
| 19:44:15.837 | GET | https://www.bestbuy.com/~assets/bby/_com/@ds/unified-chat/dist/javascript/unified-chat-in… | 200 | — | 4 ms |
| 19:44:15.837 | GET | https://www.bestbuy.com/~assets/bby/_com/@ds/unified-chat/dist/javascript/unified-chat-in… | 200 | — | 5 ms |
| 19:44:15.852 | GET | https://www.bestbuy.com/pricing/v1/price/item?salesChannel=LargeView&visitorId=11d61959-6… | 200 | — | 833 ms |
| 19:44:15.854 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/@bestbuy/bby-debug/dist/client/bby-debug-85… | 200 | — | <1 ms |
| 19:44:15.943 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/8216-ceb7eb6f1a3c8c7… | 200 | — | 3 ms |
| 19:44:15.943 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/lib-dai/dist/client/826-089bbe3cbb4e88488ee… | 200 | — | 4 ms |
| 19:44:15.944 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=0&c=2493&i=8n02h2&p=privacy_prod_… | 204 | — | 57 ms |
| 19:44:15.944 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/lib-dai/dist/client/323-089bbe3cbb4e88488ee… | 200 | — | 14 ms |
| 19:44:16.050 | GET | https://www.bestbuy.com/api/tcfb/model.json?paths=%5B%5B%22shop%22%2C%22magellan%22%2C%22… | 200 | — | 521 ms |
| 19:44:16.065 | GET | https://a4091a3a2309.cdn4.forter.com/sn/a4091a3a2309/script.js | 200 | — | 7 ms |
| 19:44:16.067 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/9495-ceb7eb6f1a3c8c7… | 200 | — | 5 ms |
| 19:44:16.067 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/3696-ceb7eb6f1a3c8c7… | 200 | — | 2 ms |
| 19:44:16.068 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/8441-ceb7eb6f1a3c8c7… | 200 | — | 4 ms |
| 19:44:16.068 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/333-ceb7eb6f1a3c8c77… | 200 | — | 4 ms |
| 19:44:16.068 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/1830-ceb7eb6f1a3c8c7… | 200 | — | 4 ms |
| 19:44:16.068 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/8325-ceb7eb6f1a3c8c7… | 200 | — | 4 ms |
| 19:44:16.068 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/7243-ceb7eb6f1a3c8c7… | 200 | — | 5 ms |
| 19:44:16.082 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/analyticsInit-aa713fca754a9e167… | 200 | — | 1 ms |
| 19:44:16.091 | GET | blob:https://www.bestbuy.com/64ac6933-cbd0-4820-b0f1-7aa648ebb3c3 | 200 OK | — | 14 ms |
| 19:44:16.100 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/81-2c54adfeb00efd510480.… | 200 | — | 1 ms |
| 19:44:16.100 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/9557-e656009191eb0108a30… | 200 | — | 1 ms |
| 19:44:16.119 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/sandbox-index-26.16.2.html?pare… | 200 | — | <1 ms |
| 19:44:16.123 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/customer-journal-d87e751… | 200 | — | 1 ms |
| 19:44:16.125 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/5090-ceb7eb6f1a3c8c7… | 200 | — | 1 ms |
| 19:44:16.125 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/814-ceb7eb6f1a3c8c77… | 200 | — | 3 ms |
| 19:44:16.125 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/7754-ceb7eb6f1a3c8c7… | 200 | — | 3 ms |
| 19:44:16.125 | GET | https://www.bestbuy.com/~assets/bby/_com/evoc/talk-to-us/dist/client/3945-ceb7eb6f1a3c8c7… | 200 | — | 4 ms |
| 19:44:16.189 | GET | blob:https://www.bestbuy.com/377cfb28-8dc8-4794-a3bf-c92ea85f0b5d | 200 OK | — | 98 ms |
| 19:44:16.211 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/cj-digital-schema1-2faec… | 200 | — | 1 ms |
| 19:44:16.214 | GET | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 200 | — | 201 ms |
| 19:44:16.214 | GET | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/kDGYzLOQ/d2YKXBFXew4/TD/gwXSZsbmQt?v… | 200 | — | 205 ms |
| 19:44:16.229 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 262 ms |
| 19:44:16.249 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/blue-assist/dist/client/client-1868d6d83328… | 200 | — | 2 ms |
| 19:44:16.250 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/blue-assist/dist/client/client-ba310cf51233… | 200 | — | 1 ms |
| 19:44:16.263 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/platformContainer.2022.11.10.1.js | 200 | — | 5 ms |
| 19:44:16.263 | GET | https://www.bestbuy.com/~assets/bby/_com/brix/7.5.0/js/2509.js | 200 | — | 5 ms |
| 19:44:16.263 | GET | https://www.bestbuy.com/~assets/bby/_com/brix/7.5.0/js/1778.js | 200 | — | 6 ms |
| 19:44:16.263 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/blue-assist/dist/client/8580-1868d6d8332841… | 200 | — | 3 ms |
| 19:44:16.263 | GET | https://www.bestbuy.com/~assets/bby/_com/shop/blue-assist/dist/client/7163-1868d6d8332841… | 200 | — | 6 ms |
| 19:44:16.273 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-2022-vendors-_yarn_cache_react… | 200 | — | <1 ms |
| 19:44:16.273 | GET | https://www.bestbuy.com/~assets/bby/_com/federation/mf-dep-2022-vendors-_yarn___virtual__… | 200 | — | 2 ms |
| 19:44:16.313 | POST | https://www.bestbuy.com/gateway/graphql | -1 | — | <1 ms |
| 19:44:16.448 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 358 ms |
| 19:44:16.485 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/initChildPipeline-688a87c4a5f75… | 200 | — | 1 ms |
| 19:44:16.501 | GET | https://tmx.bestbuy.com/89x-e1rdDzsxaLfT?938290307a22a441=77-5pD4BkYyFkxM6HVYsMukgWZ88Z8G… | 200 OK | — | 376 ms |
| 19:44:16.508 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/confirmIt-245d713c1a9c5a… | 200 | — | 2 ms |
| 19:44:16.508 | GET | https://tmx.bestbuy.com/jTBOIi8u9A9b0P2p?2147e4e204287da0=SPpyK6ILpkiE41WLY5uD5RjEhbBamZ6… | 200 OK | — | 372 ms |
| 19:44:16.509 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/5874-9a107908d934684f83e… | 200 | — | 1 ms |
| 19:44:16.509 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/adobeInit-a2318ff1a8645e… | 200 | — | 1 ms |
| 19:44:16.529 | GET | https://tmx.bestbuy.com/_1IVv5alyt8j1gtL?5a95ab4cb113d828=JUZ-P8E8bpXmo2wqH3A3izWc39hO4PO… | 200 OK | — | 392 ms |
| 19:44:16.551 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/aq-init-6e37ecd8fe344c27… | 200 | — | 1 ms |
| 19:44:16.760 | POST | https://b36b7e0314ba4bb5a2979e1b72285963-a4091a3a2309.cdn.forter.com/prop.json | 200 OK | — | 207 ms |
| 19:44:16.775 | GET | blob:https://www.bestbuy.com/14610cab-fb78-4855-b03b-bb7d3f02100d | -1 | — | <1 ms |
| 19:44:16.809 | GET | blob:https://www.bestbuy.com/4e85c70d-b142-4cab-9edc-86855ecb3578 | -1 | — | <1 ms |
| 19:44:16.839 | GET | https://cdn0.forter.com/a4091a3a2309/b36b7e0314ba4bb5a2979e1b72285963/prop.json?_=1779047… | 200 OK | — | 276 ms |
| 19:44:16.861 | GET | blob:https://www.bestbuy.com/5f4b4fc9-7569-49ba-b272-be73928536f4 | -1 | — | <1 ms |
| 19:44:16.871 | POST | https://cdn3.forter.com/events | 200 | — | 59 ms |
| 19:44:16.904 | GET | https://tmx.bestbuy.com/fp/clear.png | 200 OK | — | 406 ms |
| 19:44:16.904 | GET | https://tmx.bestbuy.com/01gGQdgc3MIh1kFs?70d712d35b8fa36d=fnej79DeWeKVbGfY6JqmHIVebh6cAMG… | 204 204 | — | 405 ms |
| 19:44:16.907 | GET | https://tmx.bestbuy.com/eaNY8WpKfPI-BEWi?c68cb5238e3249e9=1LWxIXOLreKlV1Z99hn6w9bQKeHQJnU… | 200 OK | — | 227 ms |
| 19:44:16.911 | GET | https://tmx.bestbuy.com/01gGQdgc3MIh1kFs?70d712d35b8fa36d=fnej79DeWeKVbGfY6JqmHIVebh6cAMG… | 200 OK | — | 103 ms |
| 19:44:16.911 | GET | https://tmx.bestbuy.com/NZA3T8nIBWDo3yIN?056015223a28b78c=DReIV-Bev6ALrZ2Z4yaDs-7nqToJzpw… | 200 OK | — | 104 ms |
| 19:44:16.913 | GET | https://h64.online-metrix.net/FQS79FQZi_tpw5NV?a550f147521b241a=AQSLMkk4hT1J2G0Fiu9y4hUye… | 200 OK | — | 381 ms |
| 19:44:16.913 | GET | https://tmx.bestbuy.com/nVIhMJZhV3MM16G6?42ccf2e8633688c3=U4U0BL41fBXyzA3zz2hHQOlbOB2TVwU… | 200 OK | — | 211 ms |
| 19:44:16.913 | GET | https://ummqowa26fhed77vwlje5clagyrpliga7pj2b4gv412a6394a4df14desac.d.aa.online-metrix.ne… | 200 OK | — | 529 ms |
| 19:44:16.931 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 396 ms |
| 19:44:16.998 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 623 ms |
| 19:44:17.232 | GET | https://cdn0.forter.com/a4091a3a2309/b36b7e0314ba4bb5a2979e1b72285963/prop.json?_=1779047… | 200 OK | — | 155 ms |
| 19:44:17.242 | POST | https://cdn6.forter.com/a4091a3a2309/b36b7e0314ba4bb5a2979e1b72285963/prop.json | 200 | — | 98 ms |
| 19:44:17.242 | POST | https://b36b7e0314ba4bb5a2979e1b72285963-a4091a3a2309.cdn.forter.com/prop.json | 200 OK | — | 255 ms |
| 19:44:17.282 | GET | https://tmx.bestbuy.com/cqh8GDftRgs-QmuB?6677dbd55f5ea981=zPTGVUsq6ZS-cutEy-xZM597rU4ZsfD… | 200 OK | — | 106 ms |
| 19:44:17.282 | GET | https://tmx.bestbuy.com/CArMlMbmoLW09PPL?82750d3e036aab9e=HDmwHMeQi-swGi--kqReuqvLWn7V7_S… | 200 OK | — | 106 ms |
| 19:44:17.283 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 123 ms |
| 19:44:17.416 | GET | https://cdn0.forter.com/a4091a3a2309/b36b7e0314ba4bb5a2979e1b72285963/prop.json?_=1779047… | 200 OK | — | 132 ms |
| 19:44:17.439 | GET | https://tmx.bestbuy.com/01gGQdgc3MIh1kFs?70d712d35b8fa36d=fnej79DeWeKVbGfY6JqmHIVebh6cAMG… | 200 OK | — | 107 ms |
| 19:44:17.440 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 106 ms |
| 19:44:17.465 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/kDGYzLOQ/d2YKXBFXew4/TD/gwXSZsbmQt | 200 | — | 185 ms |
| 19:44:17.477 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/kDGYzLOQ/d2YKXBFXew4/TD/gwXSZsbmQt | 200 | — | 372 ms |
| 19:44:17.518 | GET | blob:https://www.bestbuy.com/d38e0268-a9d7-4318-9ef5-bc16c54b5f2c | -1 | — | <1 ms |
| 19:44:17.536 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 317 ms |
| 19:44:17.550 | POST | https://cdn0.forter.com/a4091a3a2309/b36b7e0314ba4bb5a2979e1b72285963/wpt.json | 200 OK | — | 97 ms |
| 19:44:17.723 | POST | https://b36b7e0314ba4bb5a2979e1b72285963-a4091a3a2309.cdn.forter.com/prop.json | 200 OK | — | 199 ms |
| 19:44:17.942 | GET | https://tmx.bestbuy.com/01gGQdgc3MIh1kFs?70d712d35b8fa36d=fnej79DeWeKVbGfY6JqmHIVebh6cAMG… | 200 OK | — | 106 ms |
| 19:44:18.333 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=1&c=2493&i=8n02h2&p=privacy_prod_… | 204 | — | 73 ms |
| 19:44:18.333 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=3&c=2493&i=8n02h2&p=privacy_prod_… | 204 | — | 76 ms |
| 19:44:18.333 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=2&c=2493&i=8n02h2&p=privacy_prod_… | 204 | — | 76 ms |
| 19:44:18.380 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 284 ms |
| 19:44:18.507 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 114 ms |
| 19:44:18.509 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 112 ms |
| 19:44:18.571 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 99 ms |
| 19:44:19.144 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 213 ms |
| 19:44:19.148 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/checkout-e762e2e4e0d843b… | 200 | — | 424 ms |
| 19:44:19.149 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/cabo-a90a5fac5066adf3dac… | 200 | — | 424 ms |
| 19:44:19.149 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/thankYou-9679e9ed55fc494… | 200 | — | 423 ms |
| 19:44:19.149 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/payWithPointsCheckout-3f… | 200 | — | 424 ms |
| 19:44:19.719 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 63 ms |
| 19:44:19.845 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 373 ms |
| 19:44:19.946 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/kDGYzLOQ/d2YKXBFXew4/TD/gwXSZsbmQt | 200 | — | 313 ms |
| 19:44:20.000 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 92 ms |
| 19:44:20.020 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 95 ms |
| 19:44:20.021 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 93 ms |
| 19:44:20.147 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 103 ms |
| 19:44:20.503 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 242 ms |
| 19:44:20.838 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=4&c=2493&i=8n02h2&p=privacy_prod_… | 204 | — | 63 ms |
| 19:44:21.216 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 470 ms |
| 19:44:21.500 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 106 ms |
| 19:44:21.528 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 97 ms |
| 19:44:21.528 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 111 ms |
| 19:44:21.652 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 96 ms |
| 19:44:21.747 | POST | https://bf26528hhp.bf.dynatrace.com/bf?type=js3&sn=v_4_srv_28_sn_A1JDCPTI74ISRKR34IA8SVRC… | 200 | — | 81 ms |
| 19:44:21.879 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 248 ms |
| 19:44:22.125 | GET | https://us-autocomplete-pro.api.smarty.com/lookup?key=27601191151557000&max_results=7&sea… | 200 | — | 485 ms |
| 19:44:22.591 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 331 ms |
| 19:44:22.658 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 95 ms |
| 19:44:23.001 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 110 ms |
| 19:44:23.037 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 104 ms |
| 19:44:23.037 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 118 ms |
| 19:44:23.340 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=5&c=2493&i=8n02h2&p=privacy_prod_… | 204 | — | 64 ms |
| 19:44:23.921 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 441 ms |
| 19:44:23.922 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 643 ms |
| 19:44:23.926 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 324 ms |
| 19:44:24.040 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 109 ms |
| 19:44:24.041 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 104 ms |
| 19:44:24.161 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 108 ms |
| 19:44:24.500 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 110 ms |
| 19:44:25.842 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=6&c=2493&i=8n02h2&p=privacy_prod_… | 204 | — | 57 ms |
| 19:44:26.044 | POST | https://www.bestbuy.com/services/conversation/web/api/v1/unified-chat/logger?appVersion=2… | 200 | — | 275 ms |
| 19:44:26.797 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 613 ms |
| 19:44:26.804 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 238 ms |
| 19:44:27.046 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 99 ms |
| 19:44:27.046 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 118 ms |
| 19:44:27.196 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 103 ms |
| 19:44:27.831 | GET | blob:https://www.bestbuy.com/f9c97b30-5c73-48db-a247-d7412341db0d | -1 | — | <1 ms |
| 19:44:27.887 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 368 ms |
| 19:44:27.991 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 368 ms |
| 19:44:28.048 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 112 ms |
| 19:44:28.048 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 118 ms |
| 19:44:28.198 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 102 ms |
| 19:44:28.358 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=7&c=2493&i=8n02h2&p=privacy_prod_… | 204 | — | 63 ms |
| 19:44:28.654 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 227 ms |
| 19:44:29.425 | POST | https://www.bestbuy.com/zKQ0hr/v_Sj/apN/Ae1/ovXeCYsA/acGYzLOQruiJ8m/BVB-WxFXew4/Xh/8zP3tB… | 201 | — | 477 ms |
| 19:44:30.086 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 260 ms |
| 19:44:30.088 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 98 ms |
| 19:44:30.090 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 105 ms |
| 19:44:30.221 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 96 ms |
| 19:44:30.752 | POST | https://streams.bestbuy.com/customer/web-streams/v1/events/digital-experience-event | 200 | — | 224 ms |
| 19:44:30.871 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=8&c=2493&i=8n02h2&p=privacy_prod_… | 204 | — | 59 ms |
| 19:44:31.223 | GET | https://tmx.bestbuy.com/vh3gvfb3BWPy1qea?0598743d0977467e=9zB0fHYq7WAzJFUbTt5I0sCdLQhVD54… | 204 204 | — | 92 ms |
| 19:44:31.228 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/gtagATC-7cfc8330b65e6ea1… | 200 | — | 1 ms |
| 19:44:32.132 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/chunks/csq-e7b417297256d5bf8126… | 200 | — | 129 ms |
| 19:44:32.265 | GET | https://www.bestbuy.com/~assets/bby/_com/analytics-dotcom/vendors/contentsquare/26-8-1/li… | 200 | — | 86 ms |
| 19:44:32.402 | GET | blob:https://www.bestbuy.com/8f50f482-a893-4415-abf8-8a13e3f792e6 | 200 OK | — | 23 ms |
| 19:44:32.414 | GET | https://c.contentsquare.net/pageview?ex=&pvt=n&cvars=%7B%221%22%3A%5B%22pageType%22%2C%22… | 204 | — | 241 ms |
| 19:44:32.429 | GET | https://c.contentsquare.net/dvar?v=13.89.2&pid=1795&pn=1&sn=1&uu=7d408d61-fa3d-af77-8b18-… | 204 | — | 57 ms |
| 19:44:32.439 | POST | https://c.contentsquare.net/display?v=13.89.2&pid=1795&pn=1&sn=1&uu=7d408d61-fa3d-af77-8b… | 204 | — | 220 ms |
| 19:44:33.375 | GET | https://data.privacy.ensighten.com/privacy/v1/b/b.rnc?n=9&c=2493&i=8n02h2&p=privacy_prod_… | 204 | — | 70 ms |

## Console output

- `log` 19:43:37.929 — %cDEO Client SDK color: #fff;background:#000;padding:0.25em  | Returning false, "exp0442" not present in configfile.
- `warning` 19:43:37.929 — document.domain mutation is ignored because the surrounding agent cluster is origin-keyed.
- `error` 19:43:38.454 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `debug` 19:43:38.532 — platformContainerOrchestrationProxyLoaded
- `warning` 19:43:38.789 — Warning: fragment with name BuyingOptions already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:39.604 — Warning: fragment with name CustomerInfo already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:39.612 — Warning: fragment with name Customer_Fragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `error` 19:43:39.631 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `info` 19:43:39.672 — 2026-05-17T19:43:39.001Z logLevel=INFO, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=GRAPHQL, clientId=homepage-web, url=/gateway/graphql, batchInterval=50, batchSize=20, logMessage="GraphQL client details"
- `info` 19:43:39.672 — 2026-05-17T19:43:39.001Z logLevel=INFO, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=browser-logger, logLevel=undefined, forceLog=undefined, logMessage="Fetching internal bby apollo client config"
- `warning` 19:43:39.672 — 2026-05-17T19:43:39.002Z logLevel=WARN, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=browser-logger, clientId=homepage-web, response={"errors":[{"message":"Failed to fetch","networkError":{},"extensions":{"response":{"status"…
- `error` 19:43:39.909 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `info` 19:43:40.464 — 2026-05-17T19:43:40.002Z logLevel=INFO, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=browser-logger, logLevel=undefined, forceLog=undefined, logMessage="Fetching internal bby apollo client config"
- `info` 19:43:40.464 — 2026-05-17T19:43:40.003Z logLevel=INFO, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=browser-logger, Managed Content Applications="CJ Analytics", logMessage="CJ SDK initialized"
- `warning` 19:43:40.464 — 2026-05-17T19:43:40.003Z logLevel=WARN, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=browser-logger, clientId=homepage-web, response={"errors":[{"message":"Failed to fetch","networkError":{},"extensions":{"response":{"status"…
- `warning` 19:43:40.464 — 2026-05-17T19:43:40.003Z logLevel=WARN, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=browser-logger, clientId=homepage-web, logMessage="Attempting to run fulfillment link without config. Defaulting to off."
- `debug` 19:43:40.576 — Error
- `log` 19:43:40.597 — CJ Capture SDK - Composed Event: {contract: Array(1), identities: Object, source: Object, appState: Object, basket: Object}
- `error` 19:43:40.610 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `endGroup` 19:43:40.714 — {}
- `info` 19:43:40.859 — ZodError: [ ⏎   { ⏎     "code": "invalid_type", ⏎     "expected": "object", ⏎     "received": "undefined", ⏎     "path": [], ⏎     "message": "Required" ⏎   } ⏎ ] ⏎     at get error (https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/4420-5279598c221a3883.js:2665:653555) …
- `error` 19:43:40.859 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:40.861 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:40.863 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:40.863 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:40.883 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:40.890 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:40.898 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:40.908 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `log` 19:43:41.009 — [AskBlue][web][info] ConfigRepository: cache read {event.id: ASK_BLUE:CONFIG:REPOSITORY_READ, event.domain: repository, event.outcome: miss, operation.name: repository.config.get_config, operation.duration_ms: 636}
- `log` 19:43:41.009 — [AskBlue][web][info] ConfigManager: repository cache read {event.id: ASK_BLUE:CONFIG:CACHE_READ, event.domain: manager, event.outcome: miss, operation.name: manager.config.cache_read, operation.duration_ms: 637}
- `warning` 19:43:41.014 — 2026-05-17T19:43:41.003Z logLevel=WARN, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=browser-logger, clientId=homepage-web, repeatGroupId=mpa6nuem-0002, repeatCount=8, logMessage="Attempting to run fulfillment link without co…
- `info` 19:43:41.029 — ZodError: [ ⏎   { ⏎     "code": "invalid_type", ⏎     "expected": "object", ⏎     "received": "undefined", ⏎     "path": [], ⏎     "message": "Required" ⏎   } ⏎ ] ⏎     at get error (https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/4420-5279598c221a3883.js:2665:653555) …
- `info` 19:43:41.036 — 2026-05-17T19:43:41.005Z logLevel=INFO, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=AskBlue, logLevel=undefined, forceLog=undefined, logMessage="ConfigRepository: cache read {\"event.id\":\"ASK_BLUE:CONFIG:REPOSITORY_READ\",…
- `info` 19:43:41.036 — 2026-05-17T19:43:41.006Z logLevel=INFO, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=AskBlue, logLevel=undefined, forceLog=undefined, logMessage="ConfigManager: repository cache read {\"event.id\":\"ASK_BLUE:CONFIG:CACHE_READ…
- `warning` 19:43:41.036 — 2026-05-17T19:43:41.006Z logLevel=WARN, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=browser-logger, clientId=homepage-web, logMessage="Attempting to run fulfillment link without config. Defaulting to off."
- `error` 19:43:41.036 — 2026-05-17T19:43:41.006Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=GRAPHQL-LINK, clientId=homepage-web, linkName=networkErrorLink, operationName=Header_GlobalNavData, headersInContext={"X-Client-Id":"homepa…
- `log` 19:43:41.057 — %cDEO Client SDK color: #fff;background:#000;padding:0.25em  | Returning false, "exp0347" not present in configfile.
- `log` 19:43:41.057 — %cDEO Client SDK color: #fff;background:#000;padding:0.25em  | Returning false, "exp0306" not present in configfile.
- `log` 19:43:41.057 — %cDEO Client SDK color: #fff;background:#000;padding:0.25em  | Returning false, "exp0510" not present in configfile.
- `warning` 19:43:41.066 — 2026-05-17T19:43:41.006Z logLevel=WARN, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=browser-logger, clientId=homepage-web, logMessage="Attempting to run fulfillment link without config. Defaulting to off."
- `error` 19:43:41.066 — 2026-05-17T19:43:41.006Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=GRAPHQL-LINK, clientId=homepage-web, linkName=networkErrorLink, operationName=getPlatmanContentByNodeId, headersInContext={"X-Client-Id":"h…
- `error` 19:43:41.067 — 2026-05-17T19:43:41.007Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=GRAPHQL-LINK, clientId=homepage-web, linkName=networkErrorLink, operationName=BatchedPlpConfigAndSmartSearchSuggest, headersInContext={"X-C…
- `error` 19:43:41.068 — 2026-05-17T19:43:41.007Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=GRAPHQL-LINK, clientId=homepage-web, linkName=networkErrorLink, operationName=GetLocationTooltipMessaging, headersInContext={"X-Client-Id":…
- `error` 19:43:41.068 — 2026-05-17T19:43:41.007Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=GRAPHQL-LINK, clientId=homepage-web, linkName=networkErrorLink, operationName=CustomerData, headersInContext={"X-Client-Id":"homepage-web",…
- `error` 19:43:41.075 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `info` 19:43:41.141 — ZodError: [ ⏎   { ⏎     "code": "invalid_type", ⏎     "expected": "object", ⏎     "received": "undefined", ⏎     "path": [], ⏎     "message": "Required" ⏎   } ⏎ ] ⏎     at get error (https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/4420-5279598c221a3883.js:2665:653555) …
- `error` 19:43:41.226 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:41.242 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `warning` 19:43:41.274 — [AskBlue][web][warn] ConfigApiService: empty config document {event.id: ASK_BLUE:CONFIG:FETCH, event.domain: service, event.outcome: empty, operation.name: service.config.graphql.fetch, operation.duration_ms: 265}
- `error` 19:43:41.276 — 2026-05-17T19:43:41.006Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=GRAPHQL-LINK, clientId=homepage-web, linkName=networkErrorLink, operationName=AppConfig, headersInContext={"X-Client-Id":"homepage-web","X-…
- `error` 19:43:41.276 — 2026-05-17T19:43:41.006Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=GRAPHQL-LINK, clientId=homepage-web, linkName=networkErrorLink, operationName=ConfigData_Init, headersInContext={"X-Client-Id":"homepage-we…
- `error` 19:43:41.276 — 2026-05-17T19:43:41.006Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=GRAPHQL-LINK, clientId=homepage-web, linkName=networkErrorLink, operationName=personalized_home_query_for_story_flexible_messages_story_one…
- `error` 19:43:41.276 — 2026-05-17T19:43:41.007Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=GRAPHQL-LINK, clientId=homepage-web, linkName=networkErrorLink, operationName=personalized_home_query_for_story_top_deals_story_v2_action_t…
- `error` 19:43:41.277 — 2026-05-17T19:43:41.007Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=GRAPHQL-LINK, clientId=homepage-web, linkName=networkErrorLink, operationName=managedContentByTypeAndId, headersInContext={"X-Client-Id":"h…
- `info` 19:43:41.283 — ZodError: [ ⏎   { ⏎     "code": "invalid_type", ⏎     "expected": "object", ⏎     "received": "undefined", ⏎     "path": [], ⏎     "message": "Required" ⏎   } ⏎ ] ⏎     at get error (https://www.bestbuy.com/~assets/bby/_com/bestbuy/homepage/_next/static/chunks/4420-5279598c221a3883.js:2665:653555) …
- `log` 19:43:41.303 — [AskBlue][web][info] ConfigRepository: config saved {event.id: ASK_BLUE:CONFIG:REPOSITORY_WRITE, event.domain: repository, event.outcome: success, operation.name: repository.config.save_config, operation.duration_ms: 28}
- `log` 19:43:41.304 — [AskBlue][web][info] ConfigManager: server fetch complete {event.id: ASK_BLUE:CONFIG:REFRESH, event.domain: manager, event.outcome: success, operation.name: manager.config.refresh, operation.duration_ms: 294}
- `log` 19:43:41.304 — [AskBlue][web][info] configVisibility: synced platform config {source: server, platform: web, requestKey: web:anonymous, shouldRender: false, hasPlatformConfig: true}
- `warning` 19:43:41.478 — 2026-05-17T19:43:41.009Z logLevel=WARN, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=AskBlue, logLevel=undefined, forceLog=undefined, logMessage="ConfigApiService: empty config document {\"event.id\":\"ASK_BLUE:CONFIG:FETCH\"…
- `error` 19:43:41.479 — 2026-05-17T19:43:41.009Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=GRAPHQL-LINK, clientId=homepage-web, linkName=networkErrorLink, operationName=customerVisitorOfferQuery, headersInContext={"X-Client-Id":"v…
- `info` 19:43:41.479 — 2026-05-17T19:43:41.009Z logLevel=INFO, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=AskBlue, logLevel=undefined, forceLog=undefined, logMessage="ConfigRepository: config saved {\"event.id\":\"ASK_BLUE:CONFIG:REPOSITORY_WRITE…
- `info` 19:43:41.479 — 2026-05-17T19:43:41.009Z logLevel=INFO, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=AskBlue, logLevel=undefined, forceLog=undefined, logMessage="ConfigManager: server fetch complete {\"event.id\":\"ASK_BLUE:CONFIG:REFRESH\",…
- `info` 19:43:41.479 — 2026-05-17T19:43:41.009Z logLevel=INFO, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=AskBlue, logLevel=undefined, forceLog=undefined, logMessage="configVisibility: synced platform config {\"source\":\"server\",\"platform\":\"…
- `error` 19:43:41.669 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:42.039 — Failed to load resource: net::ERR_NAME_NOT_RESOLVED
- `warning` 19:43:42.976 — TypeError: Cannot set properties of null (setting 'href') ⏎     at doStuff (eval at <anonymous> (https://www.bestbuy.com/~assets/bby/_com/shop/stips/dist/client/109-8d41dfb3ae61238f1c8715ac8641b1bc.js:1:5212), <anonymous>:18:22) ⏎     at documentReadyCheck (eval at <anonymous> (https://www.bestbuy.…
- `info` 19:43:43.674 — 2026-05-17T19:43:43.003Z logLevel=INFO, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger=browser-logger, Managed Content Applications="CJ Analytics", logMessage="CJ SDK initialized"
- `error` 19:43:43.674 — 2026-05-17T19:43:43.003Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, ut=undefined, logger="HomePage - GHP", logMessage="[BBY SW] Error fetching experiment data: {}"
- `log` 19:43:45.305 — %cDEO Client SDK color: #fff;background:#000;padding:0.25em  | Returning false, "exp0338" not present in configfile.
- `warning` 19:43:45.305 — document.domain mutation is ignored because the surrounding agent cluster is origin-keyed.
- `error` 19:43:45.596 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `debug` 19:43:45.891 — platformContainerOrchestrationProxyLoaded
- `warning` 19:43:46.180 — Warning: fragment with name BuyingOptions already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `log` 19:43:46.208 — EkoAnalytics is not defined, initializing a no-op function...
- `warning` 19:43:46.242 — Warning: fragment with name ManagedContentFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.246 — Warning: fragment with name ProductPriceFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.247 — Warning: fragment with name ProductPriceFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.334 — Warning: fragment with name Pricing already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.334 — Warning: fragment with name Products already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `error` 19:43:46.471 — getting logger for env: 2 logLevel: warn
- `debug` 19:43:46.472 — [Apollo Version Detector] {source: @apollo/client, detectedVersion: 4, VERSION: undefined, hasStableUseSuspenseQuery: true, hasExperimentalSuspenseQuery: false}
- `warning` 19:43:46.479 — Warning: fragment with name BsinBuyingOptionsFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.632 — Warning: fragment with name ConfigFields already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.632 — Warning: fragment with name VisitorFields already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.632 — Warning: fragment with name PlanPaidMemberEventsFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.632 — Warning: fragment with name DropEventsFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.642 — Warning: fragment with name PlpViewStoreInfo already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.642 — Warning: fragment with name PlpViewCobaltInfo already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.642 — Warning: fragment with name Customer_Fragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.642 — Warning: fragment with name ProductCategoryFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.649 — Warning: fragment with name PlpView_BadgesFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.649 — Warning: fragment with name PlpView_BadgesV2Fragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.649 — Warning: fragment with name ComboBadgesFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.649 — Warning: fragment with name FulfillmentGetItFastOptionsFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.649 — Warning: fragment with name ListingBannerFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.649 — Warning: fragment with name SearchProductFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.649 — Warning: fragment with name SearchComboFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.649 — Warning: fragment with name PlpViewSearchMediaProductFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.649 — Warning: fragment with name PlpViewStoreDataWithLocationConnectionFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.649 — Warning: fragment with name PlpViewSearchProductInfoFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.649 — Warning: fragment with name PlpViewDocumentsListViewFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.649 — Warning: fragment with name PlpViewDocumentsGridViewFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.649 — Warning: fragment with name PlpViewDisplayDocumentsFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.649 — Warning: fragment with name AppleIntelligenceProductFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.650 — Warning: fragment with name FullfillmentProductBySkuIdFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.650 — Warning: fragment with name MpFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.650 — Warning: fragment with name FullfillmentOptionsFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.650 — Warning: fragment with name ButtonStatesFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.650 — Warning: fragment with name ShippingDetailsFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.650 — Warning: fragment with name DeliveryDetailsFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.650 — Warning: fragment with name IspuDetailsFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.650 — Warning: fragment with name IspuAvailabilityFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.650 — Warning: fragment with name IspuStoreFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name ReviewStats_Fragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name BSIN_FRAGMENT_PLP_DATA already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name BadgeV2Minimal already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name BadgeV2 already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name MarketplaceFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name ProductPriceFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name PriceExperienceInit_Product already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name PriceBlockInit_Product already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name PriceBlockInit_ItemPrice already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name ConditionalTapForPrice_ItemPrice already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name Header_ItemPrice already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name TopPriceMessage_ItemPrice already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name DealAlert_ItemPrice already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name CustomerPrice_ItemPrice already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name Savings_ItemPrice already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name BottomPriceMessage_ItemPrice already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name FinanceOptions_ItemPrice already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name PaymentOptions_ItemPrice already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name Footer_ItemPrice already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name ExperimentsInit_Product already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name ExperimentsInit_ItemPrice already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name TieredOffersTrackingInit_Product already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name TieredOffersTrackingInit_ItemPrice already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name PlusXOffersGateInit_Product already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name PlusXOffersGateInit_ItemPrice already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name MembershipUpsellInit_Product already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name MembershipUpsellInit_ItemPrice already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name EcoRebatesInit_Product already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name EcoRebatesInit_ItemPrice already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.651 — Warning: fragment with name SpendAndGetInit_Product already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.652 — Warning: fragment with name SpendAndGetInit_ItemPrice already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.652 — Warning: fragment with name CaboSucoInit_Product already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.652 — Warning: fragment with name CaboSucoInit_ItemPrice already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.652 — Warning: fragment with name GiftWithPurchaseInit_Product already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.652 — Warning: fragment with name GiftWithPurchaseInit_ItemPrice already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.652 — Warning: fragment with name OffersInit_Product already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.652 — Warning: fragment with name OffersInit_SkuOffersConnection already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.652 — Warning: fragment with name OffersInit_SkuOffer already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.652 — Warning: fragment with name PromotionalOptionListInit_Product already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.652 — Warning: fragment with name FinanceOptionsInit_ItemPrice already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.652 — Warning: fragment with name NotifyMe_ProductBySkuId already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.652 — Warning: fragment with name PlpViewInboundMarketplaceProductVariationFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.652 — Warning: fragment with name PlpViewSharedProductVariationFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.652 — Warning: fragment with name DetailedSearchProductFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.652 — Warning: fragment with name PlpView_SearchCommonFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.652 — Warning: fragment with name PlpView_SearchInitFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.652 — Warning: fragment with name MarketplaceSellerFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.652 — Warning: fragment with name SiteControlNodeDataFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.659 — Warning: fragment with name ProductListItemFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.659 — Warning: fragment with name AppleIntelligenceProductFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.659 — Warning: fragment with name MarketplaceFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.660 — Warning: fragment with name PlpViewInboundMarketplaceProductVariationFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:43:46.723 — Warning: fragment with name ManagedContentFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `error` 19:43:46.821 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:46.845 — Error triggering event 'pageLoad' for Tag 'adobeDcoPdpCategory': Error: Cannot find module './adobeDcoPdpCategory/index' [GOTEAM, MultiTenant, eventTrigger, pageLoad]
- `log` 19:43:46.919 — Truncating agent event because the size for property [hint] exceeds size limit of 100 characters: [1068]
- `debug` 19:43:47.005 — Error
- `endGroup` 19:43:47.044 — {}
- `error` 19:43:47.266 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `warning` 19:43:47.295 — Warning: fragment with name ProductListItemFragment already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `log` 19:43:47.425 — Rendering SheetContent with currentView: undefined []
- `log` 19:43:47.437 — setUserId undefined
- `log` 19:43:47.437 — setEnvironment dotcom_prod
- `log` 19:43:47.438 — setIsBot false
- `log` 19:43:47.438 — setPerfTestFlag false
- `log` 19:43:47.438 — setAttributes [Object, Object, Object, Object, Object]
- `log` 19:43:47.438 — setAllowListUserId undefined
- `debug` 19:43:47.450 — Headers not available in current context: Error: `headers` was called outside a request scope. Read more: https://nextjs.org/docs/messages/next-dynamic-api-wrong-context ⏎     at o (https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/2364-302376caa88aa8c6.js:1:37470) ⏎     at d (h…
- `debug` 19:43:47.472 — Config loading completed
- `debug` 19:43:47.472 — Plp Config loading completed
- `log` 19:43:47.871 — Rendering SheetContent with currentView: undefined []
- `log` 19:43:47.934 — Rendering SheetContent with currentView: undefined []
- `log` 19:43:47.996 — Rendering SheetContent with currentView: undefined []
- `log` 19:43:48.058 — Rendering SheetContent with currentView: undefined []
- `log` 19:43:48.134 — Rendering SheetContent with currentView: undefined []
- `log` 19:43:48.247 — Rendering SheetContent with currentView: undefined []
- `warning` 19:43:48.291 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.304 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.307 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `log` 19:43:48.393 — Rendering SheetContent with currentView: undefined []
- `warning` 19:43:48.420 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.424 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.425 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:48.444 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.445 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.445 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `log` 19:43:48.483 — Rendering SheetContent with currentView: undefined []
- `warning` 19:43:48.497 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.500 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.500 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:48.527 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.529 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.530 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:48.547 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.550 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.550 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `log` 19:43:48.603 — Rendering SheetContent with currentView: undefined []
- `warning` 19:43:48.622 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.625 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.626 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:48.643 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.646 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.646 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:48.663 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.665 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.666 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:48.688 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.694 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.695 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `log` 19:43:48.752 — Rendering SheetContent with currentView: undefined []
- `warning` 19:43:48.766 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.768 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.768 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:48.778 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.780 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.780 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:48.795 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.797 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.797 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:48.807 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.812 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.812 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `log` 19:43:48.890 — Rendering SheetContent with currentView: undefined []
- `warning` 19:43:48.904 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.906 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.906 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:48.925 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.927 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.928 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:48.960 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.964 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.965 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:48.985 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.990 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:48.990 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `log` 19:43:49.058 — Rendering SheetContent with currentView: undefined []
- `warning` 19:43:49.068 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.071 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.071 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:49.096 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.098 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.099 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:49.112 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.114 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.114 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:49.127 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.132 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.132 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `log` 19:43:49.187 — Rendering SheetContent with currentView: undefined []
- `warning` 19:43:49.216 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.224 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.225 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:49.262 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.268 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.269 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:49.304 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.309 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.309 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:49.334 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.339 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.340 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `log` 19:43:49.442 — Rendering SheetContent with currentView: undefined []
- `warning` 19:43:49.455 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.459 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.459 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:49.473 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.474 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.475 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:49.495 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.496 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.496 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:49.506 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.509 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.509 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `log` 19:43:49.572 — Rendering SheetContent with currentView: undefined []
- `warning` 19:43:49.586 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.589 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.589 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:49.612 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.614 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.614 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:49.631 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.633 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.634 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:49.648 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.652 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.652 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `log` 19:43:49.727 — Rendering SheetContent with currentView: undefined []
- `warning` 19:43:49.738 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.739 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.740 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:49.754 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.757 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.757 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:49.774 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.775 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.776 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:49.790 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.795 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.795 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `log` 19:43:49.836 — Rendering SheetContent with currentView: undefined []
- `warning` 19:43:49.842 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.843 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.844 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:49.859 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.861 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.862 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:49.886 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.889 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.889 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:49.918 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.924 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:49.925 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `log` 19:43:49.987 — Rendering SheetContent with currentView: undefined []
- `warning` 19:43:49.999 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.002 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.002 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:50.022 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.025 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.025 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:50.039 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.041 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.041 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:50.056 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.060 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.060 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `log` 19:43:50.122 — Rendering SheetContent with currentView: undefined []
- `warning` 19:43:50.132 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.133 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.133 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:50.142 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.143 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.143 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:50.155 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.157 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.157 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:50.165 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.167 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.167 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `log` 19:43:50.215 — Rendering SheetContent with currentView: undefined []
- `warning` 19:43:50.226 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.228 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.228 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:50.243 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.245 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.245 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:50.257 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.266 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.267 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:50.283 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.287 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.287 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `log` 19:43:50.340 — Rendering SheetContent with currentView: undefined []
- `warning` 19:43:50.352 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.353 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.354 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:50.378 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.380 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.380 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:50.394 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.396 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.396 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:50.409 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.412 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.412 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `log` 19:43:50.474 — Rendering SheetContent with currentView: undefined []
- `warning` 19:43:50.482 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.484 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.484 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:50.499 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.500 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.500 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:50.509 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.510 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.510 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:50.523 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.526 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.527 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `log` 19:43:50.586 — Rendering SheetContent with currentView: undefined []
- `warning` 19:43:50.599 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.601 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.602 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:50.619 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.622 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.622 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:50.637 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.638 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.639 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:50.663 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.667 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.667 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `log` 19:43:50.733 — setUserId undefined
- `log` 19:43:50.733 — setEnvironment dotcom_prod
- `log` 19:43:50.734 — setIsBot false
- `log` 19:43:50.734 — setPerfTestFlag false
- `log` 19:43:50.734 — setAttributes []
- `log` 19:43:50.734 — setAllowListUserId undefined
- `log` 19:43:50.766 — Rendering SheetContent with currentView: undefined []
- `warning` 19:43:50.776 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.778 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.778 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:50.799 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.801 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.801 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:50.809 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.811 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.811 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:50.824 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.826 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:50.826 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `log` 19:43:50.839 — setUserId undefined
- `log` 19:43:50.839 — setEnvironment dotcom_prod
- `log` 19:43:50.839 — setIsBot false
- `log` 19:43:50.839 — setPerfTestFlag false
- `log` 19:43:50.839 — setAttributes []
- `log` 19:43:50.839 — setAllowListUserId undefined
- `log` 19:43:50.849 — %cDEO Client SDK color: #fff;background:#000;padding:0.25em  | Returning false, exp0507 not present in dotcom_Prod_bby_dotcom_53F42C3.
- `log` 19:43:50.849 — %cDEO Client SDK color: #fff;background:#000;padding:0.25em  | Returning false, exp0347 not present in dotcom_Prod_bby_dotcom_53F42C3.
- `log` 19:43:50.849 — %cDEO Client SDK color: #fff;background:#000;padding:0.25em  | Returning false, exp0306 not present in dotcom_Prod_bby_dotcom_53F42C3.
- `log` 19:43:50.849 — %cDEO Client SDK color: #fff;background:#000;padding:0.25em  | Returning false, exp0510 not present in dotcom_Prod_bby_dotcom_53F42C3.
- `log` 19:43:50.851 — %cDEO Client SDK color: #fff;background:#000;padding:0.25em  | Returning false, exp0507 not present in dotcom_Prod_bby_dotcom_53F42C3.
- `log` 19:43:50.851 — %cDEO Client SDK color: #fff;background:#000;padding:0.25em  | Returning false, exp0507 not present in dotcom_Prod_bby_dotcom_53F42C3.
- `log` 19:43:50.855 — setUserId undefined
- `log` 19:43:50.856 — setEnvironment dotcom_prod
- `log` 19:43:50.856 — setIsBot false
- `log` 19:43:50.856 — setPerfTestFlag false
- `log` 19:43:50.856 — setAttributes [Object, Object, Object, Object, Object]
- `log` 19:43:50.856 — setAllowListUserId undefined
- `log` 19:43:50.856 — setUserId undefined
- `log` 19:43:50.856 — setEnvironment dotcom_prod
- `log` 19:43:50.856 — setIsBot false
- `log` 19:43:50.856 — setPerfTestFlag false
- `log` 19:43:50.856 — setAttributes []
- `log` 19:43:50.856 — setAllowListUserId undefined
- `log` 19:43:50.856 — setUserId undefined
- `log` 19:43:50.856 — setEnvironment dotcom_prod
- `log` 19:43:50.857 — setIsBot false
- `log` 19:43:50.857 — setPerfTestFlag false
- `log` 19:43:50.857 — setAttributes []
- `log` 19:43:50.857 — setAllowListUserId undefined
- `log` 19:43:50.857 — %cDEO Client SDK color: #fff;background:#000;padding:0.25em  | Returning false, exp0464 not present in dotcom_Prod_bby_dotcom_53F42C3.
- `log` 19:43:50.857 — %cDEO Client SDK color: #fff;background:#000;padding:0.25em  | Returning false, exp0464 not present in dotcom_Prod_bby_dotcom_53F42C3.
- `log` 19:43:50.858 — %cDEO Client SDK color: #fff;background:#000;padding:0.25em  | Returning false, exp0464 not present in dotcom_Prod_bby_dotcom_53F42C3.
- `log` 19:43:50.858 — setUserId undefined
- `log` 19:43:50.858 — setEnvironment dotcom_prod
- `log` 19:43:50.858 — setIsBot false
- `log` 19:43:50.858 — setPerfTestFlag false
- `log` 19:43:50.858 — setAttributes [Object, Object, Object, Object, Object]
- `log` 19:43:50.858 — setAllowListUserId undefined
- `log` 19:43:50.858 — setUserId undefined
- `log` 19:43:50.858 — setEnvironment dotcom_prod
- `log` 19:43:50.858 — setIsBot false
- `log` 19:43:50.858 — setPerfTestFlag false
- `log` 19:43:50.858 — setAttributes []
- `log` 19:43:50.858 — setAllowListUserId undefined
- `log` 19:43:50.859 — setUserId undefined
- `log` 19:43:50.859 — setEnvironment dotcom_prod
- `log` 19:43:50.859 — setIsBot false
- `log` 19:43:50.859 — setPerfTestFlag false
- `log` 19:43:50.859 — setAttributes []
- `log` 19:43:50.859 — setAllowListUserId undefined
- `log` 19:43:50.859 — %cDEO Client SDK color: #fff;background:#000;padding:0.25em  | Returning false, exp0514 not present in dotcom_Prod_bby_dotcom_53F42C3.
- `log` 19:43:50.859 — %cDEO Client SDK color: #fff;background:#000;padding:0.25em  | Returning false, exp0514 not present in dotcom_Prod_bby_dotcom_53F42C3.
- `log` 19:43:50.859 — %cDEO Client SDK color: #fff;background:#000;padding:0.25em  | Returning false, exp0514 not present in dotcom_Prod_bby_dotcom_53F42C3.
- `log` 19:43:50.904 — CJ Capture SDK - Composed Event: {contract: Array(1), identities: Object, source: Object, appState: Object, basket: Object}
- `error` 19:43:50.910 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `log` 19:43:51.037 — Rendering SheetContent with currentView: undefined []
- `warning` 19:43:51.046 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.048 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.048 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:51.079 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.082 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.082 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:51.101 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.104 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.104 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:51.120 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.122 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.122 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `log` 19:43:51.181 — Rendering SheetContent with currentView: undefined []
- `warning` 19:43:51.186 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.187 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.187 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:51.200 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.201 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.201 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:51.216 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.224 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.224 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:51.238 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.241 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.241 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `log` 19:43:51.348 — Rendering SheetContent with currentView: undefined []
- `warning` 19:43:51.348 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.348 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.348 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:51.365 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.368 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.368 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:51.387 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.390 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.391 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:51.407 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.410 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.410 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:51.446 — [1:183632] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"6646419","errorContextName":"more-buying-options-plp","level":"WARN","message":"MPX | more-buying-options-plp | l | more-buying-options-…
- `warning` 19:43:51.450 — [1:183632] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"6646420","errorContextName":"more-buying-options-plp","level":"WARN","message":"MPX | more-buying-options-plp | l | more-buying-options-…
- `warning` 19:43:51.452 — [1:183632] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"6601524","errorContextName":"more-buying-options-plp","level":"WARN","message":"MPX | more-buying-options-plp | l | more-buying-options-…
- `warning` 19:43:51.455 — [1:183632] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"6601553","errorContextName":"more-buying-options-plp","level":"WARN","message":"MPX | more-buying-options-plp | l | more-buying-options-…
- `error` 19:43:51.612 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:51.612 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:51.612 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:51.612 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:51.612 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:51.613 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `warning` 19:43:51.625 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.633 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.642 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:51.642 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.646 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.647 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:51.648 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.652 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.653 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:51.654 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.657 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:51.658 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `error` 19:43:51.786 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:51.789 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:51.841 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:51.842 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:51.854 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:51.857 — [Report Only] Refused to frame 'https://www.google.com/' because an ancestor violates the following Content Security Policy directive: "frame-ancestors 'self'". ⏎ 
- `log` 19:43:51.864 — [AskBlue][web][info] ConfigRepository: cache read {event.id: ASK_BLUE:CONFIG:REPOSITORY_READ, event.domain: repository, event.outcome: hit, operation.name: repository.config.get_config, operation.duration_ms: 569}
- `log` 19:43:51.864 — [AskBlue][web][info] ConfigManager: repository cache read {event.id: ASK_BLUE:CONFIG:CACHE_READ, event.domain: manager, event.outcome: hit, operation.name: manager.config.cache_read, operation.duration_ms: 569}
- `log` 19:43:51.865 — [AskBlue][web][info] configVisibility: synced platform config {source: cache, platform: web, requestKey: web:anonymous, shouldRender: false, hasPlatformConfig: true}
- `log` 19:43:51.951 — Rendering SheetContent with currentView: undefined []
- `log` 19:43:51.956 — true CustomEvent true function dispatchEvent() { [native code] } {appState: Object, listResult: Object, skus: Array(18), search: Object, decisions: Array(6)} SHOULD WE MAKE THE PAGE LOAD CALL?
- `log` 19:43:51.956 — DISPATCHING PAGE LOAD EVENT function dispatchEvent() { [native code] }
- `log` 19:43:51.991 — Rendering SheetContent with currentView: undefined []
- `warning` 19:43:52.003 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:52.007 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:52.007 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:52.024 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:52.026 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:52.027 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:52.042 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:52.045 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:52.045 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `warning` 19:43:52.072 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:52.077 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:52.092 — DEO feature "exp0481" enabled but no matching recipe in experiments: undefined. Falling back to CONTROL.
- `error` 19:43:52.204 — 2026-05-17T19:43:52.003Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=Header_GlobalNavData, errorDetails="{\"name\":\"ServerError\",\"response\":{},\"…
- `error` 19:43:52.204 — 2026-05-17T19:43:52.004Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=ProductListHierarchy_Init, errorDetails="{\"name\":\"ServerError\",\"response\":…
- `error` 19:43:52.204 — 2026-05-17T19:43:52.004Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=IntentData_Init, errorDetails="{\"name\":\"ServerError\",\"response\":{},\"statu…
- `error` 19:43:52.205 — 2026-05-17T19:43:52.005Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=AppConfig, errorDetails="{\"name\":\"ServerError\",\"response\":{},\"statusCode\…
- `error` 19:43:52.205 — 2026-05-17T19:43:52.005Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=getPLPSearchProductBySkuId, errorDetails="{\"name\":\"ServerError\",\"response\"…
- `warning` 19:43:52.219 — PLP_LOAD span events are deprecated
- `error` 19:43:52.219 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:52.265 — 2026-05-17T19:43:52.004Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=GetLocationTooltipMessaging, errorDetails="{\"name\":\"ServerError\",\"response\…
- `error` 19:43:52.265 — 2026-05-17T19:43:52.005Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=PlpView_ProductListItem_Init, errorDetails="{\"name\":\"ServerError\",\"response…
- `error` 19:43:52.265 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:52.266 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:52.333 — 2026-05-17T19:43:52.003Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=PlpView_ProductListItem_Init, errorDetails="{\"name\":\"ServerError\",\"response…
- `error` 19:43:52.333 — 2026-05-17T19:43:52.003Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=CustomerData, errorDetails="{\"name\":\"ServerError\",\"response\":{},\"statusCo…
- `error` 19:43:52.341 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `warning` 19:43:52.418 — [AskBlue][web][warn] ConfigApiService: empty config document {event.id: ASK_BLUE:CONFIG:FETCH, event.domain: service, event.outcome: empty, operation.name: service.config.graphql.fetch, operation.duration_ms: 554}
- `log` 19:43:52.562 — [AskBlue][web][info] ConfigRepository: config saved {event.id: ASK_BLUE:CONFIG:REPOSITORY_WRITE, event.domain: repository, event.outcome: success, operation.name: repository.config.save_config, operation.duration_ms: 143}
- `log` 19:43:52.564 — [AskBlue][web][info] ConfigManager: server fetch complete {event.id: ASK_BLUE:CONFIG:REFRESH, event.domain: manager, event.outcome: success, operation.name: manager.config.refresh, operation.duration_ms: 700}
- `log` 19:43:52.566 — [AskBlue][web][info] configVisibility: synced platform config {source: server, platform: web, requestKey: web:anonymous, shouldRender: false, hasPlatformConfig: true}
- `error` 19:43:52.721 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `warning` 19:43:52.840 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:52.872 — [1:183406] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"10127477","level":"ERROR","message":"No orderId provided. MoreBuyingOptions requires an BSIN to function."} {logger: MPX, componentVersi…
- `error` 19:43:52.901 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:52.976 — 2026-05-17T19:43:52.006Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=PlpView_ProductListItem_Init, errorDetails="{\"name\":\"ServerError\",\"response…
- `error` 19:43:52.977 — 2026-05-17T19:43:52.007Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=PriceExperience_OfferListSiteControlTimeline, errorDetails="{\"name\":\"ServerEr…
- `error` 19:43:52.977 — 2026-05-17T19:43:52.007Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=managedContentByTypeAndId, errorDetails="{\"name\":\"ServerError\",\"response\":…
- `error` 19:43:52.977 — 2026-05-17T19:43:52.007Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=customerVisitorOfferQuery, errorDetails="{\"name\":\"ServerError\",\"response\":…
- `error` 19:43:52.977 — 2026-05-17T19:43:52.007Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=ProductListImage_Init, errorDetails="{\"name\":\"ServerError\",\"response\":{},\…
- `error` 19:43:53.029 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:53.029 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:53.113 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:53.114 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:53.114 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `warning` 19:43:53.120 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:53.139 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:53.143 — [1:183406] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"10127477","level":"ERROR","message":"No orderId provided. MoreBuyingOptions requires an BSIN to function."} {logger: MPX, componentVersi…
- `error` 19:43:53.187 — 2026-05-17T19:43:53.007Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=ProductListItemTitle_Init, errorDetails="{\"name\":\"ServerError\",\"response\":…
- `error` 19:43:53.187 — 2026-05-17T19:43:53.007Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=ReviewStats_Init, errorDetails="{\"name\":\"ServerError\",\"response\":{},\"stat…
- `error` 19:43:53.187 — 2026-05-17T19:43:53.007Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=PriceExperienceInit_GetProduct, errorDetails="{\"name\":\"ServerError\",\"respon…
- `error` 19:43:53.187 — 2026-05-17T19:43:53.007Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=FulfillmentSelector_FulfillmentDynamicQuery, errorDetails="{\"name\":\"ServerErr…
- `error` 19:43:53.187 — 2026-05-17T19:43:53.007Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=AddToCart_FulfillmentDynamicQuery, errorDetails="{\"name\":\"ServerError\",\"res…
- `warning` 19:43:53.268 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:53.280 — [1:183406] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"12192945","level":"ERROR","message":"No orderId provided. MoreBuyingOptions requires an BSIN to function."} {logger: MPX, componentVersi…
- `warning` 19:43:53.335 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:53.344 — [1:183406] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"10127477","level":"ERROR","message":"No orderId provided. MoreBuyingOptions requires an BSIN to function."} {logger: MPX, componentVersi…
- `warning` 19:43:53.356 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:53.357 — [1:183406] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"12192945","level":"ERROR","message":"No orderId provided. MoreBuyingOptions requires an BSIN to function."} {logger: MPX, componentVersi…
- `warning` 19:43:53.400 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:53.411 — [1:183406] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"10127477","level":"ERROR","message":"No orderId provided. MoreBuyingOptions requires an BSIN to function."} {logger: MPX, componentVersi…
- `error` 19:43:53.446 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `warning` 19:43:53.450 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:53.456 — [1:183406] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"12192945","level":"ERROR","message":"No orderId provided. MoreBuyingOptions requires an BSIN to function."} {logger: MPX, componentVersi…
- `error` 19:43:53.494 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:53.495 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:53.495 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:53.495 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `warning` 19:43:53.510 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:53.520 — [1:183406] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"10127477","level":"ERROR","message":"No orderId provided. MoreBuyingOptions requires an BSIN to function."} {logger: MPX, componentVersi…
- `error` 19:43:53.525 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:53.530 — 2026-05-17T19:43:53.000Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=NotifyMe_ProductBySkuId, errorDetails="{\"name\":\"ServerError\",\"response\":{}…
- `error` 19:43:53.530 — 2026-05-17T19:43:53.000Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=ProductListImage_Init, errorDetails="{\"name\":\"ServerError\",\"response\":{},\…
- `error` 19:43:53.530 — 2026-05-17T19:43:53.001Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=ReviewStats_Init, errorDetails="{\"name\":\"ServerError\",\"response\":{},\"stat…
- `warning` 19:43:53.571 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:53.580 — [1:183406] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"12192945","level":"ERROR","message":"No orderId provided. MoreBuyingOptions requires an BSIN to function."} {logger: MPX, componentVersi…
- `warning` 19:43:53.606 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:53.613 — [1:183406] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"11903923","level":"ERROR","message":"No orderId provided. MoreBuyingOptions requires an BSIN to function."} {logger: MPX, componentVersi…
- `error` 19:43:53.656 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:53.661 — 2026-05-17T19:43:53.001Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=ProductListImage_Init, errorDetails="{\"name\":\"ServerError\",\"response\":{},\…
- `error` 19:43:53.661 — 2026-05-17T19:43:53.001Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=NotifyMe_ProductBySkuId, errorDetails="{\"name\":\"ServerError\",\"response\":{}…
- `error` 19:43:53.661 — 2026-05-17T19:43:53.001Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=AddToCart_FulfillmentDynamicQuery, errorDetails="{\"name\":\"ServerError\",\"res…
- `error` 19:43:53.661 — 2026-05-17T19:43:53.001Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=ProductListItemTitle_Init, errorDetails="{\"name\":\"ServerError\",\"response\":…
- `error` 19:43:53.661 — 2026-05-17T19:43:53.001Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=PriceExperienceInit_GetProduct, errorDetails="{\"name\":\"ServerError\",\"respon…
- `warning` 19:43:53.709 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:53.733 — [1:183406] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"10127477","level":"ERROR","message":"No orderId provided. MoreBuyingOptions requires an BSIN to function."} {logger: MPX, componentVersi…
- `error` 19:43:53.781 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:53.841 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:53.841 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:53.841 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:53.842 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:53.869 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:53.869 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `warning` 19:43:53.883 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:53.968 — [1:183406] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"10127477","level":"ERROR","message":"No orderId provided. MoreBuyingOptions requires an BSIN to function."} {logger: MPX, componentVersi…
- `error` 19:43:53.980 — 2026-05-17T19:43:53.000Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=FulfillmentSelector_FulfillmentDynamicQuery, errorDetails="{\"name\":\"ServerErr…
- `error` 19:43:53.980 — 2026-05-17T19:43:53.000Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=ProductListItemTitle_Init, errorDetails="{\"name\":\"ServerError\",\"response\":…
- `error` 19:43:53.980 — 2026-05-17T19:43:53.000Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=ProductListImage_Init, errorDetails="{\"name\":\"ServerError\",\"response\":{},\…
- `error` 19:43:53.980 — 2026-05-17T19:43:53.000Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=PriceExperienceInit_GetProduct, errorDetails="{\"name\":\"ServerError\",\"respon…
- `error` 19:43:53.980 — 2026-05-17T19:43:53.001Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=AddToCart_FulfillmentDynamicQuery, errorDetails="{\"name\":\"ServerError\",\"res…
- `info` 19:43:54.032 — [1:3282373] COMMERCE_VIEW | ADD_TO_CART | INIT_ANALYTICSQ_DEPPROXY | ATC_Version: __VERSION__ Module
- `info` 19:43:54.033 — [1:3282373] COMMERCE_VIEW | ADD_TO_CART | INIT_EVENTMANAGER_DEPPROXY | ATC_Version: __VERSION__ {EventManager: , default: e, __esModule: true}
- `warning` 19:43:54.120 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:54.144 — [1:183406] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"10127477","level":"ERROR","message":"No orderId provided. MoreBuyingOptions requires an BSIN to function."} {logger: MPX, componentVersi…
- `warning` 19:43:54.245 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:54.261 — [1:183406] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"12192945","level":"ERROR","message":"No orderId provided. MoreBuyingOptions requires an BSIN to function."} {logger: MPX, componentVersi…
- `warning` 19:43:54.337 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:54.362 — [1:183406] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"11903923","level":"ERROR","message":"No orderId provided. MoreBuyingOptions requires an BSIN to function."} {logger: MPX, componentVersi…
- `warning` 19:43:54.397 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:54.402 — [1:183406] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"12476024","level":"ERROR","message":"No orderId provided. MoreBuyingOptions requires an BSIN to function."} {logger: MPX, componentVersi…
- `warning` 19:43:54.450 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:54.457 — [1:183406] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"10127477","level":"ERROR","message":"No orderId provided. MoreBuyingOptions requires an BSIN to function."} {logger: MPX, componentVersi…
- `warning` 19:43:54.479 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:54.485 — [1:183406] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"12192945","level":"ERROR","message":"No orderId provided. MoreBuyingOptions requires an BSIN to function."} {logger: MPX, componentVersi…
- `warning` 19:43:54.512 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:54.520 — [1:183406] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"11903923","level":"ERROR","message":"No orderId provided. MoreBuyingOptions requires an BSIN to function."} {logger: MPX, componentVersi…
- `warning` 19:43:54.540 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:54.541 — [1:183406] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"12476024","level":"ERROR","message":"No orderId provided. MoreBuyingOptions requires an BSIN to function."} {logger: MPX, componentVersi…
- `error` 19:43:54.553 — TypeError: Cannot read properties of undefined (reading 'skuId') ⏎     at P (https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/8662-195308428d21d0dc.js:1:80461) ⏎     at https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/8662-195308428d21d0dc.js:1:82655 ⏎     …
- `error` 19:43:54.553 — Error: [useEGPDataQuery] Unknown error - Parameters: {"customer":{"profileLabels":[]},"skuId":"10127477","isCombo":false,"platform":"lv","openBoxCondition":null,"zipCode":"55423","isUserLoggedIn":false,"displayLocation":"searchResults"} ⏎     at iV (https://www.bestbuy.com/~assets/bby/_com/shop/plp…
- `warning` 19:43:54.554 — [Price::ErrorBoundary] Uncaught error: Error: [useEGPDataQuery] Unknown error - Parameters: {"customer":{"profileLabels":[]},"skuId":"10127477","isCombo":false,"platform":"lv","openBoxCondition":null,"zipCode":"55423","isUserLoggedIn":false,"displayLocation":"searchResults"} ⏎     at iV (https://ww…
- `error` 19:43:54.555 — TypeError: Cannot read properties of undefined (reading 'skuId') ⏎     at P (https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/8662-195308428d21d0dc.js:1:80461) ⏎     at https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/8662-195308428d21d0dc.js:1:82655 ⏎     …
- `error` 19:43:54.555 — Error: [useEGPDataQuery] Unknown error - Parameters: {"customer":{"profileLabels":[]},"skuId":"12192945","isCombo":false,"platform":"lv","openBoxCondition":null,"zipCode":"55423","isUserLoggedIn":false,"displayLocation":"searchResults"} ⏎     at iV (https://www.bestbuy.com/~assets/bby/_com/shop/plp…
- `warning` 19:43:54.556 — [Price::ErrorBoundary] Uncaught error: Error: [useEGPDataQuery] Unknown error - Parameters: {"customer":{"profileLabels":[]},"skuId":"12192945","isCombo":false,"platform":"lv","openBoxCondition":null,"zipCode":"55423","isUserLoggedIn":false,"displayLocation":"searchResults"} ⏎     at iV (https://ww…
- `error` 19:43:54.557 — TypeError: Cannot read properties of undefined (reading 'skuId') ⏎     at P (https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/8662-195308428d21d0dc.js:1:80461) ⏎     at https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/8662-195308428d21d0dc.js:1:82655 ⏎     …
- `error` 19:43:54.558 — Error: [useEGPDataQuery] Unknown error - Parameters: {"customer":{"profileLabels":[]},"skuId":"11903923","isCombo":false,"platform":"lv","openBoxCondition":null,"zipCode":"55423","isUserLoggedIn":false,"displayLocation":"searchResults"} ⏎     at iV (https://www.bestbuy.com/~assets/bby/_com/shop/plp…
- `warning` 19:43:54.559 — [Price::ErrorBoundary] Uncaught error: Error: [useEGPDataQuery] Unknown error - Parameters: {"customer":{"profileLabels":[]},"skuId":"11903923","isCombo":false,"platform":"lv","openBoxCondition":null,"zipCode":"55423","isUserLoggedIn":false,"displayLocation":"searchResults"} ⏎     at iV (https://ww…
- `error` 19:43:54.562 — 2026-05-17T19:43:54.002Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=NotifyMe_ProductBySkuId, errorDetails="{\"name\":\"ServerError\",\"response\":{}…
- `error` 19:43:54.562 — 2026-05-17T19:43:54.002Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=FulfillmentSelector_FulfillmentDynamicQuery, errorDetails="{\"name\":\"ServerErr…
- `error` 19:43:54.562 — 2026-05-17T19:43:54.002Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=ReviewStats_Init, errorDetails="{\"name\":\"ServerError\",\"response\":{},\"stat…
- `error` 19:43:54.562 — 2026-05-17T19:43:54.002Z logLevel=ERROR, 0=P, 1=L, 2=P, 3=_, 4=V, 5=I, 6=E, 7=W, 8=_, 9=L, 10=O, 11=G, 12=G, 13=E, 14=R, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=browser-logger, componentStack="\n    at L (https://www.bestbuy.com/~asse…
- `error` 19:43:54.586 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:54.586 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `warning` 19:43:54.592 — [1:183632] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"10127477","errorContextName":"more-buying-options-plp","level":"WARN","message":"MPX | more-buying-options-plp | l | more-buying-options…
- `warning` 19:43:54.598 — [1:183632] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"12192945","errorContextName":"more-buying-options-plp","level":"WARN","message":"MPX | more-buying-options-plp | l | more-buying-options…
- `warning` 19:43:54.601 — [1:183632] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"11903923","errorContextName":"more-buying-options-plp","level":"WARN","message":"MPX | more-buying-options-plp | l | more-buying-options…
- `warning` 19:43:54.605 — [1:183632] {"logger":"MPX","componentVersion":"1.23.0","filter":"mpx-sc-paul-logger-format","displayLocation":"more-buying-options-plp","deviceClass":"l","skuId":"12476024","errorContextName":"more-buying-options-plp","level":"WARN","message":"MPX | more-buying-options-plp | l | more-buying-options…
- `warning` 19:43:54.624 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:54.649 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:54.649 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:54.651 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:54.651 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:54.675 — 2026-05-17T19:43:54.004Z logLevel=ERROR, 0=P, 1=L, 2=P, 3=_, 4=V, 5=I, 6=E, 7=W, 8=_, 9=L, 10=O, 11=G, 12=G, 13=E, 14=R, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=browser-logger, componentStack="\n    at L (https://www.bestbuy.com/~asse…
- `error` 19:43:54.704 — 2026-05-17T19:43:54.004Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=ProductListItemTitle_Init, errorDetails="{\"name\":\"ServerError\",\"response\":…
- `error` 19:43:54.704 — 2026-05-17T19:43:54.004Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=ReviewStats_Init, errorDetails="{\"name\":\"ServerError\",\"response\":{},\"stat…
- `error` 19:43:54.704 — 2026-05-17T19:43:54.004Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=NotifyMe_ProductBySkuId, errorDetails="{\"name\":\"ServerError\",\"response\":{}…
- `error` 19:43:54.704 — 2026-05-17T19:43:54.004Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=PriceExperienceInit_GetProduct, errorDetails="{\"name\":\"ServerError\",\"respon…
- `error` 19:43:54.704 — 2026-05-17T19:43:54.004Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=AddToCart_FulfillmentDynamicQuery, errorDetails="{\"name\":\"ServerError\",\"res…
- `warning` 19:43:54.716 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:54.784 — Error triggering event 'addToCart' for Tag 'adobeDcoPdpCategory': Error: Cannot find module './adobeDcoPdpCategory/index' [GOTEAM, MultiTenant, eventTrigger, addToCart]
- `warning` 19:43:54.789 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:54.854 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `warning` 19:43:54.884 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:54.913 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:54.983 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `warning` 19:43:55.039 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `warning` 19:43:55.056 — Invalid DEO recipe value "undefined" for feature "removePlpPlusOffers". Falling back to CONTROL.
- `error` 19:43:55.132 — TypeError: Cannot read properties of undefined (reading 'skuId') ⏎     at P (https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/8662-195308428d21d0dc.js:1:80461) ⏎     at https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/8662-195308428d21d0dc.js:1:82655 ⏎     …
- `error` 19:43:55.132 — Error: [useEGPDataQuery] Unknown error - Parameters: {"customer":{"profileLabels":[]},"skuId":"12476024","isCombo":false,"platform":"lv","openBoxCondition":null,"zipCode":"55423","isUserLoggedIn":false,"displayLocation":"searchResults"} ⏎     at iV (https://www.bestbuy.com/~assets/bby/_com/shop/plp…
- `warning` 19:43:55.133 — [Price::ErrorBoundary] Uncaught error: Error: [useEGPDataQuery] Unknown error - Parameters: {"customer":{"profileLabels":[]},"skuId":"12476024","isCombo":false,"platform":"lv","openBoxCondition":null,"zipCode":"55423","isUserLoggedIn":false,"displayLocation":"searchResults"} ⏎     at iV (https://ww…
- `error` 19:43:55.191 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:55.192 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:55.193 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:55.210 — 2026-05-17T19:43:55.009Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=FulfillmentSelector_FulfillmentDynamicQuery, errorDetails="{\"name\":\"ServerErr…
- `error` 19:43:55.212 — 2026-05-17T19:43:55.001Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=PLP, errorDetails={}, logMessage="[BBY SW] Error fetching experiment data: {}"
- `error` 19:43:55.213 — 2026-05-17T19:43:55.002Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=RecsInterruptor_LiveConfig, errorDetails="{\"name\":\"ServerError\",\"response\"…
- `error` 19:43:55.213 — 2026-05-17T19:43:55.002Z logLevel=ERROR, 0=P, 1=L, 2=P, 3=_, 4=V, 5=I, 6=E, 7=W, 8=_, 9=L, 10=O, 11=G, 12=G, 13=E, 14=R, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=browser-logger, componentStack="\n    at L (https://www.bestbuy.com/~asse…
- `error` 19:43:55.213 — 2026-05-17T19:43:55.002Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=RecsInterruptor_FetchSkuListData, errorDetails="{\"name\":\"ServerError\",\"resp…
- `error` 19:43:55.394 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:55.402 — 2026-05-17T19:43:55.002Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=WarrantySelector_CustomerPriceAndButtonState, errorDetails="{\"name\":\"ServerEr…
- `error` 19:43:55.404 — 2026-05-17T19:43:55.003Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=Recommendations_Experience_ConfigNode, errorDetails="{\"name\":\"ServerError\",\…
- `error` 19:43:55.404 — 2026-05-17T19:43:55.004Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=browser-logger, logLevel=undefined, forceLog=undefined, logMessage="Product Carousel MF isMatchTypeInfo is false with skuId: 6646419"
- `error` 19:43:55.404 — 2026-05-17T19:43:55.004Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=ReviewStats_Init, errorDetails="{\"name\":\"ServerError\",\"response\":{},\"stat…
- `error` 19:43:55.433 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:55.595 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:43:55.720 — TypeError: Cannot read properties of null (reading 'productBySkuId') ⏎     at https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/b8dcfb4b-49ffb3360a70cb5a.js:1:188533 ⏎     at sL (https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/b8dcfb4b-49ffb3360a70cb5a.js:1…
- `error` 19:43:55.721 — [ErrorBoundary] Uncaught error: TypeError: Cannot read properties of null (reading 'productBySkuId') ⏎     at https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunks/b8dcfb4b-49ffb3360a70cb5a.js:1:188533 ⏎     at sL (https://www.bestbuy.com/~assets/bby/_com/shop/plp/_next/static/chunk…
- `error` 19:43:57.603 — 2026-05-17T19:43:57.002Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=browser-logger, logLevel=undefined, forceLog=undefined, repeatGroupId=mpa6o5xm-000d, repeatCount=2, logMessage="Product Carousel MF isMatchTypeInfo is fa…
- `error` 19:43:57.603 — 2026-05-17T19:43:57.003Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=getProduct, errorDetails="{\"name\":\"ServerError\",\"response\":{},\"statusCode…
- `error` 19:43:57.603 — 2026-05-17T19:43:57.003Z logLevel=ERROR, sid=fae875cc-b99e-452a-a0e7-b4bd9fdc8dfa, vt=11d61959-64a5-4174-a3ae-470acdd2933e, deviceClass=l, logger=GRAPHQL-LINK, clientId=plp-web, linkName=networkErrorLink, operationName=RecsXMatchTypeInfo, errorDetails="{\"name\":\"ServerError\",\"response\":{},\"st…
- `warning` 19:44:00.098 — document.domain mutation is ignored because the surrounding agent cluster is origin-keyed.
- `log` 19:44:00.203 — %cDEO Client SDK color: #fff;background:#000;padding:0.25em  | Returning false, "exp0283" not present in configfile.
- `log` 19:44:00.335 — getServerComponent suppressed
- `log` 19:44:00.356 — CJ Capture SDK - Composed Event: {contract: Array(1), identities: Object, source: Object, appState: Object, basket: Object}
- `warning` 19:44:01.375 — Warning: fragment with name Pricing already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:44:01.375 — Warning: fragment with name Products already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `warning` 19:44:01.409 — Warning: fragment with name BuyingOptions already exists. ⏎ graphql-tag enforces all fragment names across your application to be unique; read more about ⏎ this in the docs: http://dev.apollodata.com/core/fragments.html#unique-names
- `info` 19:44:01.510 — [2:1694560] COMMERCE_VIEW | CART_FE | ASYNC_LOAD_ENABLED | FEVersion:26.18.31
- `error` 19:44:02.172 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `warning` 19:44:02.667 — TypeError: Cannot set properties of null (setting 'href') ⏎     at doStuff (eval at <anonymous> (https://www.bestbuy.com/~assets/bby/_com/shop/stips/dist/client/109-8d41dfb3ae61238f1c8715ac8641b1bc.js:1:5212), <anonymous>:18:22) ⏎     at documentReadyCheck (eval at <anonymous> (https://www.bestbuy.…
- `warning` 19:44:02.724 — Failed to parse video contentType: video/mp4; codecs=hev1.1.6.L120.90
- `debug` 19:44:02.724 — Error
- `warning` 19:44:02.760 — No available adapters.
- `debug` 19:44:02.805 — Headers not available in current context: Error: `headers` was called outside a request scope. Read more: https://nextjs.org/docs/messages/next-dynamic-api-wrong-context ⏎     at n (https://www.bestbuy.com/~assets/bby/_com/shop/header/dist/client/8639-a28fb014640ca3fd163cf39cf6be4769.js:10:3509871)…
- `debug` 19:44:02.808 — Headers not available in current context: Error: `headers` was called outside a request scope. Read more: https://nextjs.org/docs/messages/next-dynamic-api-wrong-context ⏎     at n (https://www.bestbuy.com/~assets/bby/_com/shop/header/dist/client/8639-a28fb014640ca3fd163cf39cf6be4769.js:10:3509871)…
- `info` 19:44:02.929 — [2:1694560] COMMERCE_VIEW | CART_FE | LOAD_TIME | ASYNCHRONOUS | 2 - 3 SECONDS |  2.974 SECONDS | FEVersion:26.18.31
- `info` 19:44:03.022 — [2:1694560] LOG_MESSAGE: PAYMENTS_EXPERIENCE | BUY_NOW_PAY_LATER |  | TRIGGER_COMPONENT: ZIP_LEARN_MORE_LINK | TRIGGER_EVENT: VIEW_INITIALIZED | FEVersion: 2.0.20 | userAgent: Google Chrome or Chromium
- `info` 19:44:03.023 — [2:1694560] LOG_MESSAGE: PAYMENTS_EXPERIENCE | BUY_NOW_PAY_LATER | INSTALLMENT AMOUNT: 89.37 | TRIGGER_COMPONENT: BNPL_BANNER | TRIGGER_EVENT: VIEW_INITIALIZED | FEVersion: 2.0.20 | userAgent: Google Chrome or Chromium
- `warning` 19:44:03.050 — [2:1694560]  UPA-LOGGER | Invalid pass through headers are configured | { ⏎   "logger": "GRAPHQL-passHeadersLink", ⏎   "clientId": "cart-web", ⏎   "SID": "not-present", ⏎   "VT": "not-present", ⏎   "xRequestId": "not-present" ⏎ }
- `warning` 19:44:03.051 — [2:1694560]  UPA-LOGGER | Pass through cookies are configured wrongly | { ⏎   "logger": "GRAPHQL-passCookiesLink", ⏎   "clientId": "cart-web", ⏎   "SID": "not-present", ⏎   "VT": "not-present", ⏎   "xRequestId": "bfc1efeb-197c-4c6a-a291-cdb1336b749c" ⏎ }
- `error` 19:44:03.097 — ApolloError: Cannot read properties of undefined (reading 'clientSideFulfillmentLinkConfig') ⏎     at new t (https://www.bestbuy.com/~assets/bby/_com/vendors-node_modules_best-buy_currency-helpers_lib_currency-helpers_js-node_modules_best-buy_-0a87c8.cart.bundle-63867448470d5a48612952503c8afe07.js:…
- `warning` 19:44:03.097 — [2:1694560] COMMERCE_VIEW | CART_FE | ERROR_BOUNDARY | COMPONENT:RecsProductCarousel | LOCATION:CarouselsContainer | ⏎       Error Message: ApolloError: Cannot read properties of undefined (reading 'clientSideFulfillmentLinkConfig') | ⏎       Stack Trace:  ⏎     at hg (https://www.bestbuy.com/~asse…
- `error` 19:44:03.119 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:44:03.121 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `info` 19:44:03.273 — ZodError: [ ⏎   { ⏎     "code": "invalid_type", ⏎     "expected": "object", ⏎     "received": "undefined", ⏎     "path": [], ⏎     "message": "Required" ⏎   } ⏎ ] ⏎     at new t (https://www.bestbuy.com/~assets/bby/_com/shop/header/dist/client/393-a28fb014640ca3fd163cf39cf6be4769.js:2:4561) ⏎     a…
- `error` 19:44:03.288 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `info` 19:44:03.290 — [22:81956] MEMBERSHIP_ACQUISITION | MEMBERSHIP_UPSELL | VERSION: 26.16.1 | EGP query failed: {}
- `error` 19:44:03.293 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `info` 19:44:03.293 — [22:81956] MEMBERSHIP_ACQUISITION | MEMBERSHIP_UPSELL | VERSION: 26.16.1 | EGP query failed: {}
- `error` 19:44:03.306 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `warning` 19:44:03.307 — [2:1694560] COMMERCE_VIEW | CART_FE | VISITOR_OFFER_FETCH_ERROR | TypeError: Failed to fetch | FEVersion:26.18.31
- `info` 19:44:03.312 — ZodError: [ ⏎   { ⏎     "code": "invalid_type", ⏎     "expected": "object", ⏎     "received": "undefined", ⏎     "path": [], ⏎     "message": "Required" ⏎   } ⏎ ] ⏎     at new t (https://www.bestbuy.com/~assets/bby/_com/shop/header/dist/client/393-a28fb014640ca3fd163cf39cf6be4769.js:2:4561) ⏎     a…
- `error` 19:44:03.477 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:44:03.478 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `info` 19:44:03.484 — ZodError: [ ⏎   { ⏎     "code": "invalid_type", ⏎     "expected": "object", ⏎     "received": "undefined", ⏎     "path": [], ⏎     "message": "Required" ⏎   } ⏎ ] ⏎     at new t (https://www.bestbuy.com/~assets/bby/_com/shop/header/dist/client/393-a28fb014640ca3fd163cf39cf6be4769.js:2:4561) ⏎     a…
- `info` 19:44:03.515 — [2:1694560] COMMERCE_VIEW | CART_FE | GVP_ADDON_PRICE_BLOCK | EMBEDDED_COMPONENT_INIT_SUCCESS | FEVersion:26.18.31
- `info` 19:44:03.620 — [2:1694560] COMMERCE_VIEW | CART_FE | GVP_SAVED_ITEMS | EMBEDDED_COMPONENT_INIT_SUCCESS | FEVersion:26.18.31
- `warning` 19:44:03.690 — An iframe which has both allow-scripts and allow-same-origin for its sandbox attribute can escape its sandboxing.
- `error` 19:44:03.725 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:44:03.725 — [Network error]: header Failed to fetch
- `error` 19:44:03.810 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:44:03.810 — [Network error]: header Failed to fetch
- `log` 19:44:04.265 — %cDEO Client SDK color: #fff;background:#000;padding:0.25em  | Returning false, traffic allocation set to 0% for "web_integration_test".
- `log` 19:44:04.265 — %cDEO Client SDK color: #fff;background:#000;padding:0.25em  | Returning false, "exp0478" not present in configfile.
- `debug` 19:44:04.279 — Error
- `endGroup` 19:44:04.336 — {}
- `error` 19:44:04.539 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:44:04.540 — [Network error]: header Failed to fetch
- `log` 19:44:04.782 — Pricing/price:UPB --- CSR | 6627799 | profile=MINI
- `error` 19:44:04.819 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:44:04.819 — [Network error]: header Failed to fetch
- `error` 19:44:05.185 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `warning` 19:44:05.190 — Pricing/price:UPB --- Network unknown: Failed to fetch
- `error` 19:44:05.216 — ApolloError: Failed to fetch ⏎     at new t (https://www.bestbuy.com/~assets/bby/_com/pricing/price/dist/client/6304-28cf7995cce8475efca5412f99838295.mjs:2:584441) ⏎     at https://www.bestbuy.com/~assets/bby/_com/pricing/price/dist/client/6304-28cf7995cce8475efca5412f99838295.mjs:2:566510 ⏎     at…
- `error` 19:44:05.216 — [ErrorBoundary] Uncaught error: ApolloError: Failed to fetch ⏎     at new t (https://www.bestbuy.com/~assets/bby/_com/pricing/price/dist/client/6304-28cf7995cce8475efca5412f99838295.mjs:2:584441) ⏎     at https://www.bestbuy.com/~assets/bby/_com/pricing/price/dist/client/6304-28cf7995cce8475efca541…
- `error` 19:44:05.454 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:44:05.454 — [Network error]: header Failed to fetch
- `error` 19:44:05.454 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:44:05.454 — [Network error]: header Failed to fetch
- `debug` 19:44:05.747 — Error
- `endGroup` 19:44:05.782 — {}
- `debug` 19:44:05.948 — Config loading completed
- `debug` 19:44:05.949 — Plp Config loading completed
- `log` 19:44:05.950 — %cDEO Client SDK color: #fff;background:#000;padding:0.25em  | Returning false, "exp0347" not present in configfile.
- `log` 19:44:05.950 — %cDEO Client SDK color: #fff;background:#000;padding:0.25em  | Returning false, "exp0306" not present in configfile.
- `log` 19:44:05.950 — %cDEO Client SDK color: #fff;background:#000;padding:0.25em  | Returning false, "exp0510" not present in configfile.
- `error` 19:44:06.128 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:44:06.128 — [Network error]: header Failed to fetch
- `error` 19:44:06.160 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `error` 19:44:06.160 — [Network error]: header Failed to fetch
- `warning` 19:44:08.017 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.017 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.017 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.017 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.017 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.017 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.018 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.018 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.018 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.018 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.018 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.018 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.018 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.018 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.018 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.018 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.019 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.019 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.019 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.019 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.019 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.019 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.019 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.019 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.019 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.019 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.020 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.020 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.020 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.020 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.020 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.020 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.020 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.020 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.020 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.021 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.021 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.021 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.021 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.021 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.022 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.022 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.022 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.022 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.022 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.022 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.023 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.023 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.023 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.023 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.023 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.023 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.023 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.023 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.023 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.023 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.024 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.024 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.024 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.024 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.024 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.024 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.024 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.024 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.024 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.025 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.025 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.025 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.025 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.025 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.025 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.025 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.026 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.026 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.027 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.027 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.027 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.028 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.028 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.029 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.029 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.029 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.029 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.029 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.030 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.030 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.030 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.030 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.030 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.031 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.031 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.031 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.031 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.031 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.031 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.031 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.032 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.032 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.032 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.032 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.032 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.033 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.033 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.033 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.033 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.034 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.034 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.034 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.034 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.034 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.034 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.035 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.035 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.035 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.035 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.035 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.035 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.036 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.036 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.036 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.036 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.036 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.037 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.037 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.037 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.037 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.037 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.038 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.038 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.038 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.038 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.038 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.039 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.039 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.039 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.039 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.040 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.040 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.040 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.040 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.040 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.041 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.041 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.041 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.041 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.041 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.042 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.042 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.042 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.042 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.043 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.043 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.043 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.043 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.043 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.043 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.043 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.044 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.044 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.044 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.044 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.044 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.045 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.045 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.045 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.045 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.045 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.045 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.046 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.046 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.046 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.046 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.046 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.046 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.047 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.047 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.047 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.047 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.047 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.048 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.048 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.048 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.048 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.049 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.049 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.049 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.049 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.049 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.050 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.050 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.050 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.050 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.050 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.050 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.050 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.050 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.051 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.051 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.051 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.051 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.051 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.051 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.052 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.052 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.052 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.052 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.052 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.052 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.053 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.053 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.053 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.053 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.053 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.054 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.054 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.054 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.054 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.054 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.054 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.055 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.055 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.055 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.055 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.055 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.056 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.056 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.056 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.056 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.056 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.056 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.057 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.057 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.057 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.057 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.058 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.058 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.058 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.059 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.059 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.059 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.059 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.060 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.060 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.060 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.060 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.060 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.060 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.060 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.061 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.061 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.061 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.061 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.061 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.062 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.062 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.062 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.062 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.062 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.062 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.062 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.063 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.063 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.063 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.063 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.063 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.064 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.064 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.064 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.064 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.064 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.064 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.065 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.065 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.065 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.065 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.065 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.066 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.066 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.066 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.066 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.066 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.066 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.066 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.067 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.069 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.069 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.069 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.069 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.069 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.069 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.069 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.069 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.070 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.070 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.070 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.070 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.071 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.071 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.071 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.071 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.071 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.071 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.071 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.071 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.071 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.071 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.071 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.071 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.071 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.071 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.071 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.071 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.071 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.071 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.071 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.071 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.071 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.072 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.072 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.072 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.072 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.072 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.072 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.072 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.073 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.073 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.073 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.073 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.074 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.074 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.074 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.074 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.074 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.074 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.074 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `warning` 19:44:08.075 — Error: Too many levels to clone object. ⏎     at e.value (https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4537) ⏎     at https://www.bestbuy.com/~assets/bby/_com/gvp-d1b21d6e99fec5dcbb49ea62b9254205.min.js:10:4727 ⏎     at Array.reduce (<anonymous>) ⏎     at …
- `error` 19:44:09.580 — [2:1694560] pricing.price Failed to fetch
- `error` 19:44:09.580 — [2:1694560] pricing.price BASIC - DownstreamDependencyFailure - [2026-05-17T19:44:09.577Z] - Failed to fetch
- `log` 19:44:09.910 — CJ Capture SDK - Composed Event: {contract: Array(1), identities: Object, source: Object, appState: Object, basket: Object}
- `warning` 19:44:10.453 — [GSI_LOGGER]: Your client application uses one of the Google One Tap prompt UI status methods that may stop functioning when FedCM becomes mandatory. Refer to the migration guide to update your code accordingly and opt-in to FedCM to test your changes. Learn more: https://developers.google.com/iden…
- `warning` 19:44:10.678 — An iframe which has both allow-scripts and allow-same-origin for its sandbox attribute can escape its sandboxing.
- `debug` 19:44:11.008 — Error
- `endGroup` 19:44:11.027 — {}
- `error` 19:44:11.229 — Provider's accounts list is empty.
- `error` 19:44:13.644 — [GSI_LOGGER]: FedCM get() rejects with AbortError: signal is aborted without reason
- `warning` 19:44:15.202 — document.domain mutation is ignored because the surrounding agent cluster is origin-keyed.
- `log` 19:44:15.314 — CJ Capture SDK - Composed Event: {contract: Array(1), identities: Object, source: Object, appState: Object, basket: Object}
- `warning` 19:44:15.361 — WebpackRequireFrom: something is trying to override webpack public path. Ignoring the new valuehttps://www.bestbuy.com/~assets/bby/_com.
- `info` 19:44:15.488 — [2:1642127] COMMERCE_VIEW | CHECKOUT_FE | LOCAL_STORAGE | 0-5MB | 361.0KB | FEVersion: 26.19.23
- `info` 19:44:15.503 — [2:1642127] COMMERCE_VIEW | CHECKOUT_FE | STATE_CHANGE_FROM  TO fast-track | FEVersion: 26.19.23
- `info` 19:44:15.511 — [2:1642127] COMMERCE_VIEW | CHECKOUT_FE | FAST_TRACK_EXCEPTIONS | fulfillment is not valid, payment is not valid, has shipping items With missing address | FEVersion: 26.19.23
- `info` 19:44:15.516 — [2:1642127] COMMERCE_VIEW | CHECKOUT_FE | STATE_CHANGE_FROM fast-track TO fulfillment | FEVersion: 26.19.23
- `log` 19:44:15.826 — getServerComponent suppressed
- `warning` 19:44:16.182 — Failed to parse video contentType: video/mp4; codecs=hev1.1.6.L120.90
- `debug` 19:44:16.183 — Error
- `warning` 19:44:16.212 — An iframe which has both allow-scripts and allow-same-origin for its sandbox attribute can escape its sandboxing.
- `warning` 19:44:16.219 — No available adapters.
- `error` 19:44:16.537 — Failed to load resource: net::ERR_HTTP2_PROTOCOL_ERROR
- `debug` 19:44:16.654 — Error
- `debug` 19:44:16.680 — Error
- `endGroup` 19:44:16.718 — {}
- `endGroup` 19:44:16.747 — {}
- `error` 19:44:32.387 — Blocked script execution in 'about:blank' because the document's frame is sandboxed and the 'allow-scripts' permission is not set.

## Consolidated execution path

```text
· 2026-05-17T19:43:36.260+00:00    BrowserContext.newPage                   189 ms  
· 2026-05-17T19:43:36.455+00:00             Frame.goto                      2.14 s  https://www.bestbuy.com
· 2026-05-17T19:43:39.405+00:00             Frame.waitForTimeout            3.20 s  
· 2026-05-17T19:43:42.626+00:00              Page.screenshot                352 ms  
· 2026-05-17T19:43:43.004+00:00             Frame.goto                      2.93 s  https://www.bestbuy.com/site/searchpage.jsp?st=playstation+5+console
· 2026-05-17T19:43:46.627+00:00             Frame.waitForTimeout            4.18 s  
· 2026-05-17T19:43:50.951+00:00              Page.screenshot                1.64 s  
· 2026-05-17T19:43:52.620+00:00             Frame.queryCount                 44 ms  internal:role=button[name="Add to cart"i]
· 2026-05-17T19:43:52.681+00:00             Frame.waitForSelector           218 ms  internal:role=button[name="Add to cart"i] >> nth=0
· 2026-05-17T19:43:52.932+00:00             Frame.waitForSelector            64 ms  internal:role=button[name="Add to cart"i] >> nth=0
· 2026-05-17T19:43:53.003+00:00     ElementHandle.scrollIntoViewIfNeeded     62 ms  
· 2026-05-17T19:43:53.671+00:00     ElementHandle.dispose                    <1 ms  
· 2026-05-17T19:43:53.673+00:00             Frame.click                     413 ms  internal:role=button[name="Add to cart"i] >> nth=0
· 2026-05-17T19:43:54.738+00:00             Frame.waitForTimeout            3.02 s  
· 2026-05-17T19:43:57.773+00:00              Page.screenshot                372 ms  
· 2026-05-17T19:43:58.173+00:00             Frame.waitForSelector            32 ms  internal:text="Go to cart"i >> nth=0
· 2026-05-17T19:43:58.223+00:00             Frame.waitForSelector            29 ms  internal:text="Go to cart"i >> nth=0
· 2026-05-17T19:43:58.266+00:00     ElementHandle.scrollIntoViewIfNeeded     27 ms  
· 2026-05-17T19:43:58.916+00:00     ElementHandle.dispose                    <1 ms  
· 2026-05-17T19:43:58.918+00:00             Frame.click                     1.10 s  internal:text="Go to cart"i >> nth=0
· 2026-05-17T19:44:00.754+00:00             Frame.waitForTimeout            3.15 s  
· 2026-05-17T19:44:03.978+00:00              Page.screenshot                639 ms  
· 2026-05-17T19:44:04.627+00:00             Frame.waitForSelector            24 ms  internal:role=button[name="Checkout"i] >> nth=0
· 2026-05-17T19:44:04.661+00:00             Frame.waitForSelector           791 ms  internal:role=button[name="Checkout"i] >> nth=0
· 2026-05-17T19:44:05.481+00:00     ElementHandle.scrollIntoViewIfNeeded    279 ms  
· 2026-05-17T19:44:06.759+00:00     ElementHandle.dispose                     1 ms  
· 2026-05-17T19:44:06.762+00:00             Frame.click                     1.36 s  internal:role=button[name="Checkout"i] >> nth=0
· 2026-05-17T19:44:08.782+00:00             Frame.waitForTimeout            4.02 s  
· 2026-05-17T19:44:12.812+00:00              Page.screenshot                 99 ms  
· 2026-05-17T19:44:12.922+00:00             Frame.waitForSelector            19 ms  internal:role=button[name="Continue as Guest"i] >> nth=0
· 2026-05-17T19:44:12.947+00:00             Frame.waitForSelector            10 ms  internal:role=button[name="Continue as Guest"i] >> nth=0
· 2026-05-17T19:44:12.962+00:00     ElementHandle.scrollIntoViewIfNeeded     17 ms  
· 2026-05-17T19:44:13.584+00:00     ElementHandle.dispose                    <1 ms  
· 2026-05-17T19:44:13.586+00:00             Frame.click                      66 ms  internal:role=button[name="Continue as Guest"i] >> nth=0
· 2026-05-17T19:44:15.028+00:00             Frame.waitForTimeout            3.01 s  
· 2026-05-17T19:44:18.071+00:00              Page.screenshot                133 ms  
· 2026-05-17T19:44:18.212+00:00             Frame.waitForSelector            50 ms  internal:label="First Name"i >> nth=0
· 2026-05-17T19:44:18.272+00:00             Frame.click                     117 ms  internal:label="First Name"i >> nth=0
· 2026-05-17T19:44:19.022+00:00             Frame.fill                      113 ms  internal:label="First Name"i >> nth=0
· 2026-05-17T19:44:19.745+00:00             Frame.waitForSelector             9 ms  internal:label="Last Name"i >> nth=0
· 2026-05-17T19:44:19.758+00:00             Frame.click                      92 ms  internal:label="Last Name"i >> nth=0
· 2026-05-17T19:44:20.463+00:00             Frame.fill                       34 ms  internal:label="Last Name"i >> nth=0
· 2026-05-17T19:44:21.115+00:00             Frame.waitForSelector             9 ms  internal:label="Address"i >> nth=0
· 2026-05-17T19:44:21.129+00:00             Frame.click                      93 ms  internal:label="Address"i >> nth=0
· 2026-05-17T19:44:21.833+00:00             Frame.fill                       38 ms  internal:label="Address"i >> nth=0
· 2026-05-17T19:44:22.478+00:00             Frame.waitForSelector            10 ms  internal:label="Email Address"i >> nth=0
· 2026-05-17T19:44:22.492+00:00             Frame.click                     106 ms  internal:label="Email Address"i >> nth=0
· 2026-05-17T19:44:23.208+00:00             Frame.fill                       36 ms  internal:label="Email Address"i >> nth=0
· 2026-05-17T19:44:23.859+00:00             Frame.waitForSelector            10 ms  internal:label="Phone Number"i >> nth=0
· 2026-05-17T19:44:23.873+00:00             Frame.click                      55 ms  internal:label="Phone Number"i >> nth=0
· 2026-05-17T19:44:24.547+00:00             Frame.fill                       45 ms  internal:label="Phone Number"i >> nth=0
· 2026-05-17T19:44:25.211+00:00             Frame.waitForTimeout            1.52 s  
· 2026-05-17T19:44:26.739+00:00             Frame.click                      67 ms  h2:has-text('Shipping') >> nth=0
· 2026-05-17T19:44:27.414+00:00             Frame.waitForTimeout            507 ms  
· 2026-05-17T19:44:27.926+00:00             Frame.waitForSelector             5 ms  internal:label="City"i >> nth=0
· 2026-05-17T19:44:27.934+00:00             Frame.click                      60 ms  internal:label="City"i >> nth=0
· 2026-05-17T19:44:28.611+00:00             Frame.fill                       36 ms  internal:label="City"i >> nth=0
· 2026-05-17T19:44:29.265+00:00             Frame.waitForSelector             7 ms  internal:label="ZIP Code"i >> nth=0
· 2026-05-17T19:44:29.276+00:00             Frame.click                     153 ms  internal:label="ZIP Code"i >> nth=0
· 2026-05-17T19:44:30.039+00:00             Frame.fill                       40 ms  internal:label="ZIP Code"i >> nth=0
· 2026-05-17T19:44:30.693+00:00             Frame.waitForSelector            13 ms  internal:label="State"i >> nth=0
· 2026-05-17T19:44:30.711+00:00             Frame.selectOption               33 ms  internal:label="State"i >> nth=0
· 2026-05-17T19:44:31.359+00:00             Frame.waitForTimeout            1.02 s  
· 2026-05-17T19:44:32.398+00:00              Page.screenshot                129 ms  
· 2026-05-17T19:44:32.541+00:00             Frame.evaluateExpression          6 ms  window.scrollTo(0, document.body.scrollHeight)
· 2026-05-17T19:44:32.550+00:00             Frame.waitForTimeout            1.01 s  
· 2026-05-17T19:44:33.568+00:00              Page.screenshot                100 ms  
```

---

_Generated by playwright_trace_runbook on 2026-05-17T19:44:47+00:00_