from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Tạo chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Chạy ẩn danh
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# Khởi tạo trình duyệt WebDriver
driver = webdriver.Chrome(options=chrome_options)

url = 'https://www.amazon.com'
driver.get(url)

# Chờ cho đến khi phần tử menu xuất hiện
try:
    menu_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'hmenu-content'))
    )
    # Lấy mã HTML của trang sau khi phần tử đã xuất hiện
    html = driver.page_source
finally:
    driver.quit()

# Parse HTML với BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
soup1 = soup.find('div', id='hmenu-content')

if soup1:
    # Tìm thẻ <ul> với class và thuộc tính cụ thể
    ul_tag = soup1.find('ul', class_='hmenu hmenu-visible', attrs={'data-menu-id': '1'})
    if ul_tag:
        # Tìm thẻ <div> với class 'hmenu-item hmenu-title' và nội dung 'Shop by Department' trong ul_tag
        divscat = ul_tag.find('div', class_='hmenu-item hmenu-title', string='Shop by Department')
        if divscat:
            print("Found divscat:", divscat)
        else:
            print("Không tìm thấy thẻ <div> với class và nội dung 'Shop by Department'")
    else:
        print("Không tìm thấy thẻ <ul> với class 'hmenu hmenu-visible' và data-menu-id '1'")
else:
    print("Không tìm thấy thẻ <div> với id 'hmenu-content'")
