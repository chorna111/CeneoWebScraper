from flask import Flask,render_template,redirect,request,send_file,session
import requests
from modules import scraper,analyser
import json
import glob
import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import pandas as pd
app = Flask(__name__,static_folder='static')
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('mainpage.html')

@app.route('/ekstrakcja_opinii', methods=['GET', 'POST'])


def ekstrakcja_opinii():
     if request.method == 'POST':
        kod_produktu = request.form.get('kod-produktu')
        
        if kod_produktu.strip() == '':
            
            error_message = 'Nic nie wprowadziłeś. Podaj kod produktu.'
            return render_template('ekstraction.html', error_message=error_message)
        else:
            url = f'https://www.ceneo.pl/{kod_produktu}'
            response = requests.get(url)
            
            if response.status_code == 200 or response.status_code==405:
                urlreview=f'https://www.ceneo.pl/{kod_produktu}#tab=reviews'
                all_opinions=scraper.get_opinions(urlreview)
                
                scraper.dumping_to_opinions(kod_produktu,all_opinions)
                scraper.dumping_to_products(kod_produktu)
                opinions=pd.read_json(f'./opinions/{kod_produktu}.json')
                analyser.charts(opinions,kod_produktu)
                return redirect(url)
            else:
                error_message = 'Niepoprawny kod produktu. Spróbuj jeszcze raz.'
                return render_template('ekstraction.html', error_message=error_message)
     else:
        return render_template('ekstraction.html')

@app.route('/ekstraction')
def scenariusz2():
    return render_template('ekstraction.html')
@app.route('/lista-produktow')
def lista_produktow():
    
    products_data = []
    
    json_files = glob.glob('./products/*.json')
    
    for file in json_files:
        with open(file, 'r', encoding='UTF-8') as jf:
            products_data += json.load(jf)
    
    return render_template('productslist.html', products=products_data)
@app.route('/download/<path:file_path>')
def download_file(file_path):
    try:
        full_path = os.path.join(app.root_path, file_path)
        return send_file(full_path, as_attachment=True)
    except FileNotFoundError:
        error_message = 'File not found.'
        return render_template('error.html', error_message=error_message)
@app.route('/product/<product_id>')
def product_page(product_id):
    opinions = []
    json_files = glob.glob('./opinions/*.json')
    
    for file in json_files:
        filename = os.path.basename(file)
        if filename.startswith(product_id):
            with open(file, 'r') as json_file:
                opinions = json.load(json_file)
                break  
    return render_template('product.html', opinions=opinions,product_id=product_id)

@app.route('/charts/<product_id>')
def charts_page(product_id):
    filename_for_score_chart=f'{product_id}_score.png'
    filename_for_recommendation_chart=f'{product_id}_recommendation.png'
    return render_template('charts.html',filename_for_score_chart=filename_for_score_chart,filename_for_recommendation_chart=filename_for_recommendation_chart,product_id=product_id)

