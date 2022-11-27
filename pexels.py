import os
import header
import time
import requests
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pathlib import Path

header.header()

path = str(Path(__file__).parent)+'/downloaded_images/'
os.makedirs(path, exist_ok = True)

query = input('Enter Query: ')
query = query.replace(' ', '%20')
page_links = []
images_list = []
index_number = 0
images_download_links_list = []
pages = 1

for page_number in range(pages):
	option = Options()
	option.headless = True
	user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'
	option.add_argument('user-agent={user_agent}')
	browser = webdriver.Chrome(options = option)
	browser.set_window_size(200,200)
	browser.get('https://www.pexels.com/search/' + query +'/?page='+str(page_number))
	print('Scraping URLs in page {} from a total of {} pages.'.format(str(page_number+1), str(pages)))
	links = browser.find_elements(By.XPATH,'//*[@href]')
	for link in links:
		images_list.append(link.get_attribute('href'))
	time.sleep(0.6)
	browser.close()

images_list = list(dict.fromkeys(images_list))
	
def download_all_images(path, number, image_list, index):
	download_request = requests.get(image_list[index]).content
	with open(path + 'image' + str(number) + '.jpg', 'wb') as downloads:
		downloads.write(download_request)
	downloads.close()

with open('image_list', 'a') as images:
	for image in images_list:
		if 'jpg' in str(image) or 'jpeg' in str(image):
			images.write(image+'\n')
		else:
			pass
images.close()


with open ('image_list', 'r') as download_links:	
	for link in download_links.readlines():			
		images_download_links_list.append(link.split('?')[0])
			
download_links.close()

with concurrent.futures.ThreadPoolExecutor(100) as executor:
	for item in range(len(images_download_links_list)):
		executor.submit(download_all_images, path, str(index_number), images_download_links_list, item)
		index_number +=1
		

