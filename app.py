import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import Input , Output , State



def work_on_dataset():
    print("Hey")
    df = pd.read_csv('data/suicides.csv')
    df = df.rename(columns={'suicides/100k pop':'suicides/100k_pop'})
    european_countries = ['Russia','Germany','United Kingdom','France','Italy','Spain','Ukraine', 'Poland','Romania','Netherlands','Belgium', 'Czech Republic' , 'Greece' , 'Portugal'  ,'Sweden' , 'Hungary', 'Belarus' , 'Austria', 'Serbia' ,  'Switzerland' , 'Bulgaria' , 'Denmark' , 'Finland', 'Slovakia', 'Norway', 'Ireland' , 'Croatia' , 'Moldova' , 'Bosnia and Herzegovina',  'Albania' ,  'Lithuania' , 'North Macedonia' ,  'Slovenia' , 'Latvia',  'Estonia',  'Montenegro' ,  'Luxembourg', 'Malta', 'Iceland' ]
    df_europe = df.copy()
    df_europe = df_europe.loc[df_europe['country'].isin(european_countries)]
    df_europe_country_year_grouped =  df_europe.groupby(['country','year'])[['suicides_no','population','suicides/100k_pop']].agg('sum').reset_index()
    df_europe_country_year_grouped.head()


    ############ BUILD APP ######
    app = dash.Dash(__name__)
    server = app.server
    app.layout = html.Div([

    html.Div([
        html.H1('SUICIDES IN EUROPE IN THE BEGGINING OF CENTURY XXI')
        ], className='Title') ])

    app.run_server()




if __name__ == '__main__':
    work_on_dataset()


