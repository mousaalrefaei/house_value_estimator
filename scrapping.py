from email import header
from bs4 import BeautifulSoup, SoupStrainer
import requests
from time import sleep
from datetime import datetime
import csv
import threading


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1'
}

cookies = {"CONSENT": "YES+cb.20210720-07-p0.en+FX+410"}

#property_type = {'Apartment': '1', 'Haus': '2'}
property_type = {'Haus': '2'}
states = {
  'Schleswig-Holstein':'1',
  'Hamburg':'2',
  'Niedersachsen':'3',
  'Bremen': '4',
  'Nordrhein-Westfalen':'5',
  'Hessen':'6',
  'Rheinland-Pfalz':'7',
  'Baden-Württemberg':'8',
  'Bayern':'9',
  'Saarland':'10',
  'Berlin':'11',
  'Brandenburg':'12',
  'Mecklenburg-Vorpommern':'13',
  'Sachsen':'14',
  'Sachsen-Anhalt':'15',
  'Thüringen':'16'
}

def max_page(state, type): 
  url= 'https://www.immonet.de/immobiliensuche/sel.do?suchart=1&state=1&marketingtype=1&pageoffset=27&parentcat='+ property_type[type]+ '&sortby=0&listsize=27&objecttype=1&federalstate='+ states[state] +'&page=1'
  get_tag = SoupStrainer('div', attrs={'class':'row padding-sm-12 padding-top-sm-0'})
  response = requests.request("GET", url,headers=headers, cookies=cookies)
  soup = BeautifulSoup(response.text, 'html.parser', parse_only= get_tag)
  return soup.find_all('li', attrs={'class':'pagination-item'})[4].text



def get_lists(state, type, page):
  try:
    url = 'https://www.immonet.de/immobiliensuche/sel.do?suchart=1&state=1&marketingtype=1&pageoffset=27&parentcat='+ property_type[type]+'&sortby=0&listsize=27&objecttype=1&federalstate='+ states[state] +'&page=' + str(page)
    get_tag = SoupStrainer('div', attrs={'class':'row padding-sm-12 padding-top-sm-0'})
    response = requests.request("GET", url, headers=headers,cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser', parse_only= get_tag)
    url_list = ['https://www.immonet.de' + x['href'] for x in soup.find_all('a', attrs={'class':'block ellipsis text-225 text-default'})]
    print(f'get links from the page number: {page}/ {maxpage} for the property type: {type} in the state: {state}')
    return url_list
  except Exception as e:
    print(f'the listing error is {e}')
    sleep(2)



def get_data(url):
  try:
    get_tag = SoupStrainer('div', attrs={'class':'col-xs-12 box-50'})
    response = requests.request("GET", url, headers=headers,cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser', parse_only= get_tag)
    data = {}
    data['URL'] = url
    data['State'] = state
    data['Property_type'] = type
    data['Date'] = str(datetime.now())
    try:
      data['Ort'] = soup.find('p', attrs={'class':'text-100 pull-left'}).text.replace('Auf Karte anzeigen','').strip().replace('\t','').replace('\n','-').replace('\xa0','')
    except: data['Ort'] = ''
    try:
      data['Title'] = soup.find('h1', attrs={'id':'expose-headline'}).text.strip()
    except: data['Title'] = ''
    try:
      data['Kaufpreis'] =  soup.find('div', attrs={'id':'priceid_1'}).text.strip().replace('€','').replace('.00','')
    except: data['Kaufpreis'] = ''
    try:
      data['Courtage für Käufer'] = soup.find('div', attrs={'id':'courtageValue'}).text.strip()
    except: data['Courtage für Käufer'] = ''
    try:
      data['Zimmer'] = soup.find('div', attrs={'id':'equipmentid_1'}).text.strip()
    except: data['Zimmer'] = ''
    try:
      data['Anzahl Parkflächen'] = soup.find('div', attrs={'id':'equipmentid_13'}).text.strip()
    except: data['Anzahl Parkflächen'] = ''
    try:
      data['Wohnfläche ca.'] = soup.find('div', attrs={'id':'areaid_1'}).text.strip().replace('\xa0m²','')
    except: data['Wohnfläche ca.'] = ''
    try:
      data['Grundstücksfläche ca.'] = soup.find('div', attrs={'id':'areaid_3'}).text.strip().replace('\xa0m²','')
    except: data['Grundstücksfläche ca.'] = ''
    try:
      data['Zustand'] = soup.find('div', attrs={'id':'objectstatecategoryValue'}).text.strip()
    except: data['Zustand'] = ''
    try:
      data['Baujahr'] = soup.find('div', attrs={'id':'yearbuild'}).text.strip()
    except: data['Baujahr'] = ''
    try:
      data['Verfügbar ab'] = soup.find('div', attrs={'id':'deliveryValue'}).text.strip()
    except: data['Verfügbar ab'] = ''
    try:
      data['Energieeffizienzklasse'] = soup.find('div', attrs={'id':'efficiencyValue'}).text.strip()
    except: data['Energieeffizienzklasse'] =''
    try:
      data['Endenergiebedarf'] = soup.find('div', attrs={'id':'energyValue'}).text.strip()
    except: data['Endenergiebedarf'] = ''
    try:
      data['Energieausweis'] = soup.find('div', attrs={'id':'electricityConsumptionValue'}).text.strip()
    except: data['Energieausweis'] = ''
    try:
      data['Heizungsart'] = soup.find('div', attrs={'id':'heatTypeValue'}).text.strip()
    except: data['Heizungsart'] = ''
    try:
      data['Befeuerungsart'] = soup.find('div', attrs={'id':'heaterSupplierValue'}).text.strip()
    except: data['Befeuerungsart'] = ''
    try:
      data['Baujahr (laut Energieausweis)'] = soup.find('div', attrs={'id':'yearBuildByPassValue'}).text.strip()
    except: data['Baujahr (laut Energieausweis)'] = ''
    try:
      data['Ausstatung'] = soup.find('div', attrs={'id':'ausstattung'}).text.strip()
    except: data['Ausstatung'] = ''
    try:
      data['Objektbeschreibung'] = soup.find('p', attrs={'id':'objectDescription'}).text.strip()
    except: data['Objektbeschreibung'] = ''
    try:
      data['Lage'] = soup.find('p', attrs={'id':'locationDescription'}).text.strip()
    except: data['Lage'] = ''
    try:
      data['Sonstiges'] = soup.find('p', attrs={'id':'otherDescription'}).text.strip()
    except: data['Sonstiges'] = ''
    try:
      data['Anbieter'] = soup.find('span', attrs={'id':'bdBrokerFirmname'}).text.strip()
    except: data['Anbieter'] = ''

    writer.writerow(data)

  except Exception as e:
    print(e)


columns = ['URL','State','Property_type','Date','Ort','Title','Kaufpreis','Courtage für Käufer','Zimmer','Anzahl Parkflächen','Wohnfläche ca.', 'Grundstücksfläche ca.','Zustand','Baujahr', 'Verfügbar ab','Energieeffizienzklasse','Endenergiebedarf','Energieausweis','Heizungsart','Befeuerungsart', 'Baujahr (laut Energieausweis)', 'Ausstatung', 'Objektbeschreibung', 'Lage','Sonstiges', 'Anbieter']

output_file = open('properties.csv', 'a+', newline='', encoding='utf8')
writer = csv.DictWriter(output_file, fieldnames=columns, extrasaction='ignore')
writer.writeheader()


try:
  for type in property_type:
    for state in states:
      maxpage = max_page(state, type)
      for page in range(1,int(maxpage)):
          list = get_lists(state,type, page)
          threads = []
          for link in list:
            thread = threading.Thread(target=get_data, args=(link,))
            threads.append(thread)
            thread.start()
            if len(threads) == 26:
              for thread in threads:
                thread.join()
              threads =[]
          for thread in threads:
            thread.join()
          print(f'***** State: {state} , Type: {type}, Progress: {page} / {maxpage}')
except Exception as e:
  print(f'the error is : {e}')


##### if there is an issue while opening the csv file, use the folowing code: ####

# df = pd.read_csv('file_name.csv',encoding= 'unicode_escape', on_bad_lines='skip')
