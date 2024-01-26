import requests
import json
import bs4
import re
import fire

def hello(name="World"):
  return "Hello %s!" % name

def get_news(keyword, news_count=10):
    #keyword = 'anies'
    response = requests.get(f'https://www.google.com/search?q={keyword}&tbm=nws&start=10', headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0'})
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    linkElems = soup.select('a.WlydOe')
    links = []
    for linkElem in linkElems:
        titleElem = linkElem.select_one('div.n0jPhd')
        links.append({
            'title': titleElem.getText(),
            'href': linkElem.get('href')
        })
    #print(json.dumps(links, indent=2))

    for link in links:
        response = requests.get(link['href'], headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0'})
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        contentElems = soup.select('p, span, div.post-content')
        # filter only elements with text that ends with ., ", ?, or ' and contain more than 4 words
        contentElems = list(filter(lambda elem: re.search(r'(\.|\"|\?|\')$', elem.getText()) and len(elem.getText().split()) > 4, contentElems))
        content = '\n'.join(map(lambda elem: elem.getText(), contentElems))
        link['content'] = content

    with open('news.json', 'w') as f:
        json.dump(links, f, indent=2)

if __name__ == '__main__':
  fire.Fire(get_news)