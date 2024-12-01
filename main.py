import lxml
import requests
from bs4 import BeautifulSoup
import smtplib
import datetime

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,ko;q=0.8"
}

# Fetch the webpage
URL = "https://www.amazon.com/Oura-Ring-Gen3-Horizon-Tracking/dp/B0CSRH4K16?pd_rd_w=95Ek5&content-id=amzn1.sym.858a37e4-ceb7-4ae1-aac1-bad735ee2e4d&pf_rd_p=858a37e4-ceb7-4ae1-aac1-bad735ee2e4d&pf_rd_r=9NFV3PSY9F76NCWBNACK&pd_rd_wg=2ycYQ&pd_rd_r=9a08e2a6-b55e-4b11-824d-a843549c163a&pd_rd_i=B0CSRH4K16&ref_=pd_hp_d_btf_unk_B0CSRH4K16&th=1"
response = requests.get(URL, headers= header)
amazon_website = response.text

# Parse the HTML content
# If ‘bs4.FeatureNotFound: Couldn't find a tree builder with the features you requested: html-parser.’
# error message shows then use lxml feature instead of html.parser
soup = BeautifulSoup(amazon_website, "lxml")
whole_price = soup.find("span", class_="a-price-whole").text
decimal_price = soup.find("span", class_="a-price-fraction").text
price = float(f"{whole_price}{decimal_price}")

current_time = datetime.datetime.now()

if price <= 300 and current_time.hour == 9 and current_time.minute == 0:
    msg = "Your saved item is below $300 now!"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        result = connection.login(YOUR_EMAIL, YOUR_PASSWORD)
        connection.sendmail(
            from_addr="John Doe <john@doe.net>",
            to_addrs="foo@bar.com",
            msg=f"Subject:Amazon Price Alert!\n\n{msg}\n{URL}".encode("utf-8")
        )
else:
    print("Not less than $300")


