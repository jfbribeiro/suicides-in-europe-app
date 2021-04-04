import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input , Output , State
import plotly.express as px

# ----------------------- DATA PROCESSMENT


df = pd.read_csv('data/suicides.csv')
df = df.rename(columns={'suicides/100k pop':'suicides/100k_pop'})
european_countries = ['Russian Federation','Germany','United Kingdom','France','Italy','Spain','Ukraine', 'Poland','Romania','Netherlands','Belgium', 'Czech Republic' ,
                          'Greece' , 'Portugal'  ,'Sweden' , 'Hungary', 'Belarus' , 'Austria', 'Serbia' ,  'Switzerland' , 'Bulgaria' , 'Denmark' , 'Finland',
                          'Slovakia', 'Norway', 'Ireland' , 'Croatia' , 'Cyprus' , 'Bosnia and Herzegovina',  'Albania' ,  'Lithuania' ,  'Slovenia' , 'Latvia',
                          'Estonia',  'Montenegro' ,  'Luxembourg', 'Malta', 'Iceland' ]
df_europe = df.copy()
df_europe = df_europe.loc[df_europe['country'].isin(european_countries)]
df_europe_country_year_grouped =  df_europe.groupby(['country','year'])[['suicides_no','population','suicides/100k_pop']].agg('sum').reset_index()
df_europe_country_year_grouped.head()

options = [
        {"label": "Russian Federation", "value": "Russian Federation"},
        {"label": "Germany", "value": "Germany"},
        {"label": "United Kingdom", "value": "United Kingdom"},
        {"label": "France", "value": "France"},
        {"label": "Italy", "value": "Italy"},
        {"label": "Spain", "value": "Spain"},
        {"label": "Ukraine", "value": "Ukraine"},
        {"label": "Poland", "value": "Poland"},
        {"label": "Romania", "value": "Romania"},
        {"label": "Netherlands", "value": "Netherlands"},
        {"label": "Belgium", "value": "Belgium"},
        {"label": "Czech Republic", "value": "Czech Republic"},
        {"label": "Greece", "value": "Greece"},
        {"label": "Portugal", "value": "Portugal"},
        {"label": "Sweden", "value": "Sweden"},
        {"label": "Hungary", "value": "Hungary"},
        {"label": "Belarus", "value": "Belarus"},
        {"label": "Austria", "value": "Austria"},
        {"label": "Serbia", "value": "Serbia"},
        {"label": "Switzerland", "value": "Switzerland"},
        {"label": "Bulgaria", "value": "Bulgaria"},
        {"label": "Denmark", "value": "Denmark"},
        {"label": "Finland", "value": "Finland"},
        {"label": "Slovakia", "value": "Slovakia"},
        {"label": "Norway", "value": "Norway"},
        {"label": "Ireland", "value": "Ireland"},
        {"label": "Croatia", "value": "Croatia"},
        {"label": "Bosnia and Herzegovina", "value": "Bosnia and Herzegovina"},
        {"label": "Albania", "value": "Albania"},
        {"label": "Lithuania", "value": "Lithuania"},
        {"label": "Slovenia", "value": "Slovenia"},
        {"label": "Latvia", "value": "Latvia"},
        {"label": "Estonia", "value": "Estonia"},
        {"label": "Montenegro", "value": "Montenegro"},
        {"label": "Luxembourg", "value": "Luxembourg"},
        {"label": "Malta", "value": "Malta"},
        {"label": "Iceland", "value": "Iceland"},
        {"label": "Cyprus", "value": "Cyprus"},
    ]

years = []

colors = {
    'background': '#BBBABA',
    'title': '#9B1E03',
    'text': '#000000'
}

#---------------------  BUILD APP LAYOUT
app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([
    html.Br(), html.Br(),
    html.Div([
        html.H1('SUICIDES IN EUROPE IN THE BEGGINING OF CENTURY XXI')
        ], className='title' ,style={'textAlign':'center'}),
    html.Div([
        html.P('This web application was developed within the scope of the "Data Visualization" course to explore in an interactive way the evolution of suicides in Europe at the beginning of the current century.')
    ],style={'textAlign':'center'}),
    html.Br(), html.Br(), html.Br(),

    #------ PARENT DIV : CONTAIN CHLOROPLET MAP AND MULTIPLE COMPARISION PLOT
    html.Div([

    #---- LEFT PANEL
    html.Div([
    html.Div([
            dcc.Graph(id="europe_map")
    ]),

    html.Br(),html.Br(),html.Br(),

    html.Div([
    dcc.Slider(
        id='slider_date',
        min=2000,
        max=2015,
        step=1,
        value=2000,
        marks={
          2000: {'label': '2000', 'style': {'color': colors['title']}},
          2001: {'label': '2001', 'style': {'color': colors['title']}},
          2002: {'label': '2002', 'style': {'color': colors['title']}},
          2003: {'label': '2003', 'style': {'color': colors['title']}},
          2004: {'label': '2004', 'style': {'color': colors['title']}},
          2005: {'label': '2005', 'style': {'color': colors['title']}},
          2006: {'label': '2006', 'style': {'color': colors['title']}},
          2007: {'label': '2007', 'style': {'color': colors['title']}},
          2008: {'label': '2008', 'style': {'color': colors['title']}},
          2009: {'label': '2009', 'style': {'color': colors['title']}},
          2010: {'label': '2010', 'style': {'color': colors['title']}},
          2011: {'label': '2011', 'style': {'color': colors['title']}},
          2012: {'label': '2012', 'style': {'color': colors['title']}},
          2013: {'label': '2013', 'style': {'color': colors['title']}},
          2014: {'label': '2014', 'style': {'color': colors['title']}},
          2015: {'label': '2015', 'style': {'color': colors['title']}},
        }
    )], style={'margin-left': '10%','margin-right':'10%'}) ,

    html.Br(), html.Br(), html.Br(),
    ], className='left'),

    #---- RIGHT PANEL
    html.Div([
    dcc.Dropdown(
        id = 'multi_country_selection',
        options=options,
        value=['Portugal'],
        multi=True
    ),
    html.Div([
        dcc.Graph(id="multi_suicide_number"),
    ]),
    ], className='right'),

    ], className='parent'),


    html.Div([
        html.H1('Country Information')
        ], className='subTitle', style={


    }),

    #---- Country Information Dropdowns
    html.Div([
        html.Div([
        dcc.Dropdown(
            id = 'dropdown-country',
            className= 'dropdown_style',
            options=options,
            value = '',
            placeholder='Country'
        ),
        ], style={'width':'20%' , 'margin-left': '5%' , 'float':'left'}),


        html.Div([
            dcc.Dropdown(
                id = 'dropdown-years',
                placeholder = 'Years',
                options=years,
                className= 'dropdown_style',
                value=''
            )
        ], style= {'display': 'block' , 'margin-left': '2%' , 'width':'20%' , 'float':'left'}
        )
    ], style={'width':'80%'}),
     html.Br(), html.Br(),

    #---- Country Information
    html.Div([
        html.Div([
           html.P('Country Population :' , className='reference')  ,
           html.P(  id='country_population', className='information')  ,
        ],style={'display':'flex'}) ,
        html.Div([
           html.P('Country GDP Per Capita ($): ' , className='reference')  ,
           html.P(id='country_gdp' , className='information' )  ,
        ],style={'display':'flex'}) ,
    ],id='information_div' , style={'display': 'none' }) ,


    html.Br(), html.Br(), html.Br(),

    #--- AGE AND GENDER PLOTS
    html.Div([
    html.Div([
        dcc.Graph(id="age_plot"),
    ], className='right'),
    html.Div([
        dcc.Graph(id="gender_pie")
    ], className='right'),
    ],id='hided_plots' ),

    html.Br(), html.Br(), html.Br(),

    #--- FOOTER
    html.Div([
    html.P('Application developed by João Francisco Ribeiro'),
    html.A('Used dataset can be found here', href='https://www.kaggle.com/russellyates88/suicide-rates-overview-1985-to-2016' , target='_blank' ),
    ],style={'textAlign': 'center'}),

    html.Br(),
    ],className='fullscreen')


# ----------------------- CALLBACK FUNCTIONS

@app.callback(
    Output(component_id='country_population', component_property='children'),
    Output(component_id='country_gdp' ,component_property='children'),
    Output(component_id='information_div' , component_property='style'),
    Output(component_id='hided_plots' , component_property='style'),
    [Input(component_id='dropdown-years', component_property='value'),
     Input(component_id='dropdown-country', component_property='value')])
def update_country_info(year,country):

    if year != '' and country != '':
        pop = df_europe_country_year_grouped.loc[ (df_europe_country_year_grouped.year == year) & (df_europe_country_year_grouped.country == country)]['population'].astype(str).iloc[0]
        gdp = df_europe.loc[ (df_europe.year == year) & (df_europe.country == country)]['gdp_per_capita ($)'].astype(str).iloc[0]
        return pop , gdp , {'display': 'block' }  , {'display': 'block', 'display': 'flex', 'justify-content': 'space-around' }
    else:
        return '','', {'display': 'none' } , {'display': 'none' } 

@app.callback(
    Output('multi_suicide_number' , "figure"),
    [Input(component_id='multi_country_selection', component_property='value')])
def suicides_number_per_country(countries):
    if len(countries) > 0 :
        map_df = df_europe_country_year_grouped.loc[(df_europe_country_year_grouped.country.isin(countries)) & (df_europe_country_year_grouped['year'] > 1999) & (df_europe_country_year_grouped['year'] < 2016)]

        fig = px.line(map_df, x='year', y='suicides_no', color='country' , labels={'suicides_no':'Number of Suicides ', 'year': 'Year ','country':'Country '})
        fig.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['title']
        )
        return fig
    else:
        fig = px.line()
        fig.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['title']
        )
        return fig


@app.callback(
    Output('europe_map' , "figure"),
    [Input(component_id='slider_date', component_property='value')])
def generate_map_europe(date_value):

    map_df = df_europe_country_year_grouped.loc[(df_europe_country_year_grouped.year == date_value) ]

    fig = px.choropleth(data_frame=map_df, locationmode='country names', labels={'suicides/100k_pop':'Suicides per 100K Habitants ' , 'country':'Country '}  , hover_data=['country'] , locations=map_df['country'], scope='europe' , color=map_df['suicides/100k_pop'],color_continuous_scale='orrd' )
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['title'],
        margin={"r":0,"t":0,"l":0,"b":0},
        geo=dict(bgcolor='rgba(0,0,0,0)')
    )


    return fig

#@app.callback(
#    Output(component_id='hided_plots', component_property='style'),
#    [Input(component_id='dropdown-years', component_property='value')])
#def show_2_graphs(year):

#    if year == '':
#        return  {'display': 'none' }
#    else:
 #       return {'display': 'block' ,  'display': 'flex' , 'justify-content': 'space-around'}

@app.callback(
    Output('age_plot' , "figure"),
    Output(component_id='age_plot', component_property='style') ,
    [Input(component_id='dropdown-years', component_property='value'),
     Input(component_id='dropdown-country', component_property='value')])
def generate_age_plot(dropdown_years , dropdown_country):

    if dropdown_years != '' and dropdown_country != '':
        dff = df_europe.loc[(df_europe.year==dropdown_years) & (df_europe.country==dropdown_country)]

        plot_age = px.bar(
            data_frame=dff,
            x=dff.age,
            y=dff.suicides_no,
            color=dff.sex,
            labels={'suicides_no':'Number of Suicides ', 'age': 'Age Group ','sex':'Gender '}
        )

        plot_age.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['title'],
            margin=dict(t=0, b=0, l=0, r=0),
            geo=dict(bgcolor='rgba(0,0,0,0)')
        )

        return plot_age  , {'display': 'block', 'width':'45%'}

    return px.pie() , {'display': 'none'}


@app.callback(
    Output('gender_pie' , "figure"),
    Output(component_id='gender_pie', component_property='style') ,
    [Input(component_id='dropdown-years', component_property='value'),
     Input(component_id='dropdown-country', component_property='value')])
def generate_gender_pie(dropdown_years , dropdown_country):

    if dropdown_years != '' and dropdown_country != '':
        dff = df_europe.loc[(df_europe.year==dropdown_years) & (df_europe.country==dropdown_country)].groupby(['country','year','sex'])[['suicides_no']].agg('sum').reset_index()

        piechart=px.pie(
            data_frame=dff,
            names=dff.sex,
            values=dff.suicides_no,
            hole=.3,
            labels={'suicides_no':'Number of Suicides ', 'age': 'Age Group ','sex':'Gender '} 
        )

        piechart.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['title'],

        )

        return piechart , {'display': 'block','width':'45%'}

    return px.pie() , {'display': 'none'}

@app.callback(
   Output(component_id='dropdown-years', component_property='style'),
   Output(component_id='dropdown-years', component_property='options'),
   [Input(component_id='dropdown-country', component_property='value')])
def show_hide_element(visibility_state):
    years.clear()
    if visibility_state != '':
        yearsFromDF = df_europe_country_year_grouped.loc[ (df_europe_country_year_grouped['country'] == visibility_state) & (df_europe_country_year_grouped['year'] > 1999) & (df_europe_country_year_grouped['year'] < 2016) ]['year']
        for i in yearsFromDF:
            years.append({'label': i, 'value': i})
        return {'display': 'block'} , years
    if visibility_state == '':
        return {'display': 'none'} , years




if __name__ == '__main__':
    app.run_server(debug=True)

