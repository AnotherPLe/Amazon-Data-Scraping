import pandas as pd
import mysql.connector

# Đọc dữ liệu từ các file CSV mới được lưu
category_data = pd.read_csv("D:\\LNTP ở HUST\\Học tập\\Năm 3\\20232\\Đồ án 1\\Data-Crawling-Of-Amazon-main\\Data-Crawling-Of-Amazon-main\\DataSource\\DataAfterETL\\Caterogy.csv")
product_data = pd.read_csv("D:\\LNTP ở HUST\\Học tập\\Năm 3\\20232\\Đồ án 1\\Data-Crawling-Of-Amazon-main\\Data-Crawling-Of-Amazon-main\\DataSource\\DataAfterETL\\Product.csv")
customer_ranking_data = pd.read_csv("D:\\LNTP ở HUST\\Học tập\\Năm 3\\20232\\Đồ án 1\\Data-Crawling-Of-Amazon-main\\Data-Crawling-Of-Amazon-main\\DataSource\\DataAfterETL\\CustomerRatings.csv")
seller_ranking_data = pd.read_csv("D:\\LNTP ở HUST\\Học tập\\Năm 3\\20232\\Đồ án 1\\Data-Crawling-Of-Amazon-main\\Data-Crawling-Of-Amazon-main\\DataSource\\DataAfterETL\\SellerRankings.csv")

# Loại bỏ các dòng có giá trị null cho cột 'ASIN'
category_data.dropna(subset=['ASIN'], inplace=True)
product_data.dropna(subset=['ASIN'], inplace=True)
customer_ranking_data.dropna(subset=['ASIN'], inplace=True)
seller_ranking_data.dropna(subset=['ASIN'], inplace=True)

# Kết nối đến MySQL
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="phuocle11001203",
    database="da1_OLTP"
)
cursor = db_connection.cursor()

# Tạo các bảng nếu chưa tồn tại
create_tables_queries = [
    """
    CREATE TABLE IF NOT EXISTS Products (
        ASIN VARCHAR(20) PRIMARY KEY NOT NULL,
        ProductName VARCHAR(255),
        Link VARCHAR(3000),
        Price DEMICAL (10,3),
        PriceGroup NVARCHAR(50),
        Link NVARCHAR(1600),
        DateFirstAvailable DATE,
        Manufacturer NVARCHAR(50),
        CountryOfOrigin NVARCHAR(50),
        Continent NVARCHAR(50),
        ItemWeight DEMICAL (10,3),
        PriceDetail DEMICAL (10,3),
        AmazonGlobalShipping DEMICAL (10,3),
        EstimatedImportCharges DEMICAL (10,3),
        DayDelivered INT,

    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Category (
        CategoryID INT AUTO_INCREMENT PRIMARY KEY,
        ASIN VARCHAR(20) NOT NULL,
        MainCategory VARCHAR(255),
        SubCategory VARCHAR(255),
        FOREIGN KEY (ASIN) REFERENCES Products(ASIN)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS CustomerRatings (
        ASIN VARCHAR(20) PRIMARY KEY NOT NULL,
        CustomerRating DECIMAL(2, 1),
        CustomerReview INT,
        FOREIGN KEY (ASIN) REFERENCES Products(ASIN)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS SellerRankings (
        ASIN VARCHAR(20) PRIMARY KEY NOT NULL,
        MainRankingValue VARCHAR(250),
        MainRankingCategory VARCHAR(255),
        SubRankingValue VARCHAR(250),
        SubRankingCategory VARCHAR(255),
        FOREIGN KEY (ASIN) REFERENCES Products(ASIN)
    );
    """,
]

import pandas as pd
import mysql.connector

# Đọc dữ liệu từ các file CSV mới được lưu
category_data = pd.read_csv("D:\\LNTP ở HUST\\Học tập\\Năm 3\\20232\\Đồ án 1\\Data-Crawling-Of-Amazon-main\\Data-Crawling-Of-Amazon-main\\DataSource\\DataAfterETL\\Caterogy.csv")
product_data = pd.read_csv("D:\\LNTP ở HUST\\Học tập\\Năm 3\\20232\\Đồ án 1\\Data-Crawling-Of-Amazon-main\\Data-Crawling-Of-Amazon-main\\DataSource\\DataAfterETL\\Product.csv")
customer_ranking_data = pd.read_csv("D:\\LNTP ở HUST\\Học tập\\Năm 3\\20232\\Đồ án 1\\Data-Crawling-Of-Amazon-main\\Data-Crawling-Of-Amazon-main\\DataSource\\DataAfterETL\\CustomerRatings.csv")
seller_ranking_data = pd.read_csv("D:\\LNTP ở HUST\\Học tập\\Năm 3\\20232\\Đồ án 1\\Data-Crawling-Of-Amazon-main\\Data-Crawling-Of-Amazon-main\\DataSource\\DataAfterETL\\SellerRankings.csv")

# Loại bỏ các dòng có giá trị null cho cột 'ASIN'
category_data.dropna(subset=['ASIN'], inplace=True)
product_data.dropna(subset=['ASIN'], inplace=True)
customer_ranking_data.dropna(subset=['ASIN'], inplace=True)
seller_ranking_data.dropna(subset=['ASIN'], inplace=True)

# Kết nối đến MySQL
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="phuocle11001203",
    database="DA1_OLTP"
)
cursor = db_connection.cursor()

# Tạo các bảng nếu chưa tồn tại
create_tables_queries = [
    """
    CREATE TABLE IF NOT EXISTS Products (
        ASIN VARCHAR(20) PRIMARY KEY NOT NULL,
        ProductName VARCHAR(255),
        Link VARCHAR(3000),
        PriceGroup NVARCHAR(50),
        DateFirstAvailable DATE,
        Manufacturer NVARCHAR(50),
        CountryOfOrigin NVARCHAR(50),
        Continent NVARCHAR(50),
        ItemWeight DECIMAL(10,3),
        ProductSizeTier NVARCHAR(50),
        PriceDetail DECIMAL(10,3),
        AmazonGlobalShipping DECIMAL(10,3),
        EstimatedImportCharges DECIMAL(10,3),
        DayDelivered INT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Category (
        CategoryID INT AUTO_INCREMENT PRIMARY KEY,
        ASIN VARCHAR(20) NOT NULL,
        MainCategory VARCHAR(255),
        SubCategory VARCHAR(255),
        FOREIGN KEY (ASIN) REFERENCES Products(ASIN)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS CustomerRatings (
        ASIN VARCHAR(20) PRIMARY KEY NOT NULL,
        CustomerRating DECIMAL(2, 1),
        CustomerReview INT,
        FOREIGN KEY (ASIN) REFERENCES Products(ASIN)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS SellerRankings (
        ASIN VARCHAR(20) PRIMARY KEY NOT NULL,
        MainRankingValue VARCHAR(250),
        MainRankingCategory VARCHAR(255),
        SubRankingValue VARCHAR(250),
        SubRankingCategory VARCHAR(255),
        FOREIGN KEY (ASIN) REFERENCES Products(ASIN)
    );
    """,
]

for query in create_tables_queries:
    cursor.execute(query)

# Chuyển đổi dữ liệu từ DataFrame sang danh sách các hàng
category_records = category_data[['ASIN', 'MainCategory', 'SubCategory']].values.tolist()
product_records = product_data[['ASIN', 'ProductName', 'Link', 'PriceGroup', 'DateFirstAvailable', 'Manufacturer', 'CountryOfOrigin', 'Continent', 'ItemWeight','ProductSizeTier', 'PriceDetail', 'AmazonGlobalShipping', 'EstimatedImportCharges', 'DayDelivered']].values.tolist()
customer_ranking_records = customer_ranking_data[['ASIN', 'CustomerRating', 'CustomerReview']].values.tolist()
seller_ranking_records = seller_ranking_data[['ASIN', 'MainRankingValue', 'MainRankingCategory', 'SubRankingValue', 'SubRankingCategory']].values.tolist()

# Chèn dữ liệu vào bảng tương ứng, sử dụng ON DUPLICATE KEY UPDATE để xử lý các bản ghi trùng lặp
insert_product_query = """
INSERT INTO Products (ASIN, ProductName, Link, PriceGroup, DateFirstAvailable, Manufacturer, CountryOfOrigin, Continent, ItemWeight,ProductSizeTier, PriceDetail, AmazonGlobalShipping, EstimatedImportCharges, DayDelivered)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    ProductName = VALUES(ProductName),
    Link = VALUES(Link),
    PriceGroup = VALUES(PriceGroup),
    DateFirstAvailable = VALUES(DateFirstAvailable),
    Manufacturer = VALUES(Manufacturer),
    CountryOfOrigin = VALUES(CountryOfOrigin),
    Continent = VALUES(Continent),
    ItemWeight = VALUES(ItemWeight),
    ProductSizeTier = VALUES(ProductSizeTier),
    PriceDetail = VALUES(PriceDetail),
    AmazonGlobalShipping = VALUES(AmazonGlobalShipping),
    EstimatedImportCharges = VALUES(EstimatedImportCharges),
    DayDelivered = VALUES(DayDelivered)
"""
cursor.executemany(insert_product_query, product_records)

insert_category_query = """
INSERT INTO Category (ASIN, MainCategory, SubCategory)
VALUES (%s, %s, %s)
ON DUPLICATE KEY UPDATE
    MainCategory = VALUES(MainCategory),
    SubCategory = VALUES(SubCategory)
"""
cursor.executemany(insert_category_query, category_records)

insert_customer_ranking_query = """
INSERT INTO CustomerRatings (ASIN, CustomerRating, CustomerReview)
VALUES (%s, %s, %s)
ON DUPLICATE KEY UPDATE
    CustomerRating = VALUES(CustomerRating),
    CustomerReview = VALUES(CustomerReview)
"""
cursor.executemany(insert_customer_ranking_query, customer_ranking_records)

insert_seller_ranking_query = """
INSERT INTO SellerRankings (ASIN, MainRankingValue, MainRankingCategory, SubRankingValue, SubRankingCategory)
VALUES (%s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    MainRankingValue = VALUES(MainRankingValue),
    MainRankingCategory = VALUES(MainRankingCategory),
    SubRankingValue = VALUES(SubRankingValue),
    SubRankingCategory = VALUES(SubRankingCategory)
"""
cursor.executemany(insert_seller_ranking_query, seller_ranking_records)

# Commit và đóng kết nối
db_connection.commit()
db_connection.close()

print("Data has been successfully inserted into the database.")
