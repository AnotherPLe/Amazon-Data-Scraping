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
url = f'https://www.amazon.com/s?i=fashion-luggage&bbn=16225017011&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A15743241&ref=nav_em__nav_desktop_sa_intl_travel_totes_0_2_19_5'


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

        #driver.get(url)
        #time.sleep(😎)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        divs = divs1.find_all('div', 'sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small')
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

        #driver.get(url)
        #time.sleep(😎)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        divs = divs2.find_all('div', class_ ='sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 AdHolder sg-col s-widget-spacing-small sg-col-4-of-20a')

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
divs1 = soup.find('div', 's-main-slot s-result-list s-search-results sg-row')
#print(divs1)
divs2 = soup.find('div','sg-col-20-of-24 s-matching-dir sg-col-16-of-20 sg-col sg-col-8-of-12 sg-col-12-of-16')
#print(divs2)
if not divs1 and divs2:
    print("Not found divs1 and found divs2 \n Đang thực hiện crawl theo hàng sản phẩm()...")
    findasrow(url)  # Truyền url vào hàm findasrow()
elif divs1 and not divs2:
    print("Not found divs2 and found divs1 \n Đang thực hiện crawl theo ô sản phẩm ()...")
    crawlastiles(url)  # Truyền url vào hàm crawlastiles()
elif not divs1 and not divs2:
    print("Not found divs1 and divs2 \n Đang thực hiện crawl theo ô sản phẩm, sản phẩm chỉ có 1 trang ()...")
    crawlastiles1page(url)  # Truyền url vào hàm crawlastiles()