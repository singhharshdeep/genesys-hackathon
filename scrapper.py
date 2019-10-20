import requests
from bs4 import BeautifulSoup
import json

base_url = 'https://www.elections.ca/Scripts/vis'

# List of Postal Codes
postal_codes = []
faqs = {}
json_object = []

# Load postal codes
def get_postal_codes():
    postal_codes_url = 'https://data.mongabay.com/igapo/toronto_zip_codes.htm'
    response = requests.get(postal_codes_url)
    soup = BeautifulSoup(response.text, "html.parser")
    for region in soup.findAll('td', text=lambda text: text and 'M4B' in text)[0:20]:
        postal_codes.append(str(region.string).strip().replace(' ', ''))

# Get venue information for postal code
def get_venue_for(postal_code):
    venue_url = '{baseUrl}/voting?L=e&ED=35007&EV=51&EV_TYPE=1&PC={postalCode}&PROV=ON&PROVID=35&PAGEID=31'.format(baseUrl=base_url, postalCode=postal_code)
    response = requests.get(venue_url)
    soup = BeautifulSoup(response.text, "html.parser")
    if len(soup.find_all('ul', class_='toc')) != 0:
        question = 'Where do I vote in {postalCode}'.format(postalCode=postal_code)
        answer = ''
        for element in soup.find_all('ul', class_='toc')[0].children:
            answer += str(element.string)
        json_object.append(create_document(question=question, answer=answer))

# Get candidates for postal code
def get_candidates_for(postal_code):
    candidate_url = '''{baseUrl}/candidates?L=e&ED=35007&EV=51&EV_TYPE=1&PC={postalCode}&PROV=ON&PROVID=35&QID=-1&PAGEID=17'''.format(
    baseUrl=base_url, postalCode=postal_code)
    response = requests.get(candidate_url)
    soup = BeautifulSoup(response.text, "html.parser")
    for element in soup.find_all('tr'):
        for data in element.children:
            if any(word in str(data) for word in ['Liberal', 'Conservative', 'New Democrat']):
                question = 'Who is the running candidate for '
                if str(data.string.strip()) == 'Liberal Party of Canada':
                    question += 'Liberals '
                elif str(data.string.strip()) == 'Conservative Party of Canada':
                    question += 'Conservatives '
                else:
                    question += 'New Democrats (NDP) '
                question += 'in {postalCode}'.format(postalCode=postal_code)
                answer = '{candidate} is the running candidate for {party} in {postalCode}'.format(
                candidate=str(data.previous_sibling.previous_sibling.previous_sibling.previous_sibling.string.strip()), party=str(data.string.strip()), postalCode=postal_code)
                json_object.append(create_document(question=question, answer=answer))


def create_document(question, answer):
    response = {
    "type": "faq",
    "faq": {
        "question": question,
        "answer": answer
    }
    }
    return json.dumps(response)

get_postal_codes()
for code in postal_codes:
    get_venue_for(postal_code=code)
    get_candidates_for(postal_code=code)

print(len(json_object))
# print(json.dumps(json_object))
