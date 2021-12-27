import requests
import pandas as pd


def RFC3339_datetime(year, month, day, hour=None, minute=None, second=None):
    if hour == None:
        hour = 0

    if minute == None:
        minute = 0

    if second == None:
        second = 0

    return f"{year}-{month}-{day}T{hour}:{minute}:{second}+00:00"


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def tweets_search(keywords, start_time, end_time):
    # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
    # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
    query_params = {'query': '',
                    'tweet.fields': 'author_id',
                    'start_time': start_time,
                    'end_time': end_time}
    'from #TSLA OR elon musk'
    keywords = keywords.split(',')
    query_params['query'] += " OR ".join(keywords)

    search_url_tweets_search = "https://api.twitter.com/2/tweets/search/recent"
    json_response = connect_to_endpoint(search_url_tweets_search, query_params)
    return pd.concat([pd.DataFrame(t, index=[0]) for t in json_response['data']])