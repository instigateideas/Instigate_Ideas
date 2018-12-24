from selenium import webdriver

chrome_path = "/home/arunachalam/Documents/chrome_driver/chromedriver"
browser = webdriver.Chrome(chrome_path)
whats_app_web_url = "https://web.whatsapp.com/"
contact_search = "Praveen"

browser.get(url = whats_app_web_url)
print('Opening browser.. Please scan the QR Code')

search_box = browser.find_element_by_xpath('.//*[@class="jN-F5 copyable-text selectable-text"]')
search_box.send_keys(contact_search)

contact_list = browser.find_element_by_xpath('.//*[@class="RLfQR"]').text.split('\n')
if contact_search in contact_list:
    print('The contact is available to send message..')

click_name = browser.find_element_by_xpath('//*[@class="_2wP_Y"]')
click_name.click()

type_content = "Today Shopping..."
InputElement = browser.find_element_by_xpath('.//*[@class ="_3F6QL _2WovP"]')
InputElement.click()
text_enter =browser.find_element_by_xpath('.//*[@class="_2S1VP copyable-text selectable-text"]')
text_enter.send_keys(type_content)
send_element = browser.find_element_by_xpath('.//*[@class="_35EW6"]')
send_element.click()
