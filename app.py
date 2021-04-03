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

#---------------------  BUILD APP LAYOUT
app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([

    html.Div([
        html.H1('SUICIDES IN EUROPE IN THE BEGGINING OF CENTURY XXI')
        ], className='Title'),


    html.Br(), html.Br(), html.Br(),

    html.Div([
            dcc.Graph(id="europe_map")
    ]),

    html.Br(),html.Br(),html.Br(),

    dcc.Slider(
        id='slider_date',
        min=2000,
        max=2015,
        step=1,
        value=2000,
        marks={
          2000: {'label': '2000', 'style': {'color': '#77b0b1'}},
          2001: {'label': '2001', 'style': {'color': '#77b0b1'}},
          2002: {'label': '2002', 'style': {'color': '#77b0b1'}},
          2003: {'label': '2003', 'style': {'color': '#77b0b1'}},
          2004: {'label': '2004', 'style': {'color': '#77b0b1'}},
          2005: {'label': '2005', 'style': {'color': '#77b0b1'}},
          2006: {'label': '2006', 'style': {'color': '#77b0b1'}},
          2007: {'label': '2007', 'style': {'color': '#77b0b1'}},
          2008: {'label': '2008', 'style': {'color': '#77b0b1'}},
          2009: {'label': '2009', 'style': {'color': '#77b0b1'}},
          2010: {'label': '2010', 'style': {'color': '#77b0b1'}},
          2011: {'label': '2011', 'style': {'color': '#77b0b1'}},
          2012: {'label': '2012', 'style': {'color': '#77b0b1'}},
          2013: {'label': '2013', 'style': {'color': '#77b0b1'}},
          2014: {'label': '2014', 'style': {'color': '#77b0b1'}},
          2015: {'label': '2015', 'style': {'color': '#77b0b1'}},
        }
    ) ,
    html.Br(), html.Br(), html.Br(),

    dcc.Dropdown(
        id = 'multi_country_selection',
        options=options,
        value=['Portugal'],
        multi=True
    ) ,

    html.Div([
        dcc.Graph(id="multi_suicide_number"),
    ]),


    html.Div([
        dcc.Dropdown(
            id = 'dropdown-country',
            options=options,
            value = '',
            placeholder='Country'
        ),
        html.Br(),
        # Create Div to place a conditionally visible element inside
        html.Div([
        # Create element to hide/show, in this case an 'Input Component'
            dcc.Dropdown(
                id = 'dropdown-years',
                placeholder = 'Years',
                options=years,
                value=''
            )
        ], style= {'display': 'block'} # <-- This is the line that will be changed by the dropdown callback
        )
    ]),

    html.Div([
        dcc.Graph(id="age_plot"),
        dcc.Graph(id="gender_pie")
    ],id='hided_plots' , style={'display': 'none'})


    ])


# ----------------------- CALLBACK FUNCTIONS

@app.callback(
    Output('multi_suicide_number' , "figure"),
    [Input(component_id='multi_country_selection', component_property='value')])
def suicides_number_per_country(countries):
    if len(countries) > 0 :
        map_df = df_europe_country_year_grouped.loc[(df_europe_country_year_grouped.country.isin(countries)) & (df_europe_country_year_grouped['year'] > 1999) & (df_europe_country_year_grouped['year'] < 2016)]

        fig = px.line(map_df, x='year', y='suicides_no', color='country')
        return fig
    else:
        return px.line()


@app.callback(
    Output('europe_map' , "figure"),
    [Input(component_id='slider_date', component_property='value')])
def generate_map_europe(date_value):

    map_df = df_europe_country_year_grouped.loc[(df_europe_country_year_grouped.year == date_value) ]

    fig = px.choropleth(data_frame=map_df, locationmode='country names', hover_data=['country'] , locations=map_df['country'], scope='europe' , color=map_df['suicides/100k_pop'],color_continuous_scale='Viridis' )



    return fig

@app.callback(
    Output(component_id='hided_plots', component_property='style'),
    [Input(component_id='dropdown-years', component_property='value')])
def show_2_graphs(year):

    if year == '':
        return  {'display': 'none'}
    else:
        return {'display': 'block'}

@app.callback(
    Output('age_plot' , "figure"),
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
        )

        return plot_age

    return px.pie()


@app.callback(
    Output('gender_pie' , "figure"),
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
        )

        return piechart

    return px.pie()

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

