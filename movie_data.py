import requests
import csv
from bs4 import BeautifulSoup

url = "https://www.imdb.com/title/tt0076759/"

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
print('Movie Name:',soup.h1.string)

section = soup.find('section').find('section').contents[3]
pagesection = section.find(class_ = "ipc-page-section").contents[2]
a_tag = pagesection.contents[1].find("a", attrs={"aria-label":"View User Ratings"})
ratings = a_tag.find("span").string
print('Rating:', ratings)
lowerhalf = soup.find('section').contents[1]
castsection = lowerhalf.find("section", class_="title-cast")
director = castsection.contents[2].contents[0].a.string
writers = castsection.contents[2].contents[1].find_all("li")

print('director:', director)
for writer in writers:
    print('Writers:', writer.a.string)
#print(writers)

stars = section.find_all("ul")[2].contents[2].div.find_all("li")

for star in stars:
    print('Cast:', star.a.string)

genres = lowerhalf.find("section", attrs={"data-testid":"Storyline"}).find("li", attrs={"data-testid": "storyline-genres"}).find_all("li")

for genre in genres:
    print('Genres:',genre.a.string)

ReleaseMonth = lowerhalf.find("section", attrs={"data-testid":"Details"}).li.li.a.string.split(" ", 1)[0]
print('ReleaseMonth:', ReleaseMonth)
languages = lowerhalf.find("section", attrs={"data-testid":"Details"}).find("li", attrs={"data-testid":"title-details-languages"}).find_all("li")
moneymatters = budget = lowerhalf.find("section", attrs={"data-testid":"BoxOffice"})
budget = moneymatters.li.li.span.string.split(" ", 1)[0]
print('Budget:',budget)
for language in languages:
    print('Languages:', language.a.string)

boxofficeUS = int(moneymatters.ul.contents[1].li.span.string[1:].replace(',',''))
boxofficeWorld = int(moneymatters.ul.contents[3].li.span.string[1:].replace(',',''))
print('BoxOffice:$',boxofficeUS + boxofficeWorld)


header = ['Name', 'Rating', 'Director', 'Writers', 'Cast', 'Genres', 'ReleaseMonth', 'Budget', 'Language', 'boxoffice']
Data = [soup.h1.string, ratings, director, writers[0].a.string, stars[0].a.string, genres[0].a.string, ReleaseMonth, budget, languages[0].a.string, boxofficeUS + boxofficeWorld]
with open('movies.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    writer.writerow(header)

    writer.writerow(Data)