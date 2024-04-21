import json
import re
import html
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
from flask import jsonify

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.82 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}


class Data:

    def filter_data(self, upcoming_list, future_list, data_list):
        current_date = datetime.now().date()
        for data in data_list:
            start_date = parse(data['start_date']).date()

            if start_date == current_date:
                upcoming_list.append(data)
            elif start_date > current_date:
                future_list.append(data)

    def get_data(self, contest_result, contest_list, pattern, allowed_sources):
        for contest in contest_list:
            data = contest.findNext('a', class_='data-ace')
            if data['data-ace']:
                try:
                    expression = re.sub(pattern, r'"title":"\1 : \"\2\""', data['data-ace'])
                    event = json.loads(expression)

                    if event['location'].split('.')[0] in allowed_sources:
                        start_date_object = datetime.strptime(event['time']['start'], "%B %d, %Y %H:%M:%S")
                        start_date = start_date_object.strftime("%B %d, %Y")
                        start_time = start_date_object.strftime("%H:%M:%S")
                        end_date_object = datetime.strptime(event['time']['end'], "%B %d, %Y %H:%M:%S")
                        end_date = end_date_object.strftime("%B %d, %Y")
                        end_time = end_date_object.strftime("%H:%M:%S")

                        contest_platform = event['location'].split('.')[0]
                        contest_url = event['desc'].split('url: ')[1]
                        contest_name = event['title']
                        contest_duration = contest.findNext('div', class_='duration').text
                        contest_start_time = start_time
                        contest_start_date = start_date
                        contest_end_time = end_time
                        contest_end_date = end_date
                        contest_time_zone = event['time']['zone']

                        result = {
                            'platform': contest_platform,
                            'title': contest_name,
                            'url': contest_url,
                            'start_date': contest_start_date,
                            'start_time': contest_start_time,
                            'duration': contest_duration,
                            'end_date': contest_end_date,
                            'end_time': contest_end_time,
                            'time_zone': contest_time_zone
                        }
                        contest_result.append(result)
                except: continue

    def get_contest(self):
        url = 'https://clist.by/?view=list&favorite=off'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        pattern = r'"title":"([^"]*) : "([^"]*)""'

        active_contest = soup.select('.contest.running')
        future_contest = soup.select('.contest.coming')
        allowed_sources = ['codechef', 'codeforces', 'leetcode', 'hackerearth', 'actoder', 'hackerrank']

        ahead = []
        active = []
        upcoming = []
        future = []

        self.get_data(active, active_contest, pattern, allowed_sources)
        self.get_data(ahead, future_contest, pattern, allowed_sources)
        self.filter_data(upcoming, future, ahead)

        result = {
            "active": active,
            "upcoming": upcoming,
            "future": future
        }

        return jsonify(result)