from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Chrome()
descr_data = []
driver.get("https://iotvega.com/product/bs01")  # Используем второй элемент списка, так как первый - это название товара
descriptions = driver.find_elements(By.ID, "portfolio-information")

for description in descriptions:
    product_description = description.find_element(By.CLASS_NAME, "col-sm-12").get_attribute("textContent")
    descr_data.append(product_description.strip())

driver.quit()
df_descr = pd.DataFrame(descr_data, columns=["Описание"])
df_combined = pd.concat([df_descr], axis=1)
df_combined.to_excel("products_data1.xlsx", index=False)
