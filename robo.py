import requests
import bs4
import re
import mysql.connector
import sys
import random
import threading
import time
import json
from datetime import datetime




def run_every():
    threading.Timer(random.randint(60.0, 300.0), run_every).start() # called every minute
    config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
    'database': 'ads',
    'raise_on_warnings': True
    }
    mydb = mysql.connector.connect(**config)

    mycursor = mydb.cursor()

    def get_city_function():
        cities = list()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM cities")
        myresult = mycursor.fetchall()
        for x in myresult:
            cities.append(x[1])
        return cities[random.choice(range(len(cities)))]

    city_name = get_city_function()
    
    print("start fetch")
    
    DIVAR_BASE_URL = 'https://divar.ir'
    # divar shiraz

    divar = requests.get(
        DIVAR_BASE_URL + '/s/'+city_name)
    divar_soup = bs4.BeautifulSoup(divar.content, 'lxml')

    #print(DIVAR_BASE_URL + '/s/'+city_name+'/auto')
    
    #sys.exit()
    results = divar_soup.select('.post-card-item')

    i = 0
    links_to_product = list()
    while i < len(results):
        links_to_product.append(results[i].select(
            '.kt-post-card')[0].get('href'))
        i += 1

    items = []
    for link_to_product in links_to_product:
        print(DIVAR_BASE_URL+link_to_product)
        product = requests.get(DIVAR_BASE_URL+link_to_product)
        product_soup = bs4.BeautifulSoup(product.content, 'lxml')
        x = product_soup.title.string.split("|")
                
        from bs4 import BeautifulSoup  
        soup = BeautifulSoup(product.text, 'html.parser')  
        
        #soup = soup.select('<div>',attrs={'class':'kt-carousel post-image-slider kt-carousel--padded'})
        #results = soup.select('img', attrs={'class':'kt-image-block__image'})
        
        records = []  
        str = "divarcdn"
        #for result in results:  
            #if str in result['src']:
               # records.append(result['src'])
            


        #print('images:  ')
        #print(records)

        #if(len(records) > 0 ):
            #print(x)

        title = x[0]
        category = x[1]
        city = x[2]
        province = city_name
        #city = x[2].split('،')[1]
        #province = x[2].split('،')[0]
        patterns = link_to_product.split('/')
        code =format(patterns[-1])
        

        headers = {
            "Host": "api.divar.ir",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://divar.ir/",
            "Authorization": "Basic eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiMDkzODQyMjc0NzciLCJpc3MiOiJhdXRoIiwiaWF0IjoxNjU2NzU4MDA5LCJleHAiOjE2NTgwNTQwMDksInZlcmlmaWVkX3RpbWUiOjE2NTY3NTgwMDksInVzZXItdHlwZSI6InBlcnNvbmFsIiwidXNlci10eXBlLWZhIjoiXHUwNjdlXHUwNjQ2XHUwNjQ0IFx1MDYzNFx1MDYyZVx1MDYzNVx1MDZjYyIsInNpZCI6ImVhN2Q5OTI0LTI3ZDQtNDRmOS05OGY5LTBiZjNkN2IzNGFhMSJ9.tY7bF-ixMP5ajwZoLeSU5eTobFpLkSN8giiX61t0IDc",
            "Origin": "https://divar.ir",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
        }
        phone_number = requests.get('https://api.divar.ir/v5/posts/'+(code)+'/contact/',headers=headers)
        #print(phone_number.json())
        phone = phone_number.json()['widgets']['contact']['phone']
        
        print('Title: '+title)
        print('Category: '+category)
        print('City: '+city)
        print('Phone: '+phone)
        print('Code: '+code) 

        if phone and phone.strip():
            items.append( (title, category,city,phone,code,json.dumps(records)) );
            """
            except NameError:
                phone_number.json()['error']:
                print("there is an error for fetching")
                time.sleep(random.randint(600.0, 1200.0))
            """
            mycursor = mydb.cursor()
            sql = "INSERT INTO ads (title,category,city,phone,code,images) VALUES (%s, %s, %s, %s, %s, %s)"
            mycursor.executemany(sql, items)

            mydb.commit()
            mydb.close()
        time.sleep(random.randint(60.0, 300.0))

    """
    mycursor = mydb.cursor()
    sql = "INSERT INTO ads (title,category,city,province,phone,code) VALUES (%s, %s, %s, %s, %s, %s)"
    mycursor.executemany(sql, items)

    mydb.commit()

    """
run_every()
