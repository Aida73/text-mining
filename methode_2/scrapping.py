from bs4 import BeautifulSoup
import urllib
import requests


# Check the Network
def connect(host='https://www.rimessolides.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False


"""This function will help us to a list of data which are used in order to label a dataframe
It returns a list of elements. 
"""

# raise case aucun resultat
# raise case serveur error
# raise case not correct word


def getCategories(categorie):

    url = 'https://www.rimessolides.com/motscles.aspx'
    import random
    # We use a list of fake agents to bypass the limitations of some sites against scrapping
    user_agents_list = [
        'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    ]

    categories = []
    if connect():
        res = requests.get(url, headers={
                           'User-Agent': random.choice(user_agents_list)}, params={'m': categorie})
        #res = requests.get(url)
        if res.ok:
            soup = BeautifulSoup(res.text, 'lxml')
            result = soup.findAll('a', {'class': 'l-black'})
            noResult = soup.find('span', {'class': 'medium-bold'})
            if (noResult and noResult.text.startswith("Aucun")):
                return "Une des catégorie n'est pas correct"
            else:
                for elt in result:
                    categories.append(elt.text)
                return categories

        else:
            return res.headers
    else:
        print("Verifier votre connexion internet")


#print(isinstance(getCategories("médicalejfnrjn"), str))
