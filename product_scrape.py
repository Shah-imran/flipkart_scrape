import os
import time
import csv
from selenium import webdriver
import queue
from threading import Thread
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

link_q = queue.Queue()
field_names = ("category", "title", "highlights", "size_chart", "size", 
            "description", "specifications", "price", "product_details", "image", "product_links")


        
def check_exists_by_class_name(driver, class_name):
    try:
        driver.find_element_by_class_name(class_name)
    except NoSuchElementException:
        return False
    return True

def read_url():
    with open("products.txt", "r", encoding="utf-8") as file:
        urls = file.read()
        urls = urls.split("\n")

    return urls

def write_to_file():
    if not os.path.exists("result.csv"):
        with open("result.csv", 'a', newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames = field_names)
            writer.writeheader()
            print("File created")
    while True:   
        while not link_q.empty():
            with open("result.csv", 'a', newline='', encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames = field_names)
                writer.writerow(link_q.get())
        
        time.sleep(1)

def scrape(start, urls):
    global link_q
    len_urls = len(urls)
    last_index_worked = 0
    print("Total Links : {}".format(len_urls), end="\n")
    for index in range(start, len_urls):
        try:
            driver.get(urls[index])
            category = ""
            title = "" 
            highlights = "" 
            description = ""
            specifications = "" 
            image = ""
            product_details = ""
            size = ""
            size_chart = ""
            price = ""
            try:
                category = driver.find_elements_by_class_name("_2whKao")[1].text
            except:
                pass

            try:
                title = driver.find_element_by_class_name("yhB1nd").text
            except:
                pass

            try:
                highlights = driver.find_element_by_class_name("_2418kt").text.replace("\n", ",")
            except:
                pass

            try:
                description = driver.find_element_by_class_name("_2o-xpa").text
            except:
                pass

            try:
                specifications = driver.find_element_by_class_name("_1UhVsV").text
            except:
                pass

            try:
                price = driver.find_element_by_class_name("_30jeq3").text
            except:
                pass

            try:
                product_details = driver.find_element_by_class_name("_1v8OXw").text
            except:
                pass

            try:
                if check_exists_by_class_name(driver, "_396QI4"):
                    image = driver.find_element_by_class_name("_396QI4").get_attribute("src")
                else:
                    image = driver.find_element_by_class_name("_396cs4").get_attribute("src")
            except:
                pass

            try:
                temp = []
                for item in driver.find_elements_by_class_name("_22QfJJ"):
                    if "Size" in item.text:
                        for item2 in item.find_elements_by_class_name("_3V2wfe"):
                            temp.append(item2.text)
                        size = ",".join(temp)
            except:
                pass

            try:
                driver.find_element_by_class_name("_1qs4Jt").click()
                size_chart = driver.find_element_by_class_name("_2WObml").text.replace("\n", ",")
            except:
                pass


            dict_t = {
                        "category": category,
                        "title": title,
                        "highlights": highlights,
                        "size_chart": size_chart,
                        "size": size,
                        "description": description,
                        "specifications": specifications,
                        "price": price,
                        "product_details": product_details,
                        "image": image,
                        "product_links": urls[index]
                    }
            link_q.put(dict_t.copy())
            last_index_worked = index
            print("Current - {} Remaining - {}      ".format(index+1, len_urls - index+1), end="\r")
        except Exception as e:
            print("Last worked at {} Error at {} : {}   ".format(last_index_worked, index, e), end="\r")

if __name__ == "__main__":
    urls = read_url()
    start = int(input("Enter Starting Index: "))
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome('/root/flipkart_scrape/chromedriver',chrome_options=chrome_options)
    # driver = webdriver.Chrome(chrome_options=chrome_options)
    
    Thread(target=write_to_file, daemon=True).start()
    
    scrape(start, urls)
    
    print("Scraping finished. Closing the file now...")
    
    while not link_q.empty():
        time.sleep(1)
    
    print("File Closed")
