import requests
from bs4 import BeautifulSoup
import re
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
    'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}

url = r"https://www.istockphoto.com/pl/search/2/image?istockcollection=main%2Cvalue&phrase=lego%20tennis"
#url = 'https://www.gettyimages.com/photos/lego-car?assettype=image'

#Words used to scrape lego images:
#household, person, building, town, superhero, hero, book, university, money, toy, buildings, home, complex, various, set, spacecraft,
#world, computer, waterfall, water, ship, soft toy, bear, beer, sweet, country, ilustration, website, paris, poland, robot, AI,
#ice, iceskating, skiing, ski, pen, pendrive, sheet, sheat, clothes, architecture, metropolis, room, bedroom, toilet,
#box, bridge, fan, fun, sport, headphones, souvenir, berlin, california, denmark, castle, pants, shirt, barcelona, hotel,
#train, railway, scotland, music, emotion, particle, bed, food, garden, lake, sea, tennis, board, phone, 

result = requests.get(url, headers=headers)
soup = BeautifulSoup(result.text, "html.parser")

path = r"./Scraped_images"
images = []
i = 0

for item in soup.find_all("img"):
    try:
        img_data = requests.get(item['src']).content
        try:
            with open(f'{path}/{i}_new.jpg', 'wb') as handler:
                handler.write(img_data)
                i += 1
        except Exception:
            print(f"Something went wrong during the file creation.")
    except requests.exceptions.MissingSchema:
        print(f"Could not write from URL: {item['src']}")
