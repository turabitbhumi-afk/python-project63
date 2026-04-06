from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False,args=["--start-maximized"])
    context = browser.new_context(no_viewport=True)
    page = context.new_page()

    page.goto("https://webscraper.io/test-sites/e-commerce/ajax")
    name = page.locator(".title").all_text_contents()
    name = [name.strip() for name in name]
    page.locator('a[href="/test-sites/e-commerce/ajax/computers"]').click()
    page.locator('a[href="/test-sites/e-commerce/ajax/computers/laptops"]').click()

    while True:
        products = page.locator(".col-lg-4")

        for i in range(products.count()):
            name = products.nth(i).locator(".title").text_content().strip()
            price = products.nth(i).locator("h4.pull-right").text_content().strip()
            print(name, price)

        next_button = page.locator(".next")

        if not next_button:
            break

        next_button.click()
        page.wait_for_timeout(2000)

    browser.close()



# Playwright E-commerce Scraper
# Site: webscraper.io/test-sites/e-commerce/ajax
# Scrapes: laptop names and prices with pagination

# from playwright.sync_api import sync_playwright
# import csv

# def scrape_laptops():
#     results = []

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)  # headless=True for production
#         page = browser.new_page()

#         print("Opening site...")
#         page.goto("https://webscraper.io/test-sites/e-commerce/ajax")

#         # Navigate to laptops category
#         page.locator('a[href="/test-sites/e-commerce/ajax/computers"]').click()
#         page.wait_for_load_state("networkidle")

#         page.locator('a[href="/test-sites/e-commerce/ajax/computers/laptops"]').click()
#         page.wait_for_load_state("networkidle")

#         page_num = 1

#         while True:
#             print(f"Scraping page {page_num}...")
#             page.wait_for_selector(".col-lg-4")

#             products = page.locator(".col-lg-4")
#             count = products.count()
#             print(f"Found {count} products")

#             for i in range(count):
#                 try:
#                     name  = products.nth(i).locator(".title").text_content().strip()
#                     price = products.nth(i).locator("h4.pull-right").text_content().strip()
#                     results.append({"name": name, "price": price})
#                     print(f"  {name} — {price}")
#                 except Exception as e:
#                     print(f"  Error on product {i}: {e}")
#                     continue

#             # Check if next page exists
#             next_btn = page.locator(".next")
#             if next_btn.count() == 0 or "disabled" in (next_btn.get_attribute("class") or ""):
#                 print("All pages scraped!")
#                 break

#             next_btn.click()
#             page.wait_for_load_state("networkidle")
#             page_num += 1

#         browser.close()

#     # Save to CSV
#     with open("laptops.csv", "w", newline="", encoding="utf-8") as f:
#         writer = csv.DictWriter(f, fieldnames=["name", "price"])
#         writer.writeheader()
#         writer.writerows(results)

#     print(f"\nDone! {len(results)} laptops saved to laptops.csv")
#     return results

# if __name__ == "__main__":
#     scrape_laptops()
