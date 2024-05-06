from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# Import data
df = pd.read_csv('./data.csv', index_col=0)

# Use bootstrap for this app
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div('My First App with Data', className='text-primary text-center fs-3')
    ]),

    dbc.Row([
        dbc.RadioItems(
            options=[{"label": x, "value": x} for x in ['Days_CO', 'Median_AQI', 'Days_NO2']],
            value='Median_AQI',
            inline=True,
            id='radio-buttons-final'
        ),
    ]),
    
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                data=df.to_dict('records'), 
                page_size=10, 
                style_table={'overflowX': 'auto'}
            ),
        ], width=6),

        dbc.Col([
            dcc.Graph(
                figure={}, 
                id='my-first-graph-final')
            ], width=6)
        ])
], fluid=True)

# Add controls for interactions
@callback(
    Output(component_id='my-first-graph-final', component_property='figure'),
    Input(component_id='radio-buttons-final', component_property='value')
)

# Runs everytime another radio button is chosen
def update_graph(col_chosen):
    fig = px.histogram(df, x='State', y=col_chosen, histfunc='avg')
    return fig

if __name__ == '__main__':
    app.run(debug=True)