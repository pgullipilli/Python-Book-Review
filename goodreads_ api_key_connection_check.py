import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

secret_key = config['GOODREADS']['API_KEY']

res = requests.get("https://www.goodreads.com/book/review_counts.json",params={"key":secret_key,"isbns": "9781632168146"})
print(res.json())