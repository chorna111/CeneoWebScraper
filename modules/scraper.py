from bs4 import BeautifulSoup
import requests
import json
import os 
import csv
import pandas as pd
def get_element(ancestor,selector=None,attribute=None,return_list=False):
    try:
        if return_list:
            return [tag.text.strip() for tag in ancestor.select(selector)].copy()
        if not selector and attribute:
            return ancestor[attribute]
        if attribute:
            return ancestor.select_one(selector)[attribute].strip()
        return ancestor.select_one(selector).text.strip()
    except (AttributeError,TypeError):
        return None
    
selectors={
        'id_opinii':[None,'data-entry-id'],
        'author':['span.user-post__author-name'],
        'published_at':['span.user-post__published>time:nth-child(1)','datetime'],
        'recommendation':['span.user-post__author-recomendation>em',None,True],
        'score':['span.user-post__score-count'],
        'pros':['div.review-feature__col:has(>div.review-feature__title--positives)>div.review-feature__item',None,True],
        'cons':['div.review-feature__col:has(>div.review-feature__title--negatives)>div.review-feature__item',None,True]
    }
single_product={}
all_products=[]
def get_opinions(x):
    
    all_opinions=[]
    while(x):
        
        response=requests.get(x)
        
        page=BeautifulSoup(response.text,'html.parser')
        opinions=page.select('div.js_product-review')
        
        for opinion in opinions:
                single_opinion={}
                product_name=page.select_one('div.product-top__title').text.strip()
                score_average=page.select_one('font').text.strip()
                single_opinion['name_of_product']=product_name
                single_opinion['average_score']=score_average
                for key,value in selectors.items():
                    
                         
                    single_opinion[key]=get_element(opinion,*value)
                  

                
                all_opinions.append(single_opinion)
        try:
        
            x='https://www.ceneo.pl'+get_element(page,'a.pagination__next','href')
        except TypeError:
            x=None 
            
            single_product['name']=product_name
            single_product['whole_count_of_opinions']=len(all_opinions)
            single_product['average_score']=score_average
            single_product['whole_count_of_pros']=sum(len(dict['pros']) for dict in all_opinions)
            single_product['whole_count_of_cons']=sum(len(dict['cons']) for dict in all_opinions)
    return all_opinions
   
        
    
def dumping_to_opinions(product_code,all_opinions):

    for single_opinion in all_opinions:
        single_opinion['id']=product_code
        

    try:
        
        os.mkdir('./opinions')
    except FileExistsError:
        pass

    with open(f'./opinions/{product_code}.json','w',encoding='UTF-8') as jf:
        json.dump(all_opinions,jf,indent=4,ensure_ascii=False)
    
  
    with open(f'./opinions/{product_code}.csv', 'w', encoding='UTF-8') as cf:
        fieldnames = all_opinions[0].keys()
        writer = csv.DictWriter(cf, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_opinions)
    df=pd.DataFrame.from_dict(all_opinions)
    
    df.to_excel(f'./opinions/{product_code}.xlsx')

all_products.append(single_product)
def dumping_to_products(product_code):
    single_product['id']=product_code
    try:
         
         os.mkdir('./products')
    except FileExistsError:
         pass
    with open(f'./products/{product_code}.json','w',encoding='UTF-8') as jf:
               json.dump(all_products,jf,indent=4,ensure_ascii=False)