# from playwright.sync_api import sync_playwright
#
# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)
#     page = browser.new_page()
#     page.goto("https://example.com")
#
#     print(page.title())
#
#     browser.close()


# from playwright.sync_api import sync_playwright
#
# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)
#     page = browser.new_page()
#     page.goto("https://quotes.toscrape.com/")
#
#     page.wait_for_selector(".quote")
#
#     quotes = page.locator(".quote").all_text_contents()
#     print(quotes)
#
#     browser.close()



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