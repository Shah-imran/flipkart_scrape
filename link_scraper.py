import os
import time
from selenium import webdriver
import queue
from threading import Thread
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

link_q = queue.Queue()

def read_url():
	with open("url.txt", "r", encoding="utf-8") as file:
		urls = file.read()
		urls = urls.split("\n")

	return urls

def write_to_file():
	while True:   
		while not link_q.empty():
			with open("products.txt", "a", encoding="utf-8") as file:
				file.write(link_q.get()+"\n")
		
		time.sleep(1)

def check_exists_by_class_name(driver, class_name):
    try:
        driver.find_element_by_class_name(class_name)
    except NoSuchElementException:
        return False
    return True

def scrape_product_links(url):
	try: 
		global link_q    
		
		driver.get(url)

		limit = int(driver.find_element_by_xpath(
		"/html/body/div[1]/div/div[3]/div[2]/div[1]/div[2]/div[12]/div/div/span[1]").text.split(" ")[-1].replace(",",""))
		class_name = "IRpwTa" if check_exists_by_class_name(driver, "IRpwTa") else "s1Q9rs"
		count = 0
		for index in range(1,30):
			driver.get(url+"&page={}".format(index))
			for item in driver.find_elements_by_class_name(class_name):
				link_q.put(item.get_attribute('href'))
				count+=1
			print("Page - {} link Count - {}".format(index, count), end="\r")
		print("Page - {} link Count - {}".format(index, count), end="\n")
	except:
		pass




if __name__ == "__main__":
	urls = read_url()
	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome('/root/flipkart_scrape/chromedriver',chrome_options=chrome_options)
   # driver = webdriver.Chrome('/root/flipkart_scrape/chromedriver')
	
	Thread(target=write_to_file, daemon=True).start()
	
	for index, item in enumerate(urls):
		print("Url {}- {}".format(index, item), end="\n")
		scrape_product_links(item)
	
	print("Scraping finished. Closing the file now...")
	
	while not link_q.empty():
		time.sleep(1)
	
	print("File Closed")

