import requests
from bs4 import BeautifulSoup
import json

base_url = 'https://www.elections.ca/Scripts/vis'

# List of Postal Codes
postal_codes = []
json_object = []

# Genesys API environment variables
endpoint = 'https://api.genesysappliedresearch.com/v2/knowledge'
kb_id = '6f1d63c3-1da0-4a1f-b94f-6e6a412987ed'
language_code = 'en-US'
org_id = 'e2242208-c200-4b57-af40-9e855461cec7'
secret_key = '11b1af90-7ebf-4418-a3eb-7e34ba756c84'

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
            answer += str(element.string).replace(':', '.').replace('\n', '.')
        json_object.append(create_document(question=question, answer=answer))

# Get candidates for postal code
def get_candidates_for(postal_code):
    candidate_url = '''{baseUrl}/candidates?L=e&ED=35007&EV=51&EV_TYPE=1&PC={postalCode}&PROV=ON&PROVID=35&QID=-1&PAGEID=17'''.format(
    baseUrl=base_url, postalCode=postal_code)
    response = requests.get(candidate_url)
    soup = BeautifulSoup(response.text, "html.parser")
    region = soup.find('h3', class_='HeaderInfo1')
    for element in soup.find_all('tr'):
        for data in element.children:
            if any(word in str(data) for word in ['Liberal', 'Conservative', 'New Democratic']):
                question = 'Who is the running candidate for '
                if str(data.string.strip()) == 'Liberal Party of Canada':
                    question += 'Liberals '
                elif str(data.string.strip()) == 'Conservative Party of Canada':
                    question += 'Conservatives '
                else:
                    question += 'New Democrats NDP '
                question += 'in {postalCode}'.format(postalCode=postal_code)
                answer = '{candidate} is the running candidate for {party} in {region}'.format(
                    candidate=str(data.find_previous_sibling('td').find_previous_sibling('td').string.strip()), party=str(data.string.strip()), region=str(region.string))
                json_object.append(create_document(question=question, answer=answer))


def create_document(question, answer):
    response = {
    "type": "faq",
    "faq": {
        "question": question,
        "answer": answer
    }
    }
    return response

get_postal_codes()
for code in postal_codes:
    get_venue_for(postal_code=code)
    get_candidates_for(postal_code=code)

# Create documents for knowledge base
response = requests.post('{endpoint}/generatetoken'.format(endpoint=endpoint),
    headers={ 'organizationid': org_id, 'secretkey': secret_key }
)

response = response.json()

token = response['token']

response = requests.patch('{endpoint}/knowledgebases/{kbid}/languages/{languageCode}/documents'.format(endpoint=endpoint, kbid=kb_id, languageCode=language_code),
    data=json.dumps(json_object),
    headers={ 'Content-Type': 'application/json', 'organizationid': org_id, 'token': token })

