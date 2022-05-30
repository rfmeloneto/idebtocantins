from turtle import width
from dash import Dash, dcc, html, Input, Output
from filelock import annotations
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

df_linha_ai = pd.read_csv('df_linha_ai.csv')
df_linha_af=pd.read_csv('linha_af.csv')
df_linha_em= pd.read_csv('linha_em.csv')
df= pd.read_csv('idebestados.csv')
df_estados_af = pd.read_csv('idebestadosaf_final.csv')
df_estados_em = pd.read_csv('idebestadosem_final.csv')
df_escolas_em = pd.read_csv('idebescolas_em.csv')
df_escolas_ai= pd.read_csv('escolas_ai.csv')
df_escolas_af= pd.read_csv('escolas_af.csv')


app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Ideb Tocantins'


navbar = dbc.NavbarSimple(
    
    brand="Secretaria de Educação do Estado do Tocantins- Painel Ideb",
    color="primary",
    dark=True,
    
)

app.layout = html.Div([

    navbar,

    dbc.Toast(children=[
        dbc.Row( children=[
            dcc.Dropdown(options=df_estados_af['Estado'].unique(),value='Tocantins', id='lista_estados'),
            dbc.Col( children=[
            html.H6('Ideb Ensino Fundamental Anos Iniciais' , style={'margin-left':160 , 'margin-top':25 }),
            dcc.Graph(id='fig_linha_ai', config={"displaylogo": False})]),
            dbc.Col( children = [
            html.H6('Ideb Ensino Fundamental Anos finais', style={'margin-left':160, 'margin-top':25}),
            dcc.Graph(id='fig_linha_af', config={"displaylogo": False})]),
        ]),
        dbc.Row( children =[

            html.H6('Ideb Ensino Médio', style={'margin-left':550}),
            dcc.Graph(id='fig_linha_em')])

     ],style={'width': 1300}),

    html.Br(),

    dbc.Toast(children=[
    dbc.Row(dbc.Col(html.H4('Ideb - Comparativo Estados - Anos Iniciais'), width={'offset':4})),
    dcc.Graph(id='ideb-anos-slider', config={"displaylogo": False}),
    dcc.Slider(
        2005,
        2019,
        step=None,
        value=2005,
        marks= {2005:'2005',2007:'2007',2009:'2009',2011:'2011',2013:'2013',2015:'2015', 2017:'2017',2019:'2019'},
        id='ano-slider'
    )], style={'width': 1300}),

    html.Br(),
    dbc.Toast(children=[
    dbc.Row(dbc.Col(html.H4('Ideb - Comparativo Estados - Anos Finais'), width={'offset':4})),

    dcc.Graph(id='ideb-anos-finais-slider', config={"displaylogo": False}),
    dcc.Slider(
        2005,
        2019,
        step=None,
        value=2005,
        marks= {2005:'2005',2007:'2007',2009:'2009',2011:'2011',2013:'2013',2015:'2015', 2017:'2017',2019:'2019'},
        id='ano-finais-slider'
    )],style={'width': 1300}),

    html.Br(),
    dbc.Toast(children =[
    dbc.Row(dbc.Col(html.H4('Ideb - Comparativo Estados - Ensino Médio'), width={'offset':4})),
    dcc.Graph(id='ideb-em-slider', config={"displaylogo": False}),
    dcc.Slider(
        2005,
        2019,
        step=None,
        value=2005,
        marks= {2005:'2005',2007:'2007',2009:'2009',2011:'2011',2013:'2013',2015:'2015', 2017:'2017',2019:'2019'},
        id='ano-em-slider'
    )], style={'width': 1300}) ,

    html.Br(),

    dbc.Row(dbc.Col(html.H4('Ideb das Escolas Estaduais'), width={'offset':5})),
    dbc.Row(dbc.Col(html.H6('Caso o gráfico apareça vazio, significa que o Município não participou do Ideb no ano'), width={'offset':3})),
    html.Div(
        children= [
            dcc.Dropdown(options={'2017':2017, '2019' : 2019}, style=dict(width='50%'), id='ano_em', value='2017'),
            dcc.Dropdown(df_escolas_em['Cod Cid'].unique(), style=dict(width='50%'), id='município_em', value ='Palmas'),
        ],style=dict(display='flex')),
        html.Br(),
    dcc.Graph(id ='escolas_em', config={"displaylogo": False}),
    dcc.Dropdown(options={'2005':2005,'2007':2007,'2009':2009,'2011':2011,'2013':2013,'2015':2015, '2017':2017,'2019':2019}, id='escolas-ai-af', value='2005'),
    dcc.Graph(id ='escolas_ai', config={"displaylogo": False}),
    dcc.Graph(id='escolas-af', config={"displaylogo": False})


], className="p-3 bg-light rounded-3")

#----------------------------------------------------------------------------------------
@app.callback(

    Output('fig_linha_ai', 'figure'),
    Output('fig_linha_af', 'figure'),
    Output('fig_linha_em', 'figure'),
    Input('lista_estados','value')
)

def linhaestados(estado):
    
    fig1 = px.line(df_linha_ai, x ='Ano', y= estado)
    fig2 = px.line(df_linha_af, x = 'ano', y= estado)
    fig3 = px.line(df_linha_em, x = 'ano', y=estado)
    fig1.update_xaxes(type='category')
    fig2.update_xaxes(type='category')
    fig3.update_xaxes(type='category')

    return fig1 , fig2, fig3

@app.callback(
    Output('ideb-anos-slider', 'figure'),
    Input('ano-slider', 'value'))
def update_figure(ano):
    if ano == 2005:
        fig = px.scatter(df, x= str(ano), y= 'Estado', size= str(ano),symbol=df['Estado']=='Tocantins')
    else:
        fig = px.scatter(df, x= str(ano), y= 'Estado'  , color='meta'+str(ano), size= str(ano), symbol=df['Estado']=='Tocantins')

    fig.update_layout(transition_duration=500,showlegend=False)

    return fig


@app.callback(
    Output('ideb-anos-finais-slider', 'figure'),
    Input('ano-finais-slider', 'value'))
def update_figure(ano):
    if ano == 2005:
        fig = px.scatter(df_estados_af, x= str(ano), y= 'Estado', size= str(ano),symbol=df_estados_af['Estado']=='Tocantins')
    else:
        fig = px.scatter(df_estados_af, x= str(ano), y= 'Estado' , color='meta'+str(ano), size= str(ano), symbol=df_estados_af['Estado']=='Tocantins')

    fig.update_layout(transition_duration=500,showlegend=False)

    return fig

@app.callback(
    Output('ideb-em-slider', 'figure'),
    Input('ano-em-slider', 'value'))
def update_figure(ano):
    if ano == 2005:
        fig = px.scatter(df_estados_em, x= str(ano), y= 'Estado', size= str(ano),symbol=df_estados_em['Estado']=='Tocantins')
    else:
        fig = px.scatter(df_estados_em, x= str(ano), y= 'Estado' , color='meta'+str(ano), size= str(ano), symbol=df_estados_em['Estado']=='Tocantins')

    fig.update_layout(transition_duration=500,showlegend=False)

    return fig


@app.callback(
    Output('escolas_em', 'figure'),
    Input('ano_em','value'),
    Input('município_em','value')
)
def escolasEm(ano,muni):
    dfem = df_escolas_em.loc[df_escolas_em['Cod Cid']== muni]
    dfem.drop( dfem[dfem[str(ano)]==0 ].index, inplace=True)
    fig = px.bar(dfem, x= 'Escola' , y=str(ano),color = 'Escola', title= 'Nota do Ideb - Ensino Médio - ano ' + str(ano) + ' - Cidade: ' + str(muni))
    fig.update_layout(xaxis_visible=False, yaxis_title=None)
    return fig

@app.callback(
    Output('escolas_ai', 'figure'),
    Output('escolas-af', 'figure'),
    Input('escolas-ai-af','value'),
    Input('município_em','value')
)

def escolasFundamentais(ano,muni):
    dfem1 = df_escolas_ai.loc[df_escolas_ai['Cod Cid']== muni]
    dfem1.drop( dfem1[dfem1[str(ano)]==0 ].index, inplace=True)
    dfem2 = df_escolas_af.loc[df_escolas_af['Cod Cid']== muni]
    dfem2.drop( dfem2[dfem2[str(ano)]==0 ].index, inplace=True)
    fig = px.bar(dfem1, x='Escola' , y=str(ano),color = 'Escola', title= 'Nota do Ideb - Ensino Fundamental Anos Iniciais - ano ' + str(ano) + ' - Cidade: ' + str(muni))
    fig.update_layout(xaxis_visible=False, yaxis_title=None)
    fig2 = px.bar(dfem2, x='Escola' , y=str(ano),color = 'Escola', title= 'Nota do Ideb - Ensino Fundamental Anos Finais - ano ' + str(ano) + ' - Cidade: ' + str(muni))
    fig2.update_layout(xaxis_visible=False, yaxis_title=None)
    return fig , fig2




if __name__ == '__main__':
    app.run_server(debug=False)