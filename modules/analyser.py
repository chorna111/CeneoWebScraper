import os
import pandas as pd
import numpy as np



def charts(opinie, kod):
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import pyplot as plt
    opinie.score=opinie.score.map(lambda x: float(x.split('/')[0].replace(',','.')))
    score=opinie.score.value_counts().reindex(list(np.arange(0,5.5,0.5)),fill_value=0)
    score.plot.bar(color='hotpink')
    plt.xticks(rotation=0)
    plt.title('Liczba opinii z poszczególnymi liczbami gwiazdek')
    plt.xlabel('Liczba gwiazdek')
    plt.ylabel('Liczba opinii')
    for index,value in enumerate(score):
        plt.text(index,value+0.5,str(value),ha='center')
    try:
        
        os.mkdir('./app/static')
       
        
    except FileExistsError:
        pass
    plt.savefig(f'./app/static/{kod}_score.png')
    plt.close()
   
    recommendation=opinie['recommendation'].value_counts(dropna=False).sort_index()
    recommendation.plot.pie(label='',
                            autopct='%1.1f%%',
                            labels=['Nie polecam','Polecam','Nie mam zdania'],
                            colors=['hotpink','pink','gray'])
    
    plt.legend(bbox_to_anchor=(0.1,0.5,0.1,0.5))
    plt.title('Udział poszczególnych rekomendacji w ogólnej liczbie opinii')
    try:
        
        os.mkdir('./app/static')
       
        
    except FileExistsError:
        pass
    plt.savefig(f'./app/static/{kod}_recommendation.png')
    plt.close()
 
  