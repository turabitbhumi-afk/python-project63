# import requests
# from parsel import Selector
#
# cookies = {
#     'session-id': '147-2166995-8636247',
#     'session-id-time': '2082787201l',
#     'ad-oo': '0',
#     'ci': 'eyJhZ2VTaWduYWwiOiJBRFVMVCIsImlzR2RwciI6ZmFsc2V9',
#     'ubid-main': '135-4785202-6931800',
#     'session-token': '1vBKiyYb/YsYEcFHRbyn2EC7swe7raZuDPlV6KKX+uc8mNaK4wNMTctEG3EK6m1YKDm9wLvuVTUE2prin91xjy6hZXqmtB8wGRZ7lYLgnKorNP5Rfj4xL4cSTLEUGz/fj/O5YEnPbeMPZjmRmVVFehun51V6cOk6/OMHsp+azYTjHdJMEihRkAvUc8pf8CWg9sILek1l10IH4iWdkeyYm+JMRl8dDc+8',
#     'csm-hit': 'tb:FTRD7X0WXFZ6Q0CN9ECE+s-R2XT2NCPJXSXDN3N2455|1775112650326&t:1775112650326&adb:adblk_no',
#     'aws-waf-token': '2a9646eb-2f67-469e-8c8f-869f0af938a9:EQoAn00vjSA0AAAA:CIrPuT/kms2jZU54i0p6ETc7PVzYelB2X2bRMwalqmmbJfrtUhrnl3IZYBktImv0936DdaDxmpB9IDsc1tDAyamwlistSYJdDXYQRaUYwSZyyFIfxafWNvcsM/0qOa+1u0RFFKlrpbRLvQucgrL9vT9MldNnDJdzX+HykDQ7w2kDwoidvFsWlrYfmf0dOaU=',
# }
#
# headers = {
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
#     'cache-control': 'max-age=0',
#     'priority': 'u=0, i',
#     'referer': 'https://www.imdb.com/chart/top/',
#     'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'document',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'same-origin',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
#     # 'cookie': 'session-id=147-2166995-8636247; session-id-time=2082787201l; ad-oo=0; ci=eyJhZ2VTaWduYWwiOiJBRFVMVCIsImlzR2RwciI6ZmFsc2V9; ubid-main=135-4785202-6931800; session-token=1vBKiyYb/YsYEcFHRbyn2EC7swe7raZuDPlV6KKX+uc8mNaK4wNMTctEG3EK6m1YKDm9wLvuVTUE2prin91xjy6hZXqmtB8wGRZ7lYLgnKorNP5Rfj4xL4cSTLEUGz/fj/O5YEnPbeMPZjmRmVVFehun51V6cOk6/OMHsp+azYTjHdJMEihRkAvUc8pf8CWg9sILek1l10IH4iWdkeyYm+JMRl8dDc+8; csm-hit=tb:FTRD7X0WXFZ6Q0CN9ECE+s-R2XT2NCPJXSXDN3N2455|1775112650326&t:1775112650326&adb:adblk_no; aws-waf-token=2a9646eb-2f67-469e-8c8f-869f0af938a9:EQoAn00vjSA0AAAA:CIrPuT/kms2jZU54i0p6ETc7PVzYelB2X2bRMwalqmmbJfrtUhrnl3IZYBktImv0936DdaDxmpB9IDsc1tDAyamwlistSYJdDXYQRaUYwSZyyFIfxafWNvcsM/0qOa+1u0RFFKlrpbRLvQucgrL9vT9MldNnDJdzX+HykDQ7w2kDwoidvFsWlrYfmf0dOaU=',
# }
#
# response = requests.get('https://www.imdb.com/chart/top/', cookies=cookies, headers=headers)
# print(response.status_code)


from firecrawl import Firecrawl
import csv
import re

app = Firecrawl(api_key="fc-b12746b9b977463eb586f217cb91d122")

print("Scraping IMDb Top 250...")
result = app.scrape("https://www.imdb.com/chart/top/",formats=["markdown"])

md = result.markdown
lines = [line.strip() for line in md.split("\n") if line.strip()]

movies = []
i = 0

while i < len(lines):
    line = lines[i]

    # Match rank lines like #1, #2, ... #250
    if re.match(r'^#\d+$', line):
        rank = line.replace("#", "")

        title = ""
        year  = ""
        rating = ""

        # Look at next few lines
        for j in range(i + 1, min(i + 6, len(lines))):
            next_line = lines[j]

            # Title is inside [**Title**](url) — extract just the title
            title_match = re.search(r'\[\*\*(.+?)\*\*\]', next_line)
            if title_match and not title:
                title = title_match.group(1)

            # Year is merged like "19942h 22mR" — first 4 digits
            elif re.match(r'^\d{4}\d+h', next_line):
                year = next_line[:4]

            # Rating like "9.3 (3.2M)Rate"
            elif re.match(r'^\d+\.\d+\s*\(', next_line) and not rating:
                rating = re.match(r'^(\d+\.\d+)', next_line).group(1)

        if title:
            movies.append({
                "rank":   rank,
                "title":  title,
                "year":   year,
                "rating": rating,
            })
            print(f"#{rank:<4} {title:<45} {year}  {rating}⭐")

    i += 1

print(movies)
print(f"\nTotal movies found: {len(movies)}")


