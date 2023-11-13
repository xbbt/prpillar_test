import requests
from bs4 import BeautifulSoup
import pandas as pd
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
wk1 = sh[0]
wk1.set_dataframe(
    pd.DataFrame(
        {
            'review_count': [int(total_reviews.replace(',', ''))],
            'total_score': [review_score],
            'one_star_percent': percentage_per_star[0],
            'two_star_percent': percentage_per_star[1],
            'three_star_percent': percentage_per_star[2],
            'four_star_percent': percentage_per_star[3],
            'five_star_percent': percentage_per_star[4],
        }
    ),
    (1, 1),
    copy_index=False,
    copy_head=True,
    extend=True,
    fit=False,
    escape_formulae=False
)
