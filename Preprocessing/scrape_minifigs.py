import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", required=True, help = "path to directory where to save images")
args = parser.parse_args()

pages = range(1,11)
categories = ["Collectible-Minifigures", "LEGO-Brand", "Harry-Potter", "Holiday-Event"]

imgs = []

for cat in categories:
  print(cat)
  for page in pages:
      url = f'https://brickset.com/minifigs/category-{cat}/page-{page}'
      response = requests.get(url)
      soup = BeautifulSoup(response.content, "html.parser")
      articles_tags = soup.find_all("article")

      for article in articles_tags:
        if any(category in article.text for category in ["Duplo", "Elves", "Basic", "Bionicle", "Cars", "DC Super Hero Girls", "Fabuland", "Dimensions"]):
            continue
        img_link = article.find('a')['href']
        if img_link.startswith('https'):
          imgs.append(img_link)

for i, img_link in enumerate(imgs):
    response = requests.get(img_link)
    with open(f"{args.path}/{i}.jpg", "wb") as file:
        file.write(response.content)