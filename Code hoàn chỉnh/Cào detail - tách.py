import csv
import datetime
import re
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
]

main_category = input("Nhập main_category: ")
sub_category = input("Nhập sub_category: ")

def calculate_shipping_days(estimated_delivery_date_str, crawl_date_str):
    try:
        estimated_delivery_date = datetime.datetime.strptime(estimated_delivery_date_str, '%A, %B %d')
        crawl_date = datetime.datetime.strptime(crawl_date_str, '%A, %B %d')
        return (estimated_delivery_date - crawl_date).days
    except ValueError:
        return 'N/A'

def clean_text(text):
    return re.sub(r'[\u200e]', '', text)

def detailproduct_bucket(soup, divs2I):
    dimension = asinid = datefirstavailable = manufactures = country = sellerrank = color = modelnumber = weight = price = priceamzship = eic = shipping_days = 'None'

    divs3 = divs2I.find_all('span', class_='a-text-bold')
    for div in divs3:
        if 'Package Dimensions' in div.text.strip() or 'Dimensions' in div.text.strip():
            div4 = div.find_next_sibling('span')
            dimension = clean_text(div4.text.strip() if div4 else 'None')
        elif 'Item model number' in div.text.strip():
            div4 = div.find_next_sibling('span')
            modelnumber = clean_text(div4.text.strip() if div4 else 'None')
        elif 'Date First Available' in div.text.strip():
            div4 = div.find_next_sibling('span')
            datefirstavailable = clean_text(div4.text.strip() if div4 else 'None')
        elif 'Manufacturer' in div.text.strip():
            div4 = div.find_next_sibling('span')
            manufactures = clean_text(div4.text.strip() if div4 else 'None')
        elif 'ASIN' in div.text.strip():
            div4 = div.find_next_sibling('span')
            asinid = clean_text(div4.text.strip() if div4 else 'None')
        elif 'Country of Origin' in div.text.strip():
            div4 = div.find_next_sibling('span')
            country = clean_text(div4.text.strip() if div4 else 'None')
        elif 'Best Sellers Rank' in div.text.strip():
            parent_tag = div.parent
            sellerrank = clean_text(parent_tag.get_text(strip=True))
        elif 'Color' in div.text.strip():
            div4 = div.find_next_sibling('span')
            color = clean_text(div4.text.strip() if div4 else 'Not Given')

    divs2Ia = soup.find('div', class_='a-popover-preload', id='a-popover-agShipMsgPopover')
    if (divs2Ia):
        table = divs2Ia.find('table', class_='a-lineitem')
        if (table):
            lines = table.find_all('td', class_='a-span9 a-text-left')
            for td in lines:
                if 'Price' in td.text:
                    divsprice = td.find_next_sibling('td', class_='a-span2 a-text-right')
                    price = clean_text(divsprice.text.strip() if divsprice else 'None')
                if 'AmazonGlobal Shipping' in td.text:
                    divsamzship = td.find_next_sibling('td', class_='a-span2 a-text-right')
                    priceamzship = clean_text(divsamzship.text.strip() if divsamzship else 'None')
                if 'Estimated Import Charges' in td.text:
                    diveic = td.find_next_sibling('td', class_='a-span2 a-text-right')
                    eic = clean_text(diveic.text.strip() if diveic else 'None')

    estimated_delivery_date_tag = soup.find('span', class_='a-text-bold')
    estimated_delivery_date = clean_text(estimated_delivery_date_tag.text.strip() if estimated_delivery_date_tag else 'N/A')
    crawl_date = datetime.datetime.now().strftime('%A, %B %d')
    shipping_days = calculate_shipping_days(estimated_delivery_date, crawl_date)
    
    return {
        "Dimension": dimension,
        "ASIN": asinid,
        "Date First Available": datefirstavailable,
        "Manufacturer": manufactures,
        "Country of Origin": country,
        "Best Sellers Rank": sellerrank,
        "Color": color,
        "Item Model Number": modelnumber,
        "Item Weight": weight,
        "Price": price,
        "AmazonGlobal Shipping": priceamzship,
        "Estimated Import Charges": eic,
        "Day Delivered": str(shipping_days)
    }

def detailproduct_table(soup, divs2):
    dimension = asinid = datefirstavailable = manufactures = country = sellerrank = color = modelnumber = weight = price = priceamzship = eic = shipping_days = 'None'

    divs3 = divs2.find_all('th', class_='a-color-secondary a-size-base prodDetSectionEntry')
    for div in divs3:
        if 'Manufacturer' in div.text.strip():
            divs7 = div.find_next_sibling('td', class_='a-size-base prodDetAttrValue')
            manufactures = clean_text(divs7.text.strip() if divs7 else 'None')
        if 'Dimensions' in div.text.strip():
            divs4 = div.find_next_sibling('td', class_='a-size-base prodDetAttrValue')
            dimension = clean_text(divs4.text.strip() if divs4 else 'None')
        if 'ASIN' in div.text.strip():
            divs5 = div.find_next_sibling('td', class_='a-size-base prodDetAttrValue')
            asinid = clean_text(divs5.text.strip() if divs5 else 'None')
        if 'Date First Available' in div.text.strip():
            divs6 = div.find_next_sibling('td', class_='a-size-base prodDetAttrValue')
            datefirstavailable = clean_text(divs6.text.strip() if divs6 else 'None')
        if 'Country of Origin' in div.text.strip():
            divs8 = div.find_next_sibling('td', class_='a-size-base prodDetAttrValue')
            country = clean_text(divs8.text.strip() if divs8 else 'None')
        if 'Best Sellers Rank' in div.text.strip():
            divs9 = div.find_next_sibling('td')
            sellerrank = clean_text(divs9.text.strip() if divs9 else 'None')
        if 'Color' in div.text.strip():
            divs10 = div.find_next_sibling('td', class_='a-size-base prodDetAttrValue')
            color = clean_text(divs10.text.strip() if divs10 else 'Not Given')
        if 'Item model number' in div.text.strip():
            divs11 = div.find_next_sibling('td', class_='a-size-base prodDetAttrValue')
            modelnumber = clean_text(divs11.text.strip() if divs11 else 'Not Given')
        if 'Item Weight' in div.text.strip():
            divs12 = div.find_next_sibling('td', class_='a-size-base prodDetAttrValue')
            weight = clean_text(divs12.text.strip() if divs12 else 'Not Given')

    divs2a = soup.find('div', class_='a-popover-preload', id='a-popover-agShipMsgPopover')
    if (divs2a):
        table = divs2a.find('table', class_='a-lineitem')
        if (table):
            lines = table.find_all('td', class_='a-span9 a-text-left')
            for td in lines:
                if 'Price' in td.text:
                    divsprice = td.find_next_sibling('td', class_='a-span2 a-text-right')
                    price = clean_text(divsprice.text.strip() if divsprice else 'None')
                if 'AmazonGlobal Shipping' in td.text:
                    divsamzship = td.find_next_sibling('td', class_='a-span2 a-text-right')
                    priceamzship = clean_text(divsamzship.text.strip() if divsamzship else 'None')
                if 'Estimated Import Charges' in td.text:
                    diveic = td.find_next_sibling('td', class_='a-span2 a-text-right')
                    eic = clean_text(diveic.text.strip() if diveic else 'None')

    estimated_delivery_date_tag = soup.find('span', class_='a-text-bold')
    estimated_delivery_date = clean_text(estimated_delivery_date_tag.text.strip() if estimated_delivery_date_tag else 'N/A')
    crawl_date = datetime.datetime.now().strftime('%A, %B %d')
    shipping_days = calculate_shipping_days(estimated_delivery_date, crawl_date)
    
    return {
        "Dimension": dimension,
        "ASIN": asinid,
        "Date First Available": datefirstavailable,
        "Manufacturer": manufactures,
        "Country of Origin": country,
        "Best Sellers Rank": sellerrank,
        "Color": color,
        "Item Model Number": modelnumber,
        "Item Weight": weight,
        "Price": price,
        "AmazonGlobal Shipping": priceamzship,
        "Estimated Import Charges": eic,
        "Day Delivered": str(shipping_days)
    }

url_list = pd.read_csv(f'DataSource\Part 1\part1_data_Baby_Gifts.csv')

results = []

retry_limit = 3  # Đặt giới hạn số lần thử lại

def create_driver(user_agent):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--log-level=3")
    return webdriver.Chrome(options=chrome_options)

# Khởi tạo driver đầu tiên
current_user_agent = user_agents[0]
driver = create_driver(current_user_agent)

count = 0
for urldetail in url_list['Link']:
    count += 1
    retry_count = 0
    success = False
    
    # Đổi User-Agent sau mỗi 10 lần duyệt
    if count % 5 == 0:
        driver.quit()  # Đóng driver hiện tại
        current_user_agent = user_agents[(count // 5) % len(user_agents)]  # Lấy User-Agent tiếp theo trong danh sách
        driver = create_driver(current_user_agent)  # Khởi tạo driver mới với User-Agent mới
    
    print(f"Lần lấy thông tin thứ: {count} với User-Agent: {current_user_agent}")

    while retry_count < retry_limit and not success:
        try:
            driver.get(urldetail)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'prodDetails')) or 
                EC.presence_of_element_located((By.ID, 'detailBulletsWrapper_feature_div'))
            )
            success = True
        except TimeoutException:
            retry_count += 1
            print(f"Timeout while waiting for page to load: {urldetail}. Retrying {retry_count}/{retry_limit}")
            time.sleep(5)  # Chờ 5 giây trước khi thử lại

    if not success:
        print(f"Failed to load page after {retry_limit} attempts: {urldetail}")
        continue

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    divs2 = soup.find('div', id='prodDetails')
    divs2I = soup.find('div', id='detailBulletsWrapper_feature_div')

    if divs2:
        result = detailproduct_table(soup, divs2)
    elif divs2I:
        result = detailproduct_bucket(soup, divs2I)
    
    if result:
        results.append(result)
    
    print(result)

driver.quit()

filename = f"part2_dataDetail_{main_category}_{sub_category}.csv"
with open(filename, 'w', newline="", encoding='utf-8') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=result.keys())
    csv_writer.writeheader()
    csv_writer.writerows(results)

print(f"Completed scraping and saved to {filename}.")
