import datetime
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Tạo chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Chạy ẩn danh (tạm thời tắt để xem trang web)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# Hàm để tính số ngày vận chuyển dự kiến
def calculate_shipping_days(estimated_delivery_date_str, crawl_date_str):
    estimated_delivery_date = datetime.datetime.strptime(estimated_delivery_date_str, '%A, %B %d')
    crawl_date = datetime.datetime.strptime(crawl_date_str, '%A, %B %d')
    return (estimated_delivery_date - crawl_date).days

# Khởi tạo trình duyệt WebDriver
driver = webdriver.Chrome(options=chrome_options)

# URL sản phẩm trên Amazon
urldetail = 'https://www.amazon.com/SteelSeries-Arctis-Multi-Platform-Gaming-Headset/dp/B09ZWMYHCT/ref=sr_1_1_sspa?_encoding=UTF8&content-id=amzn1.sym.12129333-2117-4490-9c17-6d31baf0582a&dib=eyJ2IjoiMSJ9.WJZIGcfaxHH2NU1LngCUay4gxKxdbmUPMgelA_mwm_UV5fyJFuahG7L_kqAdMtjZxmCucyPrb_RJ0gBVnbyJ0wR-JhDck8p_a8kyIqlwlxYmLuBlnd72ujs15DRlKfHHogriLpe_f0jAizDfJ82LCaHh4JOXWrva9cGdwoxDqPbIG3Ki0-ymlYzBk-gWTqd05kK8bHjX7OwNE1UaRigDE5a0GY1vSlMbxb4x9LS5uP4.os-uAzsoXmJMDUTBN9dF0L-HrmvS1nqFZlfvpZIx4BY&dib_tag=se&keywords=gaming+headsets&pd_rd_r=709ef533-1527-4e0c-8ae0-ddb0250c0aa5&pd_rd_w=bfwJn&pd_rd_wg=1AoCi&pf_rd_p=12129333-2117-4490-9c17-6d31baf0582a&pf_rd_r=RT1CZQJNZMK97TRP2EPN&qid=1715979545&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1'
# Truy cập trang web
driver.get(urldetail)

# Sử dụng BeautifulSoup để phân tích HTML
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Khai báo các biến ban đầu để lưu kết quả
dimension = asinid = datefirstavailable = manufactures = country = sellerrank = color = modelnumber = weight = price = priceamzship = eic = shipping_days = 'None'

# Tìm div chứa thông tin chi tiết sản phẩm
divs2 = soup.find('div', id='prodDetails')
divs2I = soup.find('div', id='detailBulletsWrapper_feature_div')

def detailproduct_bucket(divs2I):
    global dimension, asinid, datefirstavailable, manufactures, country, sellerrank, color, modelnumber, weight, price, priceamzship, eic

    # Tìm tất cả các thẻ <th> trong divs2I với class 'a-color-secondary a-size-base prodDetSectionEntry'
    divs3 = divs2I.find_all('span', class_='a-text-bold')
    
    # Lặp qua các thẻ <th> để tìm kiếm thông tin
    for div in divs3:
        # Tìm thông tin về kích thước đóng gói
        if 'Package Dimensions' or 'Dimensions' in div.text.strip():
            div4 = div.find_next_sibling('span')
            dimension = div4.text.strip() if div4 else 'None'
 
        
        # Tìm thông tin về số model sản phẩm
        elif 'Item model number' in div.text.strip():
            div4 = div.find_next_sibling('span')
            modelnumber = div4.text.strip() if div4 else 'None'

            
        # Tìm thông tin về ngày sản phẩm được phát hành lần đầu tiên
        elif 'Date First Available' in div.text.strip():
            div4 = div.find_next_sibling('span')
            datefirstavailable = div4.text.strip() if div4 else 'None'

            
        # Tìm thông tin về nhà sản xuất
        elif 'Manufacturer' in div.text.strip():
            div4 = div.find_next_sibling('span')
            manufactures = div4.text.strip() if div4 else 'None'
            
        # Tìm thông tin về ASIN
        elif 'ASIN' in div.text.strip():
            div4 = div.find_next_sibling('span')
            asinid = div4.text.strip() if div4 else 'None'
            
        # Tìm thông tin về quốc gia xuất xứ
        elif 'Country of Origin' in div.text.strip():
            div4 = div.find_next_sibling('span')
            country = div4.text.strip() if div4 else 'None'

        # Tìm thông tin về xếp hạng sản phẩm
        if 'Best Sellers Rank' in div.text.strip():
            # Tìm thẻ cha chứa "Best Sellers Rank:"
            parent_tag = div.parent

            # Lấy toàn bộ text của thẻ cha
            sellerrank = parent_tag.get_text(strip=True)

        # Tìm màu    
        elif 'Color' in div.text.strip():
            div4 = div.find_next_sibling('span')
            color = div4.text.strip() if div4 else 'Not Given'

    divs2Ia = soup.find('div', class_='a-popover-preload', id='a-popover-agShipMsgPopover')
    if divs2Ia:
        print("Found divs2Ia:")
        # Tìm table trong divs2Ia
        table = divs2Ia.find('table', class_='a-lineitem')
        if table:
            print("Found table")
            lines = table.find_all('td', class_='a-span9 a-text-left')
            for td in lines:
                if 'Price' in td.text:
                    divsprice = td.find_next_sibling('td', class_='a-span2 a-text-right')
                    price = divsprice.text.strip() if divsprice else 'None'
                if 'AmazonGlobal Shipping' in td.text:
                    divsamzship = td.find_next_sibling('td', class_='a-span2 a-text-right')
                    priceamzship = divsamzship.text.strip() if divsamzship else 'None'
                if 'Estimated Import Charges' in td.text:
                    diveic = td.find_next_sibling('td', class_='a-span2 a-text-right')
                    eic = diveic.text.strip() if diveic else 'None'

    #tìm số ngày vận chuyển dự kiến
    estimated_delivery_date = soup.find('span', class_='a-text-bold').text.strip()
    crawl_date = datetime.datetime.now().strftime('%A, %B %d')
    shipping_days = calculate_shipping_days(estimated_delivery_date, crawl_date)
    return shipping_days

#hàm
def detailproduct_table(divs2):
    global dimension, asinid, datefirstavailable, manufactures, country, sellerrank, color, modelnumber, weight, price, priceamzship, eic

    # Tìm tất cả các thẻ <th> trong divs2 với class 'a-color-secondary a-size-base prodDetSectionEntry'
    divs3 = divs2.find_all('th', class_='a-color-secondary a-size-base prodDetSectionEntry')

    # Lặp qua các thẻ <th> để tìm kiếm thông tin
    for div in divs3:
        # Tìm manufacturers
        if 'Manufacturer' in div.text.strip():
            divs7 = div.find_next_sibling('td', class_='a-size-base prodDetAttrValue')
            manufactures = divs7.text.strip() if divs7 else 'None'

        # Tìm Dimension
        if 'Dimensions' in div.text.strip():
            divs4 = div.find_next_sibling('td', class_='a-size-base prodDetAttrValue')
            dimension = divs4.text.strip() if divs4 else 'None'

        # Tìm ASIN của sản phẩm
        if 'ASIN' in div.text.strip():
            divs5 = div.find_next_sibling('td', class_='a-size-base prodDetAttrValue')
            asinid = divs5.text.strip() if divs5 else 'None'

        # Tìm Date_First_Available
        if 'Date First Available' in div.text.strip():
            divs6 = div.find_next_sibling('td', class_='a-size-base prodDetAttrValue')
            datefirstavailable = divs6.text.strip() if divs6 else 'None'

        # Tìm Country
        if 'Country of Origin' in div.text.strip():
            divs8 = div.find_next_sibling('td', class_='a-size-base prodDetAttrValue')
            country = divs8.text.strip() if divs8 else 'None'

        # Tìm Best Sellers Rank
        if 'Best Sellers Rank' in div.text.strip():
            divs9 = div.find_next_sibling('td')
            sellerrank = divs9.text.strip() if divs9 else 'None'

        # Tìm màu
        if 'Color' in div.text.strip():
            divs10 = div.find_next_sibling('td', class_='a-size-base prodDetAttrValue')
            color = divs10.text.strip() if divs10 else 'Not Given'

        # Tìm item model
        if 'Item model number' in div.text.strip():
            divs11 = div.find_next_sibling('td', class_='a-size-base prodDetAttrValue')
            modelnumber = divs11.text.strip() if divs11 else 'Not Given'

        # Tìm weight
        if 'Item Weight' in div.text.strip():
            divs12 = div.find_next_sibling('td', class_='a-size-base prodDetAttrValue')
            weight = divs12.text.strip() if divs12 else 'Not Given'
    
    # Tìm bảng giá
    divs2a = soup.find('div', class_='a-popover-preload', id='a-popover-agShipMsgPopover')
    if divs2a:
        print("Found divs2a:")
        # Tìm table trong divs2a
        table = divs2a.find('table', class_='a-lineitem')
        if table:
            print("Found table")
            lines = table.find_all('td', class_='a-span9 a-text-left')
            for td in lines:
                if 'Price' in td.text:
                    divsprice = td.find_next_sibling('td', class_='a-span2 a-text-right')
                    price = divsprice.text.strip() if divsprice else 'None'
                if 'AmazonGlobal Shipping' in td.text:
                    divsamzship = td.find_next_sibling('td', class_='a-span2 a-text-right')
                    priceamzship = divsamzship.text.strip() if divsamzship else 'None'
                if 'Estimated Import Charges' in td.text:
                    diveic = td.find_next_sibling('td', class_='a-span2 a-text-right')
                    eic = diveic.text.strip() if diveic else 'None'
    #tìm số ngày ngày vận chuyển
    estimated_delivery_date = soup.find('span', class_='a-text-bold').text.strip()
    crawl_date = datetime.datetime.now().strftime('%A, %B %d')
    shipping_days = calculate_shipping_days(estimated_delivery_date, crawl_date)
    return shipping_days

# Gọi hàm để lấy thông tin sản phẩm
if divs2:
    print("Thực hiện cào bảng")
    shipping_days = detailproduct_table(divs2)
if divs2I:
    print("Thực hiện cào bucket")
    shipping_days = detailproduct_bucket(divs2I)

# Đóng trình duyệt
driver.quit()

import pandas as pd
import re

# Hàm để loại bỏ các ký tự không mong muốn
def clean_text(text):
    return re.sub(r'[\u200e]', '', text)

# In ra các giá trị đã thu thập và làm sạch chúng
dimension = clean_text(dimension)
asinid = clean_text(asinid)
datefirstavailable = clean_text(datefirstavailable)
manufactures = clean_text(manufactures)
country = clean_text(country)
sellerrank = clean_text(sellerrank)
color = clean_text(color)
modelnumber = clean_text(modelnumber)
weight = clean_text(weight)
price = clean_text(price)
priceamzship = clean_text(priceamzship)
eic = clean_text(eic)
shipping_days = clean_text(str(shipping_days))

print(f"Dimension: {dimension}")
print(f"ASIN: {asinid}")
print(f"Date First Available: {datefirstavailable}")
print(f"Manufacturer: {manufactures}")
print(f"Country of Origin: {country}")
print(f"{sellerrank}")
print(f"Color: {color}")
print(f"Item Model Number: {modelnumber}")
print(f"Item Weight: {weight}")
print(f"Price: {price}")
print(f"AmazonGlobal Shipping: {priceamzship}")
print(f"Estimated Import Charges: {eic}")
print(f"Day Delivered: {shipping_days}")

# Tạo dictionary với các giá trị đã thu thập
data = {
    "Dimension": [dimension],
    "ASIN": [asinid],
    "Date First Available": [datefirstavailable],
    "Manufacturer": [manufactures],
    "Country of Origin": [country],
    "Best Sellers Rank": [sellerrank],
    "Color": [color],
    "Item Model Number": [modelnumber],
    "Item Weight": [weight],
    "Price": [price],
    "AmazonGlobal Shipping": [priceamzship],
    "Estimated Import Charges": [eic],
    "Day Delivered": [shipping_days]
}

# Chuyển đổi dictionary thành DataFrame
df = pd.DataFrame(data)

# Lưu DataFrame vào file CSV
df.to_csv('product_details.csv', index=False)