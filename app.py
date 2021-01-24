# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 07:44:49 2021

@author: syeds
"""

import os
import pandas as pd, numpy as np
import dash
import dash_core_components as dcc, dash_html_components as html
import flask
from datetime import date
from dash.dependencies import Output, Input
import plotly.graph_objects as go



current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir,'Data')

funds_dict = {"EBAF":"Edelweiss Balanced Advantage Fund",
              "ICICBAV":"ICICI Pru Balanced Advantage Fund",
              "ICICSF":"ICICI Savings Fund",
              "KLDF":"Kotak Low Duration Fund",
              "TBAF":"Tata Balanced Adv Fund",
              }
fund_description = {"EBAF":"__Edelweiss Balanced Advantage Fund__ :  Fund has __73.16%__ investment in __indian stocks__ of which __49.45%__ is in __large cap stocks__, __11.06%__ is in __mid cap stocks__, __4.42%__ in __small cap stocks__.Fund has __18.4%__ investment in __Debt__ of which __5.82%__ in __Government securities__, __12.58%__ in funds invested in __very low risk securities__..",
              "ICICBAV":"__ICICI Prudential Balanced Advantage Fund__ :   Fund has __65.88%__ investment in __indian stocks__ of which 50.57% is in large cap stocks, 6.44% is in mid cap stocks, 2.43% in small cap stocks.Fund has 25.88% investment in Debt of which 8.29% in Government securities, 16.13% in funds invested in very low risk securities..",
              "ICICSF":"""__ICICI Savings Fund__. Low Duration Fund : Fund has __87.3% __investment in__ Debt__ of which 41.29% in Government securities, 46.1% in funds invested in very low risk securities..
                          Suitable For : Investors who want to invest for __1-3 years__ and are looking for alternative to bank deposits.
                          Crisil Rank Change : Fund Crisil rank was updated from 3 to 4 in the previous quarter.""",
              "KLDF":"""__Kotak Low Duration Fund__ : __Low Duration Fund__ : Fund has __91.45%__ investment in __Debt__ of which 18.54% in Government securities, 72.14% in funds invested in very low risk securities..
                         Suitable For : Investors who want to invest for 1-3 years and are looking for alternative to bank deposits.""",
              "TBAF":"__Tata Balanced Adv Fund__ :  Fund has __66.5%__ investment in __indian stocks__ of which 49.96% is in large cap stocks, 9.09% is in mid cap stocks, 4.1% in small cap stocks.Fund has 22.19% investment in Debt of which 4.26% in Government securities, 17.93% in funds invested in very low risk securities..",
              }

AllMutualFunds = pd.DataFrame()
for file in os.listdir(data_dir):
    # break
    fileName = file.split(".")[0]
    fileData = pd.read_excel(os.path.join(data_dir,file), engine='openpyxl')
    fileData = fileData[::-1].reset_index(drop=True)
    # fileData['NAV Date'] = fileData['NAV Date'].astype('datetime64[ns]')
    fileData['NAV Date'] = pd.to_datetime(fileData['NAV Date'],format="%d-%m-%Y")
    fileData.set_index('NAV Date',inplace=True)
    fileData.columns = [fileName]
    AllMutualFunds = pd.concat([AllMutualFunds,fileData],axis=1)
AllMutualFunds.fillna(method = 'ffill',inplace=True)   
# AllMutualFunds.dropna()  




# df = pd.read_html('https://www.moneycontrol.com/mutual-funds/tata-balanced-advantage-fund-regular-plan/portfolio-holdings/MTA1346')[2]
# df = df[['Stock Invested in','Sector','% of Total Holdings','1M Change']]
AllMutualFunds_Returns = AllMutualFunds.pct_change()
AllMutualFunds_Returns.fillna(-1,inplace=True)

AllMutualFunds_wts = AllMutualFunds_Returns.apply(lambda x: [0 if i==-1 else 1 for i in x])
AllMutualFunds_wts = AllMutualFunds_wts.apply(lambda x:x/sum(x),axis=1)

Portfolio_returns = (AllMutualFunds_Returns*AllMutualFunds_wts).sum(axis=1)


# asd

flask_app = flask.Flask(__name__)
bootstrapcss = ['https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css',
               ]
app = dash.Dash(__name__,external_stylesheets = bootstrapcss,server=flask_app, suppress_callback_exceptions=True)
app.title = "MutualFund - Allocation"

app.layout = html.Div(children = [
html.Div(className = "text-center p-3 mb-2 bg-dark text-white",children = [
        html.H1(className = ".text-secondary display-2 ",children = [
            'Mutual Fund - Allocation'
            ]),
        html.P(children = ["Analysis Done for ",html.Mark("Mr. Abdul Aziz Khan.")])
        
        ]),    
html.Div([    
    
    
    html.Div(className = "text-center p-3 mb-2",children = [
        html.Blockquote(className = "blockquote text-center",children = [
            html.P(className = "mb-0", children = """A mutual fund can do for you
                   what you would do for yourself if you had sufficient time, training and money
                   to diversify, plus the temperament to stand back from your money and make rational decisions.
                   """),
                   html.Br(),
           html.Footer(className = "blockquote-footer", children="Venita VanCaspel")
            ])
        ]),
    html.Div(className = "text-center d-inline", children = [
        html.Article(children = [
            html.H3(className = "p-3",children = "INTERESTED MUTUAL FUNDS"),
            html.Article(className = "p-3 d-inline",children =[
                html.P(className = "p-3 mb-0 d-inline",children ="  Edelweiss Balanced Advantage Fund  "),
                html.P(className = "m-3 mb-1 d-inline",children ="  ICICI Pru Balanced Advantage Fund  "),
                html.P(className = "m-3 d-inline",children ="  ICICI Savings Fund  "),
                html.P(className = "m-3 d-inline",children ="  Kotak Low Duration Fund  "),
                html.P(className = "m-3 d-inline",children ="  Tata Balanced Adv Fund  "),
                ] )
            ]),
        
        html.Div(className = "p-2 text-center",children = [
            html.H3(className = "display-4 p-4", children = "Equal Allocation Portfolio Curve"),
            html.Label(htmlFor = "portfolio-daterange",className = "col-sm-2 col",
                       children = ["Please select the ",html.Mark("Date Range :")]),
            dcc.DatePickerRange(
                id='portfolio-daterange',
                min_date_allowed=date(2003,1,1),
                max_date_allowed=date(2021, 1, 1),
                start_date=date(2015,1,1),
                end_date=date(2021, 1, 1)
            ),
            html.Div(className = "w-100 justify-content-center text-center",children = dcc.Graph(className = "p-5 d-inline-block",id="portfolio-curve"))
            
            ])
        
        
        ]),
    html.Div(className ="justify-content-center text-center",children = [
        html.H4(className = "display-4 p-4", children ="Individual Fund Portfolio Curve"),
        dcc.Tabs(id='indv-funds-tabs',className = "custom-tabs-container",parent_className='custom-tabs', value='EBAF', children=
            [dcc.Tab(className='custom-tab',selected_className='custom-tab--selected',label=j, value=i) for i,j in funds_dict.items()]
    ),
        html.Div(id="indv-curves",className="w-100")
        
        ])
  
    ],className = "m-5")
    ])
               
                   
@app.callback(Output("portfolio-curve","figure"),
              [Input("portfolio-daterange","start_date"),
              Input("portfolio-daterange","end_date")])
def update_portfolio_curve(start_date,end_date):
    
    Portfolio_returns_period = Portfolio_returns.copy()
    Portfolio_returns_period = Portfolio_returns_period.loc[start_date:end_date]
    #inside callback
    Portfolio_returns_period = Portfolio_returns_period+1
    Portfolio_returns_period = Portfolio_returns_period.cumprod()
    
    Portfolio_returns_period = Portfolio_returns_period*100
    
    y_label_val = Portfolio_returns_period.iloc[-1]
    y_label_val = round(y_label_val,2)
    
    Portfolio_returns_period_returns = (Portfolio_returns_period.iloc[-1]-Portfolio_returns_period.iloc[0])/Portfolio_returns_period.iloc[0]
    Portfolio_returns_period_returns = Portfolio_returns_period_returns*100
    Portfolio_returns_period_returns = round(Portfolio_returns_period_returns,2)
    
    Portfolio_returns_period_returns = str(Portfolio_returns_period_returns)+"%"
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Portfolio_returns_period.index, y=Portfolio_returns_period,
                    mode='lines',
                    line=dict(color='rgb(67,67,67)', width=4),
                    name='Portfolio Curve'))
    fig.update_layout(
        title = f"100 invested would become {round(Portfolio_returns_period.iloc[-1],2)} with Equal Allocation, Returns : {Portfolio_returns_period_returns}",
        xaxis=dict(
            title = "Date",
        showline=True,
        showgrid=True,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=20,
            color='rgb(82, 82, 82)',
        ),
    ),
    # yaxis=dict(
    #     showgrid=True,
    #     zeroline=False,
    #     showline=False,
    #     showticklabels=False,
    # ),
    autosize=False,
    margin=dict(
        autoexpand=False,
        l=80,
        r=80,
        t=100,
    ),
    showlegend=False,
    plot_bgcolor='white'
        )
    annotations = []
    annotations.append(dict(xref='paper', x=0.95, y=y_label_val+1,
                                  xanchor='left', yanchor='middle',
                                  text='{}'.format(y_label_val),
                                  font=dict(family='Arial',
                                            size=20),
                                  showarrow=False))
    annotations.append(dict(xref='paper', x=0.05, y=100,
                                  xanchor='left', yanchor='middle',
                                  text='{}'.format(100),
                                  font=dict(family='Arial',
                                            size=20),
                                  showarrow=False))
    fig.update_layout(annotations=annotations,
                       paper_bgcolor="#DCDCDC",
        plot_bgcolor='#DCDCDC',
                     )
    
    return fig

@app.callback(Output('indv-curves', 'children'),
              Input('indv-funds-tabs', 'value'))
def render_content(tab):
    fundName =funds_dict[tab] 
    fund_returns = AllMutualFunds_Returns[fundName.replace(" ","_")].copy()
    fund_returns = fund_returns.loc['2015':]
    fund_returns = fund_returns.loc[~(fund_returns==-1)]
    fund_returns = fund_returns+1
    fund_returns = fund_returns.cumprod()
    
    fund_returns = fund_returns*100
    
    y_label_val = fund_returns.iloc[-1]
    y_label_val = round(y_label_val,2)
    
    fund_period_returns = (fund_returns.iloc[-1]-fund_returns.iloc[0])/fund_returns.iloc[0]
    fund_period_returns = fund_period_returns*100
    fund_period_returns = round(fund_period_returns,2)
    
    fund_period_returns = str(fund_period_returns)+"%"
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fund_returns.index, y=fund_returns,
                    mode='lines',
                    line=dict(color='rgb(67,67,67)', width=4),
                    name=fundName+' Portfolio Curve'))
    fig.update_layout(
        title = f"100 invested would become {round(fund_returns.iloc[-1],2)} with Equal Allocation, Returns : {fund_period_returns}",
        xaxis=dict(
            title = "Date",
        showline=True,
        showgrid=True,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=20,
            color='rgb(82, 82, 82)',
        ),
        # paper_bgcolor="#C2CFDC",
        # plot_bgcolor='#C2CFDC'
    ),
    # yaxis=dict(
    #     showgrid=True,
    #     zeroline=False,
    #     showline=False,
    #     showticklabels=False,
    # ),
    autosize=False,
    # margin=dict(
    #     autoexpand=False,
    #     l=0,
    #     r=200,
    #     t=100,
    # ),
    showlegend=False,
    plot_bgcolor='white'
        )
    annotations = []
    annotations.append(dict(xref='paper', x=0.95, y=y_label_val+10,
                                  xanchor='left', yanchor='middle',
                                  text='{}'.format(y_label_val),
                                  font=dict(family='Arial',
                                            size=20),
                                  showarrow=False))
    annotations.append(dict(xref='paper', x=0.05, y=100-10,
                                  xanchor='left', yanchor='middle',
                                  text='{}'.format(100),
                                  font=dict(family='Arial',
                                            size=20),
                                  showarrow=False))
    fig.update_layout(annotations=annotations,
                       paper_bgcolor="#DCDCDC",
                       plot_bgcolor='#DCDCDC')
    
    
    return html.Div(children =[
        html.H3(className = "display-5 p-4",children = funds_dict[tab],style = {"font-size":"35px"}),
        
        html.Div(className = "d-inline-block",children=[
        dcc.Markdown(className = "d-inline-block w-30",children = fund_description[tab]),
        html.Div(children = dcc.Graph(className = "d-inline-block w-60",figure =fig )),
        ])
    ],className = ".bg-secondary")
   


if __name__ == "__main__":
    flask_app.run(debug=False)
















