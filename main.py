from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Chrome()
driver.get("https://iotvega.com/product")

products_data = []
prices_data = []
descr_data = []
products = driver.find_elements(By.CLASS_NAME, "one-item")
for product in products:
    product_name = product.get_attribute("textContent")
    product_link = product.get_attribute("href")
    product_image = product.find_element(By.TAG_NAME, "img").get_attribute("src")
    product_features = product.find_element(By.CLASS_NAME, "features").get_attribute("textContent")
    products_data.append([product_name, product_link, product_image, product_features])

prices = driver.find_elements(By.CLASS_NAME, "price_item")
for price in prices:
    product_price = price.get_attribute("textContent")
    prices_data.append(product_price)

# Закрываем текущий браузер и открываем новый для каждой ссылки
driver.quit()

for product_link in products_data:
    driver = webdriver.Chrome()
    driver.get(product_link[1])  # Используем второй элемент списка, так как первый - это название товара
    descriptions = driver.find_elements(By.ID, "portfolio-information")
    for description in descriptions:
        product_description = description.find_element(By.CLASS_NAME, "col-sm-12").get_attribute("textContent")
        descr_data.append(product_description.strip())
    driver.quit()  # Закрываем браузер после извлечения описания

df_general = pd.DataFrame(products_data, columns=["Название", "Ссылка", "Изображение", "Характеристики"])
df_prices = pd.DataFrame(prices_data, columns=["Цена"])
df_descr = pd.DataFrame(descr_data, columns=["Описание"])
df_combined = pd.concat([df_general, df_prices, df_descr], axis=1)
df_combined.to_excel("products_data.xlsx", index=False)