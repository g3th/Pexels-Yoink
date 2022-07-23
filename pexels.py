import os
import requests
import concurrent.futures
from selenium import webdriver
from pathlib import Path

path = str(Path(__file__).parent)+'/downloaded_images/'
os.makedirs(path, exist_ok = True)

query = input('Enter Query: ')
images_list = []
number = 0
images_download_links_list = []

browser = webdriver.Chrome()
browser.set_window_size(200,300)
browser.get('https://www.pexels.com/search/' + query)
links = browser.find_elements_by_xpath('//*[@href]')

def download_all_images(path, number, image_list, index):
	download_request = requests.get(image_list[index]).content
	with open(path + 'image' + str(number) + '.jpg', 'wb') as downloads:
		downloads.write(download_request)
	downloads.close()

for link in links:
	images_list.append(link.get_attribute('href'))
browser.close()

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
		print(executor.submit(download_all_images, path, str(number), images_download_links_list, item))
		number +=1
		

