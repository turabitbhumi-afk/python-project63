# from firecrawl import Firecrawl
# from pydantic import BaseModel
# from typing import Optional
#
# app = Firecrawl(api_key="fc-b12746b9b977463eb586f217cb91d122")
#
# class BookInfo(BaseModel):
#     title: str
#     price: str
#     stock: str
#     rating: Optional[str] = None
#
# result = app.extract(
#     ["https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"],
#     prompt="Extract the book title, price, stock availability and star rating.",
#     schema=BookInfo.model_json_schema()
# )
#
# # Access data via result.data
# data = result.data
#
# print(f"title:  {data['title']}")
# print(f"price:  {data['price']}")
# print(f"stock:  {data['stock']}")
# print(f"rating: {data['rating']}")

# ----------------------------------------------------------------------------------------
# from firecrawl import Firecrawl
# import re
#
# app = Firecrawl(api_key="fc-b12746b9b977463eb586f217cb91d122")
#
# urls = [
#     "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
#     "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
#     "https://books.toscrape.com/catalogue/soumission_998/index.html",
# ]
#
# for url in urls:
#     result = app.scrape(url, formats=["markdown"])
#     md = result.markdown
#
#     # Parse from Markdown using simple string search
#     lines = md.split("\n")
#
#     title = ""
#     price = ""
#     stock = ""
#     rating = ""
#
#     for line in lines:
#         line = line.strip()
#         if line.startswith("# "):
#             title = line.replace("# ", "")
#         if "£" in line and not price:
#             price = line.strip()
#         if "In stock" in line or "available" in line.lower():
#             stock = line.strip()
#         if "star-rating" in line.lower() or "rating" in line.lower():
#             rating = line.strip()
#
#     print(f"title:  {title}")
#     print(f"url:    {url}")
#     print(f"price:  {price}")
#     print(f"stock:  {stock}")
#     print("-" * 40)

# ----------------------------------------------------------------------------------------------

from firecrawl import Firecrawl

app = Firecrawl(api_key="fc-b12746b9b977463eb586f217cb91d122")

# Step 1: Auto-discover ALL URLs on the site
print("Mapping site...")
book_urls = []

# Loop through all 50 listing pages
for page_num in range(1, 51):
    if page_num == 1:
        url = "https://books.toscrape.com/catalogue/page-1.html"
    else:
        url = f"https://books.toscrape.com/catalogue/page-{page_num}.html"

    print(f"Scanning listing page {page_num}/50...")
    result = app.scrape(url, formats=["links"])

    # Filter links to book detail pages only
    if result.links:
        page_books = [link for link in result.links if "/catalogue/" in link and "index.html" in link
            and "page-" not in link and "category" not in link]
        book_urls.extend(page_books)
        print(f" Found {len(page_books)} books on this page")

# Remove duplicates
book_urls = list(set(book_urls))
print(f"\nTotal unique book URLs: {len(book_urls)}")

books = []
for i, url in enumerate(book_urls[:10]):  # limit to 10 for now to save credits
    print(f"Scraping [{i+1}/{len(book_urls[:10])}]: {url}")

    result = app.scrape(url, formats=["markdown"])
    md = result.markdown
    lines = md.split("\n")

    title = ""
    price = ""
    stock = ""

    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            title = line.replace("# ", "")
        if "£" in line and not price:
            price = line.strip()
        if "In stock" in line or "available" in line.lower():
            stock = line.strip()

    # Append to list as a dict
    books.append({
        "title": title,
        "url":   url,
        "price": price,
        "stock": stock,
    })

    print(f"  title: {title}")
    print(f"  price: {price}")
    print(f"  stock: {stock}")
    print("-" * 40)

# Step 4: Print full list at end
print(f"\nTotal books scraped: {len(books)}")
for book in books:
    print(book)
