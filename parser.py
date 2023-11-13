import requests
from bs4 import BeautifulSoup
import pygsheets

url = "https://www.trustpilot.com/review/www.google.com"
result = requests.get(url)
soup = BeautifulSoup(result.content)

review_score = soup.find('span', class_='typography_heading-m__T_L_X').text.strip()
# Extract the percentage of reviews for each star rating
star_ratings = soup.find_all('label', class_='styles_row__wvn4i')

total_reviews = soup.find('p', {'data-reviews-count-typography': True}).text.strip().split()[0]

percentage_per_star = []
for rating in star_ratings:
    star = rating.find('p', {'data-rating-label-typography': 'true'}).text.strip()
    percentage = rating.find('p', {'data-rating-distribution-row-percentage-typography': 'true'}).text.strip()[:-1]
    percentage_per_star.append(percentage)

gc = pygsheets.authorize(service_file='pacific-attic-387411-749e0dc3abf7.json')
sh = gc.open('pr_pillar_test')
wk1 = sh['google']
wk1.append_table(
    [
        int(total_reviews.replace(',', '')),
        review_score,
        percentage_per_star[0],
        percentage_per_star[1],
        percentage_per_star[2],
        percentage_per_star[3],
        percentage_per_star[4]
    ],
    overwrite=False
)
