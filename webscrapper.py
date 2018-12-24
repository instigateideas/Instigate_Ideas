from selenium import  webdriver
import numpy as np
import requests
import json
from itertools import cycle

# Intializing browser to scrap
chrome_path = "/home/arunachalam/Documents/chrome_driver/chromedriver"


# IP getter
def get_proxies(chromium_path):
    url_ip_website = "https://free-proxy-list.net/"
    browser = webdriver.Chrome(chromium_path)
    browser.get(url_ip_website)
    free_ip = []
    port = []
    check_time = []
    elite_or_transp = []
    # Scrapping 20 pages ip to start scrapping
    cnt = 0
    for page in list(np.arange(3, 7)):
        if cnt > 0:
            page_obj = browser.find_elements_by_xpath('//*[@id="proxylisttable_paginate"]/ul/li['+str(page)+']/a')
            page_obj[0].click()
        for i in range(1, 20):
            table_obj = browser.find_elements_by_xpath('//*[@id="proxylisttable"]/tbody/tr['+str(i)+']')
            free_ip.append(table_obj[0].text.split()[0])
            port.append(table_obj[0].text.split()[1])
            check_time.append(table_obj[0].text.split()[-1])
            elite_or_transp.append(table_obj[0].text.split()[-4])
            cnt = cnt + 1
    print('Number of Free IPs scrapped Successfully: ', cnt)
    final_dict = {'free_ip':free_ip, 'port':port, 'check_time':check_time, 'anonymity': elite_or_transp}
    browser.close()

    return final_dict

def gimme_get_proxy():
    uri_api = "https://gimmeproxy.com/api/getProxy"
    resp = requests.get(url=uri_api)
    api_resp = json.loads(resp.content)
    api_resp['status_code']

def create_browser_obj_with_ip_rotation(chromium_driver):
    chrome_options = webdriver.ChromeOptions()
    dict_proxies = get_proxies(chromium_path = chromium_driver)
    chk_url = 'https://httpbin.org/ip'
    proxy_pool = cycle(dict_proxies['free_ip'])
    cnt = 0
    for req in range(len(dict_proxies['free_ip'])):
        ip_add = next(proxy_pool)
        loc_ip = dict_proxies['free_ip'].index(ip_add)
        port_used = dict_proxies['port'][loc_ip]
        print("Request #%d" % req)
        try:
            response = requests.get(chk_url, proxies={"http": ip_add, "https": ip_add})
            print(response.json())
            break
        except:
            #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
            #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
            print("Skipping. Connnection error")
            print('--proxy-server={}:{}'.format(ip_add, port_used))
    opts = '--proxy-server={}:{}'.format(ip_add, port_used)
    print(opts)
    chrome_options.add_argument(opts)
    browser = webdriver.Chrome(executable_path= chrome_path, chrome_options=opts)

    return browser

#driver = create_browser_obj_with_ip_rotation(chrome_path= chrome_path)


# Welcome page
def intialize_amazon(chrome_path):
    driver = webdriver.Chrome(chrome_path)
    website_url = "https://www.amazon.com/"
    driver.get(url = website_url)

    return driver

# query amazon
def query_amazon_search(driver, query):
    url_query = 'https://www.amazon.com/s?k='+query+'&i=beauty-intl-ship&ref=nb_sb_noss'
    driver.get(url=url_query)

    return driver

# get product url from a page
def get_product_urls_from_a_page(driver):
    #product_list_class = "a-link-normal a-text-normal"
    num_prod_elements = driver.find_elements_by_xpath('//*[@class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"]')
    prod_url = []
    for prod_element in num_prod_elements:
        prod_url.append(prod_element.get_attribute(name="href"))
    print("Number of product in the page: ", len(prod_url))

    return prod_url

browser = create_browser_obj_with_ip_rotation(chromium_driver=chrome_path)
browser_1 = query_amazon_search(driver= browser, query='honey')
prod_urls = get_product_urls_from_a_page(driver= browser_1)



# Goto next page link for a query in amazon
get_next_page_obj = browser.find_elements_by_xpath('//*[@class="pagnLink"]/a')
# len(get_next_page_obj)
next_page_url = get_next_page_obj[0].get_attribute("href")
browser.get(next_page_url)

