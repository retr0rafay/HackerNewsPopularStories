import requests  # used for getting HTML files...allows us to download the html first
from bs4 import BeautifulSoup  # allows us to use HTML and grab the data
import pprint  # prints everything out in a nice format


def get_response_list():
    page_num = 1
    response = requests.get('https://news.ycombinator.com/news')
    response_list = [response]
    while True:
        soup = BeautifulSoup(response.text, 'html.parser')
        next_page = soup.select('.morelink')
        if next_page:
            response = requests.get(f'https://news.ycombinator.com/news?p={page_num + 1}')
            response_list.append(response)
            page_num += 1
        else:
            break
    return response_list


def get_links(responses):
    story_links = []
    for response in responses:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.select('.storylink')
        story_links.extend(links)
    return story_links


def get_subtexts(responses):
    subtext_links = []
    for response in responses:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.select('.subtext')
        subtext_links.extend(links)
    return subtext_links


def sort_stories_by_votes(hacker_news_list):
    return sorted(hacker_news_list, key=lambda k: k['points'], reverse=True)


def createCustomHackerNews(links, subtext):
    hacker_news_list = []
    for index, item in enumerate(links):
        title = item.getText()
        story_link = item.get('href', None)
        vote = subtext[index].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            # I want the title and the link for the story that has 100 or more points
            if points >= 100:
                hacker_news_list.append({'title': title, 'link': story_link, 'points': points})
    return sort_stories_by_votes(hacker_news_list)


pprint.pprint(createCustomHackerNews(get_links(get_response_list()), get_subtexts(get_response_list())))

