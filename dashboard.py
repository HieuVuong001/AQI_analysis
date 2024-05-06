from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from util import preprocess, perform_PCA
# Import data
df = pd.read_csv('./data.csv', index_col=0)

df = preprocess(df)

# This fucntion modify df (adding new columns = PC1, PC2, Overall_Quality)
perform_PCA(df)

# Use bootstrap for this app
external_stylesheets = [dbc.themes.COSMO]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Components and variables
jumbotron = html.Div(
    dbc.Container(
        [
            html.H1("CMPE 255 - Data Mining / AQI Analysis", 
                    className="display-3, text-primary"),
            html.Ul(
                [
                    html.Li('Trung Hieu Vuong', className='text-secondary'),
                    html.Li('Baljot Singh', className='text-secondary'),
                    html.Li('Jefferey Ong', className='text-secondary')
                ]
                ),
            html.Hr(className="my-2"),
        ],
        fluid=True,
        className="py-3",
    ),
    className="h-100 p-3 bg-light rounded-3",
)

PCA_jumbotron = html.Div(
        [
            html.H2("PCA", className="display-3 text-center"),
            html.Hr(className="my-2"),
            html.P(
                """
                PCA reduces the dimension of the original down to 2,
                which give us this beautiful graph. We can see that 
                the higher Principle Component 1 is, the lesser the 
                overall quality. 
                """
            ),
        ],
        className="h-100 bg-none text-dark border rounded-3",
    )

# Selection for radio buttons
pm_radio_selections = ['Days_CO', 'Days_NO2', 'Days_Ozone', 'Days_PM2_5', 'Days_PM10']
days_radio_selections = ['Good_Days', 'Moderate_Days', 
                         'Unhealthy_for_Sensitive_Groups_Days',
                         'Unhealthy_Days',
                         'Very_Unhealthy_Days',
                         'Hazardous_Days']
# Layout
app.layout = dbc.Container([
    dbc.Row([
        jumbotron
    ]),

    dbc.Row([
        html.H2('Data Table', className='text-secondary text-center'),
        dash_table.DataTable(
                data=df.to_dict('records'), 
                page_size=10, 
                style_table={'overflowX': 'auto'},
                sort_action='native',
            ),
    ]),

    html.Hr(),
    
    dbc.Row([
        html.H2('Median AQI Over the Years', className='text-secondary text-center'),

        dbc.Col([
            dbc.Label("Toggle States"),
            dbc.Checklist(
                options=[
                    {"label": state, "value": state} for state in df['State'].unique()
                ],
                value=['California'],
                id="switches-input",
                switch=True,
                inline=True,
            )
        ], width=6),

        dbc.Col([
            dcc.Graph(
                figure={}, 
                id='state-graph')
            ], width=6)
        ]),
    
    html.Hr(),
    
    dbc.Row([
        html.H2('Average Particle Matters Different States', 
                className='text-secondary text-center'),
        dbc.RadioItems(
            options=[{"label": x, "value": x} for x in pm_radio_selections],
            value='Days_CO',
            inline=True,
            id='radio-buttons-pm'
        ),
    ]),

    dbc.Row([
        dcc.Graph(
            figure={},
            id='average-pm-graph',
        )
    ]), 

    html.Hr(),

    dbc.Row([
        html.H2('Distribution of Day Classification based on AQI'),

        dbc.RadioItems(
            options=[{"label": x, "value": x} for x in days_radio_selections],
            value='Good_Days',
            inline=True,
            id='radio-buttons-days'
        ),
        dcc.Graph(
            figure={},
            id='days-dist-graph'
        )
    ]),

    dbc.Row([
        html.H2('Principle Component Analysis', className='text-secondary text-center'),
        dbc.Col([
            html.H3('Advantages of PCA'),
            html.Ul(
                [
                    html.Li('Easy to graph 2D data'),
                    html.Li("""
                            Can give insights into what each Principle Component means
                            (here, PC2 might mean pollution as bad quality increases with it)
                            """)
                ]
            ),
            html.H3('Disadvantage of PCA'),
            html.Ul(
                html.Li('Some information can be lost through compression')
            )
        ], width=5),

        dbc.Col([
            dcc.Graph(
                figure={},
                id='PCA-graph'
            )
        ], width=7),
    ]), 


], fluid=True)

# Add controls for interactions
@callback(
    Output(component_id='average-pm-graph', component_property='figure'),
    Output(component_id='state-graph', component_property='figure'),
    Output(component_id='PCA-graph', component_property='figure'),
    Output(component_id='days-dist-graph', component_property='figure'),
    Input(component_id='radio-buttons-pm', component_property='value'),
    Input(component_id='switches-input', component_property='value'),
    Input(component_id='radio-buttons-days', component_property='value'),
)

# Runs everytime another radio button is chosen
def update_graph(col_chosen, switches_chosen, dist_col_chosen):
    # Choose chosen states and aggregate
    mask = df.State.isin(switches_chosen)
    subset = df[mask]
    subset = subset.groupby(['State', 'Year'], as_index=False).agg({'Median_AQI': 'median'})

    # Average PM graph
    avg_fig = px.histogram(df, x='State', y=col_chosen, histfunc='avg')

    # AQI lineplot over the year in given states
    line_AQI_fig = px.line(subset, x='Year', y='Median_AQI', color='State')

    PCA_fig = px.scatter(df, title='Dimesionality Reduction using PCA',
                         x='PC1', y='PC2', color='Overall_Quality')
    
    dist_fig = px.box(df, y=dist_col_chosen )

    return avg_fig, line_AQI_fig, PCA_fig, dist_fig

if __name__ == '__main__':
    app.run(debug=True)