import json
import requests
from flask import jsonify
from bs4 import BeautifulSoup


class Data:
    def __init__(self, username):
        self.__username = username

    def codeforces(self):
        # getting codeforces user details from api
        url = 'https://codeforces.com/api/user.info?handles=' + self.__username
        responses = requests.get(url)
        contests = []
        # details of user from codeforces api (json)
        details_api = responses.json()
        details_api = details_api['result'][0]
        rating = details_api['rating']
        maxRating = details_api['maxRating']
        avatar = details_api['avatar']
        rank = details_api['rank']
        maxRank = details_api['maxRank']

        # getting cf contest details of user from Web-Scrapping (html)
        url2 = 'https://codeforces.com/contests/with/' + self.__username
        r = requests.get(url2)
        htmlContent = r.content
        soup = BeautifulSoup(htmlContent, 'html.parser')
        table = soup.find('table', attrs={'class': 'user-contests-table'})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            contests.append(int(cols[6]))

        result = {
            'status': 'Success',
            'username': self.__username,
            'platform': 'codeforces',
            'rating': rating,
            'max rating': maxRating,
            'avatar': avatar,
            'rank': rank,
            'max rank': maxRank,
            'contest': contests
        }
        return jsonify(result)

    def codechef(self):
        url = 'https://codechef.com/users/' + self.__username
        responses = requests.get(url)
        soup = BeautifulSoup(responses.text, 'html.parser')
        # rating
        rating = soup.find('div', class_='rating-number').text
        # stars
        star = soup.find('span', class_='rating').text
        # highest rating
        highest_rating_class = soup.find('div', class_='rating-header')
        highest_rating = highest_rating_class.find_next('small').text.split()[-1].rstrip(')')
        # Division
        divRating = soup.find('div', class_='rating-header').find('div', attrs={'class': None}).text.strip('()')
        # Rank
        rank = soup.find('div', class_='rating-ranks').find_all('a')
        global_rank = rank[0].text
        country_rank = rank[1].text
        if global_rank != 'NA':
            global_rank = int(global_rank)
            country_rank = int(country_rank)
        # contest ratings
        first = responses.text.find('[', responses.text.find('all_rating'))
        last = responses.text.find(']', first) + 1
        next_bracket = responses.text.find('[', first + 1)
        while next_bracket < last:
            last = responses.text.find(']', last + 1) + 1
            next_bracket = responses.text.find('[', next_bracket + 1)
        all_rating = json.loads(responses.text[first: last])
        ratings = []
        for article in all_rating:
            ratings.append(int(article['rating']))
        # No. of problem solved
        problem_solved = soup.find('section', class_='rating-data-section problems-solved').find('h5').text
        s1 = slice(14, 16)
        problems = int(problem_solved[s1])   # Total number of problems solved
        # profile
        avatar = soup.find('div', class_='user-details-container').find('img')
        links = avatar['src']
        result = {
            "status": "Success",
            "platform": "codechef",
            "username": self.__username,
            "stars": star,
            "div": divRating,
            "rating": rating,
            "max rating": highest_rating,
            "global rank": global_rank,
            "country rank": country_rank,
            "avatar": links,
            "problem solved": problems,
            "contests": ratings
        }
        return jsonify(result)

    def get_details(self, platform):
        if platform == 'codechef':
            return self.codechef()
        if platform == 'codeforces':
            return self.codeforces()
