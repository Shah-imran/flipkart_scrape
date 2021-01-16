import os
import time
from selenium import webdriver
import json
from threading import Thread
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

visited_links = []
product_list = list()
field_names = ("current_category", "filters", "product_links")

links_filepath = "input.txt"
output_filepath = "output"

sub_categories_class_name = "_2SqgSY"
total_categories_class_name = "_2aDURW"
category_in_focus_class_name = "_1jJQdf"

def read_url():
    with open(links_filepath, "r", encoding="utf-8") as file:
        urls = file.read()
        urls = urls.split("\n")

    return urls

def check_exists_by_class_name(driver, class_name):
    try:
        driver.find_element_by_class_name(class_name)
    except NoSuchElementException:
        return False
    return True

def re_scrape(driver, root):
    
    global tab_in_focus, product_list, visited_links
    
    if driver.current_url not in visited_links or root==True:
        visited_links.append(driver.current_url)
        try:
            if "more" in driver.find_elements_by_class_name(sub_categories_class_name)[-1].text:
                driver.find_elements_by_class_name(sub_categories_class_name)[-1].click()
        except:
            pass

        total_categories = []
        sub_categories = []
        sub_categories_links = []
        category_in_focus = ""

        try:
            total_categories = driver.find_element_by_class_name(total_categories_class_name).text.replace("CATEGORIES","").strip().split("\n")
            sub_categories = [ item.text for item in driver.find_elements_by_class_name(sub_categories_class_name) ]
            sub_categories_links = [ item.get_attribute('href') for item in driver.find_elements_by_class_name(sub_categories_class_name) ]
            category_in_focus = driver.find_element_by_class_name(category_in_focus_class_name).text
        except:
            pass
#         print(category_in_focus, driver.current_url)
        if len(sub_categories) > 0:
            for s_cat, link in zip(sub_categories, sub_categories_links):
                if s_cat != "Show less":
                    tab_in_focus+=1
                    # Open a new window
                    driver.execute_script("window.open('');")
                    # Switch to the new window
                    driver.switch_to.window(driver.window_handles[tab_in_focus])
    #                 print(tab_in_focus*" ", tab_in_focus, s_cat, "->", link)
                    driver.get(link)
                    re_scrape(driver, 0)

        current_category = ""
        filters = []
        product_links = []

        try:
            current_category = "->".join(total_categories[:total_categories.index(category_in_focus)+1])
        except:
            pass

        try:
            for item in driver.find_elements_by_class_name("ttx38n"):
                if item.get_attribute("class") == "ttx38n":
                    item.click()
        except:
            pass

        try:
            for item in driver.find_elements_by_class_name("QvtND5")[::-1]:
                if "MORE" in item.text:
                    driver.execute_script("arguments[0].click();", item)
        except:
            pass

        try:
            filters = [ filter_item.text.split("\n") for filter_item in driver.find_elements_by_class_name("_2hbLCH")[1:] ]
        except:
            pass

        try:
            product_class_name = "IRpwTa" if check_exists_by_class_name(driver, "IRpwTa") else "s1Q9rs"
            product_links = [ item.get_attribute('href') for item in driver.find_elements_by_class_name(product_class_name) ]
        except:
            pass

        dict_t =  {
            "current_category": current_category,
            "filters": filters,
            "product_links": product_links
        }

        product_list.append(dict_t.copy())
    
    if tab_in_focus != 0:
        driver.close()
        tab_in_focus-=1
        driver.switch_to.window(driver.window_handles[tab_in_focus])
    
    return True

if __name__ == "__main__":
    links_filepath = input("Enter links filepath : ")
    output_filepath = input("Enter output folder : ")
    
    if not os.path.exists(output_filepath):
        os.mkdir(output_filepath)
    
    urls = read_url()

    ChromeOptions = webdriver.ChromeOptions()
    ChromeOptions.add_argument('--disable-browser-side-navigation')
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(30)
    
    for index, url in enumerate(urls):
        try:
            print("Progress - {}/{}".format(index+1,len(urls)), end="\r")
            tab_in_focus = 0
            product_list = []
            visited_links = []
            visited_links.append(url)
            driver.get(url)
            re_scrape(driver, 1)
            with open("{}/{}.json".format(output_filepath, index), 'w') as fout:
                json.dump(product_list, fout, indent=4)
        except Exception as e:
            print(e)
    driver.quit()
    print("Finished")
            