from bs4 import BeautifulSoup
from datetime import datetime
import os

# returns array of all messages in file in format (time, user, text)
def scrapePage(file):
	soup_page = BeautifulSoup(open(file), 'html.parser')
	thread = soup_page.find('div', attrs={'class' : 'thread'})
	metas = thread.find_all('div', attrs={'class' : 'message_header'})

	times = [strToTime(meta.find('span', attrs={'class' : 'meta'}, recursive=False).text) for meta in metas]
	users = [meta.find('span', attrs={'class' : 'user'}, recursive=False).text for meta in metas]
	texts = [text.text for text in thread.find_all('p', recursive=False)]
	return zip(times, users, texts)

# returns datetime object of str
def strToTime(str):
	return datetime.strptime(str, '%A, %B %d, %Y at %I:%M%p %Z')

# returns array of all messages in folder in format (time, user, text)
def scrapeAll(folder):
	msgs = []
	for file in os.listdir(folder):
	    if file.endswith('.html'):
	        msgs.extend(scrapePage(os.path.join(folder, file)))
	return sorted(msgs, key=lambda x: (x[0], x[1]))