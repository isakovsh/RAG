import os 
import csv
import requests
import pandas as pd 
from bs4 import BeautifulSoup 

def write_to_txt(product_info):
    
    file_exists = os.path.isfile('product_info.txt')
    with open('product_info.txt', 'a' if file_exists else 'w', encoding='utf-8') as file:
        
        if not file_exists:
            file.write("Product Information:\n\n")
        
        for product_id, info in product_info.items():
            file.write("Product ID: {}\n".format(product_id))
            file.write("Product Name: {}\n".format(info['name']))
            file.write("Product Description: {}\n".format(info['description']))
            file.write("Product Price: {}\n".format(info['price']))
            file.write("\n")

            print(f"{info['name']} sucsessfully added")
    return "Completed all products"

def csv_writer(data, file_name):
    directory = "data"
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        for item in data:
            writer.writerow([item])
    return f"Successfully saved {file_name} file"


class Crawler:
    def crwal_links(self):
        links = ["mens", "womens"]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        filtered_links = []

        for link in links:
            response = requests.get(f"https://www.selfridges.com/GB/en/cat/{link}/", headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            unfilred_links = soup.find_all("a", class_="c-header-quick-links__link o-button --bold-text-cta")
            for link_ in unfilred_links:
                filtered_links.append("https://www.selfridges.com" + link_['href'])
        return csv_writer(filtered_links,"links.csv")
    def crawl(self):
        df = pd.read_csv("data/links.csv",names=['cols'])
        all_links = df['cols'].values.tolist()
        for link in all_links:
            print(link)
            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = requests.get(link, headers=headers)
            soup = BeautifulSoup(response.text,'html.parser')
            product_info = {}
            all_products = soup.find_all("div",class_="c-prod-card__cta-box")
            for idx, card in enumerate(all_products,start=1):
                try:
                    product_name = card.find('h2', class_='c-prod-card__cta-box-product-title').text.strip()
                    product_description = card.find('span', class_='c-prod-card__cta-box-description').text.strip()
                    product_price = card.find('span', class_='c-prod-card__cta-box-price').text.strip()

                    product_info[idx] = {
                    'name': product_name,
                    'description': product_description,
                    'price': product_price
                }
                except Exception as e:
                    print(e)
            
        return write_to_txt(product_info)


            