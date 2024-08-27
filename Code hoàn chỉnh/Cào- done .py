# Import các thư viện và cài đặt chrome options
import os
import re
import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm.auto import tqdm
import time
import datetime
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent



main_category = input("Nhập main_category: ")
sub_category = input("Nhập sub_category: ")
numberpage = int(input("Nhập số lượng trang cần cào: "))
numbercrawl = numberpage + 1

# Cấu hình Chrome Options
chrome_options = Options()
ua = UserAgent()
random_user_agent = ua.random
chrome_options.add_argument("--headless")  # Chạy ở chế độ không hiển thị giao diện
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")  # Bỏ qua sử dụng GPU
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")



# Sử dụng ChromeDriverManager để tự động tải và cài đặt ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Khởi tạo trình duyệt WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Khai báo các danh sách để lưu thông tin sản phẩm
product_names = []
prices = []
links = []
ratings = []
reviews = []


# URL của trang tìm kiếm trên Amazon
url = f'https://www.amazon.com/s?i=specialty-aps&bbn=16225008011&rh=n%3A%2116225008011%2Cn%3A5223262011&ref=nav_em__nav_desktop_sa_intl_programming_web_development_0_2_22_15'


# Hàm cào dữ liệu khi mỗi sản phẩm được hiển thị trên một hàng
def findasrow(url):
    for i in tqdm(range(1, numbercrawl), desc="Data From Amazon"):
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        divs = soup.find_all('div', 'a-section a-spacing-small a-spacing-top-small')    
        temp = 0
        for div in divs:
            if temp == 0:
                temp += 1
                continue
            product = div.find('a', 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
            if product is None:
                product_names.append(None)
            else:
                product_names.append(product.text)

            link = div.find('a', 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
            if link is None:
                links.append(None)
            else:
                links.append("https://www.amazon.com/" + link.get('href'))

            price = div.find('span', 'a-price-whole')
            if price is None:
                prices.append(None)
            else:
                prices.append(price.text)

            rate = div.find('span', 'a-icon-alt')
            if rate is None:
                if link is None:
                    pass
                ratings.append(None)
            else:
                ratings.append(rate.text.split()[0])

            review = div.find('span', 'a-size-base s-underline-text')
            if review is None:
                if link is None:
                    pass
                reviews.append(None)
            else:
                reviews.append(review.text)

        divs_pagination = soup.find('div', 'a-section a-text-center s-pagination-container')
        if not divs_pagination:
            print(" EComplete get data")
            break
        else:
            next_page_link = divs_pagination.find('a', 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator')
            if not next_page_link:
                print("Completed")
                break
            else:
                url = "https://www.amazon.com/" + next_page_link.get('href')

    # Lưu dữ liệu vào file CSV
    print("Length of products: ", len(product_names))
    print("Length of prices: ", len(prices))
    print("Length of links: ", len(links))
    print("Length of ratings: ", len(ratings))
    print("Length of reviews: ", len(reviews))

    # Tạo DataFrame từ dữ liệu
    df = pd.DataFrame({
        'Product Name': product_names,
        'Price': prices,
        'Rating': ratings,
        'Review': reviews,
        'Link': links
    })

    # Đường dẫn thư mục đích
    folder_path = r'D:\\LNTP ở HUST\\Học tập\\Năm 3\\20232\\Đồ án 1\\Data-Crawling-Of-Amazon-main\\Data-Crawling-Of-Amazon-main\\DataSource\\Part 1'

    # Kiểm tra và tạo thư mục nếu chưa tồn tại
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Lưu file CSV vào thư mục đã tạo
    df.to_csv(os.path.join(folder_path, f'part1_data_{main_category}_{sub_category}.csv'), index=False, encoding='utf-8-sig')
    print(f"SAVED THE FILE!!! part1_data_{main_category}_{sub_category}.csv")

# Hàm cào dữ liệu khi mỗi sản phẩm được hiển thị trong một ô nhiều trang
def crawlastiles(url):
    for i in tqdm(range(1,numbercrawl), desc="Data From Amazon"):

        driver.get(url)
        #time.sleep(😎)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        divs = soup.find_all('div', 'sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20')
        for div in divs:
            product = div.find('a', 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
            if product is None:
                product_names.append(None)
            else:
                product_names.append(product.text)
            
            link = div.find('a', 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
            if link is None:
                links.append(None)
            else:
                links.append("https://www.amazon.com/" + link.get('href'))
            
            price = div.find('span', 'a-price-whole')
            if price is None:
                prices.append(None)
            else:
                prices.append(price.text)
            
            rate = div.find('span', 'a-icon-alt')
            if rate is None:
                if link is None:
                    pass
                ratings.append(None)
            else:
                ratings.append(rate.text.split()[0])
            
            reviewnumber = div.find('span','a-size-base s-underline-text')
            if reviewnumber is None:
                if link is None:
                    pass
                reviews.append(None)
            else:
                reviews.append(reviewnumber.text)

        divs_pagination = soup.find('div', 'a-section a-text-center s-pagination-container')
        if not divs_pagination:
            print("Complete get data")
            break
        else:
            next_page_link = divs_pagination.find('a','s-pagination-item s-pagination-next s-pagination-button s-pagination-separator')
            if not next_page_link:
                print("Completed, end of pagination")
                break
            else:
                url = "https://www.amazon.com" + next_page_link.get('href')
                driver.get(url)

    # Lưu dữ liệu vào file CSV
    print("Length of products: ", len(product_names))
    print("Length of prices: ", len(prices))
    print("Length of links: ", len(links))
    print("Length of ratings: ", len(ratings))
    print("Length of reviews: ", len(reviews))

    
    
    # Tạo DataFrame từ dữ liệu
    df = pd.DataFrame({
        'Product Name': product_names,
        'Price': prices,
        'Rating': ratings,
        'Review': reviews,
        'Link': links
    })

    # Đường dẫn thư mục đích
    folder_path = r'D:\\LNTP ở HUST\\Học tập\\Năm 3\\20232\\Đồ án 1\\Data-Crawling-Of-Amazon-main\\Data-Crawling-Of-Amazon-main\\DataSource\\Part 1'

    # Kiểm tra và tạo thư mục nếu chưa tồn tại
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Lưu file CSV vào thư mục đã tạo
    df.to_csv(os.path.join(folder_path, f'part1_data_{main_category}_{sub_category}.csv'), index=False, encoding='utf-8-sig')
    print(f"SAVED THE FILE!!! part1_data_{main_category}_{sub_category}.csv")

# Hàm cào dữ liệu khi mỗi sản phẩm được hiển thị trong một ô 1 trang trang
def crawlastiles1page(url):
    for i in tqdm(range(1,numbercrawl), desc="Data From Amazon"):

        driver.get(url)
        #time.sleep(😎)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        divs = soup.find_all('div', 'sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 AdHolder sg-col s-widget-spacing-small sg-col-4-of-20')

        for div in divs:

            product = div.find('a', 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
            if product is None:
                product_names.append(None)
            else:
                product_names.append(product.text)
            
            link = div.find('a', 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
            if link is None:
                links.append(None)
            else:
                links.append("https://www.amazon.com/" + link.get('href'))
            
            price = div.find('span', 'a-price-whole')
            if price is None:
                prices.append(None)
            else:
                prices.append(price.text)
            
            rate = div.find('span', 'a-icon-alt')
            if rate is None:
                if link is None:
                    pass
                ratings.append(None)
            else:
                ratings.append(rate.text.split()[0])
            
            reviewnumber = div.find('span','a-size-base s-underline-text')
            if reviewnumber is None:
                if link is None:
                    pass
                reviews.append(None)
            else:
                reviews.append(reviewnumber.text)

    
    # Lưu dữ liệu vào file CSV
    print("Length of products: ", len(product_names))
    print("Length of prices: ", len(prices))
    print("Length of links: ", len(links))
    print("Length of ratings: ", len(ratings))
    print("Length of reviews: ", len(reviews))
    
    # Tạo DataFrame từ dữ liệu
    df = pd.DataFrame({
        'Product Name': product_names,
        'Price': prices,
        'Rating': ratings,
        'Review': reviews,
        'Link': links
    })

    # Đường dẫn thư mục đích
    folder_path = r'D:\\LNTP ở HUST\\Học tập\\Năm 3\\20232\\Đồ án 1\\Data-Crawling-Of-Amazon-main\\Data-Crawling-Of-Amazon-main\\DataSource\\Part 1'

    # Kiểm tra và tạo thư mục nếu chưa tồn tại
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Lưu file CSV vào thư mục đã tạo
    df.to_csv(os.path.join(folder_path, f'part1_data_{main_category}_{sub_category}.csv'), index=False, encoding='utf-8-sig')
    print(f"SAVED THE FILE!!! part1_data_{main_category}_{sub_category}.csv")

# Kiểm tra cách trình bày sản phẩm để quyết định cách thực hiện việc cào dữ liệu
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'html.parser')
divs = soup.find_all('div', 's-main-slot s-result-list s-search-results sg-row')
print(divs)
div1 = soup.find_all('div','sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 AdHolder sg-col s-widget-spacing-small sg-col-4-of-20')
print(div1)
if not divs and not div1:
    print("Đang thực hiện crawl theo hàng sản phẩm()...")
    findasrow(url)  # Truyền url vào hàm findasrow()
elif divs:
    print("Đang thực hiện crawl theo ô sản phẩm ()...")
    crawlastiles(url)  # Truyền url vào hàm crawlastiles()
elif div1:
    print("Đang thực hiện crawl theo ô sản phẩm, sản phẩm chỉ có 1 trang ()...")
    crawlastiles1page(url)  # Truyền url vào hàm crawlastiles()
    

#--------------------------------------------------------------------part2: cào chi tiết sản phẩm:


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
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.183 Safari/537.36"
]



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

url_list = pd.read_csv(f'D:\\LNTP ở HUST\\Học tập\\Năm 3\\20232\\Đồ án 1\\Data-Crawling-Of-Amazon-main\\Data-Crawling-Of-Amazon-main\\DataSource\\Part 1\\part1_data_{main_category}_{sub_category}.csv')

retry_limit = 1  # Đặt giới hạn số lần thử lại

results = {}

def create_driver(user_agent):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-gpu")  # Bỏ qua sử dụng GPU
    return webdriver.Chrome(options=chrome_options)

import csv
import pandas as pd

# Mở file CSV trước vòng lặp và ghi tiêu đề
filename = f"D:\\LNTP ở HUST\\Học tập\\Năm 3\\20232\\Đồ án 1\\Data-Crawling-Of-Amazon-main\\Data-Crawling-Of-Amazon-main\\DataSource\\Part 2\\part2_dataDetail_{main_category}_{sub_category}.csv"
with open(filename, 'w', newline="", encoding='utf-8') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=[
        "Dimension", "ASIN", "Date First Available", "Manufacturer", 
        "Country of Origin", "Best Sellers Rank", "Color", "Item Model Number",
        "Item Weight", "Price", "AmazonGlobal Shipping", "Estimated Import Charges", 
        "Day Delivered"
    ])
    csv_writer.writeheader()

retry_limit = 1  # Đặt giới hạn số lần thử lại

results = {}

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
    
    # Đổi User-Agent sau mỗi 5 lần duyệt
    if count % 3 == 0:
        driver.quit()  # Đóng driver hiện tại
        current_user_agent = user_agents[(count // 3) % len(user_agents)]  # Lấy User-Agent tiếp theo trong danh sách
        driver = create_driver(current_user_agent)  # Khởi tạo driver mới với User-Agent mới
    
    print(f"Lần lấy thông tin thứ: {count} với User-Agent: {current_user_agent}")

    while retry_count < retry_limit and not success:
        try:
            driver.get(urldetail)
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.ID, 'prodDetails')) or 
                EC.presence_of_element_located((By.ID, 'detailBulletsWrapper_feature_div'))
            )
            success = True
        except TimeoutException:
            retry_count += 1
            print(f"Timeout while waiting for page to load: {urldetail}. Retrying {retry_count}/{retry_limit}")

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
        # Ghi kết quả vào file CSV
        with open(filename, 'a', newline="", encoding='utf-8') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=[
                "Dimension", "ASIN", "Date First Available", "Manufacturer", 
                "Country of Origin", "Best Sellers Rank", "Color", "Item Model Number",
                "Item Weight", "Price", "AmazonGlobal Shipping", "Estimated Import Charges", 
                "Day Delivered"
            ])
            csv_writer.writerow(result)

    print(result)

driver.quit()

print(f"Completed scraping and saved to {filename}.")
