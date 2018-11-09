import requests

res = requests.get("https://www.goodreads.com/book/review_counts.json",params={"key":"H5fw2gTtqbX7RnMMpDuO4w","isbns": "9781632168146"})
print(res.json())