import requests
import bs4

''' Scraping module '''

def parse_name(name):
    name_parsed = name.title()
    name_parsed = name_parsed.replace(' ', '_')

    return name_parsed

def who_is(name):
    url = 'https://es.wikipedia.org/wiki/'
    request_page = requests.get(url)
    
    #print(f'{url} request in progress \n')

    name = parse_name(name)
    request_page = requests.get(url+name)
    html_soup_inner = bs4.BeautifulSoup(request_page.content, 'html.parser')

    texto = html_soup_inner.find('div',{'id':'mw-content-text'})
    texto = html_soup_inner.find('div', {'class' :'mw-parser-output'})			
    texto = html_soup_inner.find('p').text
    
    if texto != "":
        name = name.replace('_', ' ')
        return texto