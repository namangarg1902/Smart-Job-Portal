
import json 

import os
import sys
import subprocess

# pip install custom package to /tmp/ and add to path
subprocess.call('pip install requests -t /tmp/ --no-cache-dir'.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.call('pip install bs4 -t /tmp/ --no-cache-dir'.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

sys.path.insert(1, '/tmp/')

import requests
from bs4 import BeautifulSoup

 
images = ["images/software-engineer.svg" , "images/data-scientist.svg" , "images/project-manager.svg" , "images/product-manager.svg" , "images/sales-representative.svg" , "images/marketing-manager.svg"]

img_id = 0 

def naukridotcom(pos):
  pos.replace(" ","-")
  target_url = "https://www.shine.com/job-search/{}-jobs?q={}"
  url = target_url.format(pos,pos)
  print(requests.get(url))
  return url

def times_jobs(pos):
  pos.replace(" ","+")
  target_url = "https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={}"
  url = target_url.format(pos)
  # print(requests.get(url))
  return url



def fetch_times(designation):
  json_data = {}
  id = 0 
  global img_id
  target_url = times_jobs(str(designation))
  print("Data From Times Jobs  :")
  response = (requests.get(target_url))
  soup = BeautifulSoup(response.text, 'html.parser')
  cards = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

  l  = len(cards)

  if l<=3 :
    print("Jobs currently not there")
    return 

  # if(l>10) :
  #   l = 5
  # data = []
  
  for i in range(l):
    temp = cards[i].h2.a
    # bro = []
    # bro.append("Profile: "+(temp.strong.text).strip())
    # bro.append("Company Name: "+((cards[i].find('h3', 'joblist-comp-name')).text).strip())
    # bro.append("Apply Now: "+temp.get('href'))

    if temp.strong is None :
      return 

    pos = (temp.text).strip()
    com = ((cards[i].find('h3', 'joblist-comp-name')).text).strip().upper()
    app = temp.get('href')
    img = images[img_id]

    json_data[id] = {"Position": pos,"Company": com, "Apply Now": app , "Img": img}

    if img_id == 5:
      img_id = 0
    else :
      img_id+=1

    # print(pos)
    # print(com)
    # print(app)
    id += 1

  temp = json_data
  json_data = {}

  return temp
  # return json.dumps(json_data)


def fetch_shine(designation):

  json_data = {}
  id = 0 

  global img_id
  target_url = naukridotcom(str(designation))

  response = (requests.get(target_url))
  soup = BeautifulSoup(response.text, 'html.parser')

  req = soup.select('div h2[itemprop="name"]')
  #fetching the text from the html
  links = [(target_url+r.a.get('href')) for r in req]
  titles = [r.text for r in req]
  #Removing any spaces
  titles = [t.replace("  ", "") for t in titles]


  orgs = soup.find_all('div', class_='jobCard_jobCard_cName__mYnow')
  #fetching the text from the HTML
  orgs1 = [o.text for o in orgs]
  sub_string ='Hiring'
  #Splitting the string on a sub string and getting the first index (Cleaning up names)
  orgs1 = [o.split(sub_string)[0] for o in orgs1]
  #Removing any spaces
  orgs1 = [o.strip().upper() for o in orgs1]

  # temp = []
  
  for i in range(5):
    # bro = []

    # bro.append("Profile: " + titles[i])
    # bro.append("Company: " + orgs1[i])
    # bro.append("Apply Now: " + links[i])

    im = images[img_id]
    json_data[id] = {"Position": titles[i] , "Company": orgs1[i], "Apply Now": links[i], "Img": im}

    if img_id == 5 :
      img_id = 0
    else:
      img_id+=1


    id += 1

    # temp.append(bro)
  # return json.dumps(json_data)
    
  temp = json_data
  json_data = {}

  return temp


# def lambda_handler(event , context):
def lambda_handler(designation):

    # designation = event["design"]

    # designation = input("enter designation")

    global json_data

    fetch_times(designation)

    fetch_shine(designation)

    # print(json_data)

    # response_data = {
    #     "final_data_times": json.dumps(final_data_times),
    #     "final_data_shine": json.dumps(final_data_shine)
    # }

    # return {
    #     'statusCode': 200,
    #     'body': json.dumps(response_data)
    # }

    # for i in final_data_shine:
    #   for j in i:
    #     print(j)
    
    # for i in final_data_times:
    #   for j in i:
    #     print(j)

    # return final_data_shine 

    temp = json_data

    json_data = {}

    return temp