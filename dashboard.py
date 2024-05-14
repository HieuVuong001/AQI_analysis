from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

from plotly import graph_objects as go

from util import preprocess, perform_PCA

df = pd.read_csv('./data.csv', index_col=0)
df = preprocess(df)

perform_PCA(df)
# Use a Bootstrap theme for the app
external_stylesheets = [dbc.themes.COSMO]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Navbar
navbar = dbc.NavbarSimple(
    brand="AQI Analysis Dashboard",
    color="dark",
    dark=True,
    fluid=True,
    className="mb-4"
)

# Header Jumbotron 
jumbotron = html.Div(
    dbc.Container(
        [
            html.H1("CMPE 255 - AQI Analysis", className="display-4 mb-3 text-white"),
            html.Hr(className="my-2"),
            html.P("Explore and analyze AQI data using various visualization techniques.",
                   className="lead text-white"),
        ],
        fluid=True,
        className="py-4",
    ),
    className="p-4 border rounded-3 mb-4",
    style={
        "background": "linear-gradient(to right, #4A90E2, #00ADEF)",  
        "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.2)",
        "border": "1px solid #4A90E2",  
    },
)

# Data Table
data_table_section = html.Div(
    [
        html.H2('Data Table', className='text-center my-3'),
        dash_table.DataTable(
            data=df.to_dict('records'),
            page_size=10,
            style_table={'overflowX': 'auto'},
            sort_action='native',
        ),
    ],
    className="my-4",
)

# Median AQI Over the Years
median_aqi_section = html.Div(
    [
        html.H2('Median AQI Over the Years', className='text-center my-3'),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Toggle States"),
                        dbc.Checklist(
                            options=[{"label": state, "value": state} for state in df['State'].unique()],
                            value=['California'],
                            id="switches-input",
                            switch=True,
                            inline=True,
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    dcc.Graph(figure={}, id='state-graph'),
                    width=6,
                ),
            ],
        ),
    ],
    className="my-4",
)

# Average Particle Matters Different States
pm_section = html.Div(
    [
        html.H2('Average Particle Matters Across Different States', className='text-center my-3'),
        dbc.RadioItems(
            options=[{"label": x, "value": x} for x in ['Days_CO', 'Days_NO2', 'Days_Ozone', 'Days_PM2_5', 'Days_PM10']],
            value='Days_CO',
            inline=True,
            id='radio-buttons-pm',
        ),
        dcc.Graph(figure={}, id='average-pm-graph'),
    ],
    className="my-4",
)

# Distribution of Day Classification
days_distribution_section = html.Div(
    [
        html.H2('Distribution of Day Classification Based on AQI', className='text-center my-3'),
        dbc.RadioItems(
            options=[{"label": x, "value": x} for x in ['Good_Days', 'Moderate_Days', 'Unhealthy_for_Sensitive_Groups_Days',
                                                        'Unhealthy_Days', 'Very_Unhealthy_Days', 'Hazardous_Days']],
            value='Good_Days',
            inline=True,
            id='radio-buttons-days',
        ),
        dcc.Graph(figure={}, id='days-dist-graph'),
    ],
    className="my-4",
)

# PCA Section
pca_section = html.Div(
    [
        html.H2('Principal Component Analysis (PCA)', className='text-center my-3'),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3('Advantages of PCA'),
                        html.Ul(
                            [
                                html.Li('Easy to visualize data in 2D.'),
                                html.Li("""
                                    Can provide insights into what each Principal Component represents.
                                    Here, PC2 might correlate with pollution as higher PC2 suggests lower quality.
                                    """),
                            ]
                        ),
                        html.H3('Disadvantages of PCA'),
                        html.Ul([html.Li('Some information can be lost due to compression.')]),
                    ],
                    width=4,
                ),
                dbc.Col(
                    dcc.Graph(figure={}, id='PCA-graph'),
                    width=8,
                ),
            ],
        ),
    ],
    className="my-4",
)

def avg_median_aqi():
    # Calculating the average Median AQI for each state
    average_aqi_by_county = df.groupby('State')['Median_AQI'].mean().sort_values()
    average_aqi_by_county_df = average_aqi_by_county.reset_index().rename(columns={'Median_AQI': 'Average Median AQI'})
    
    # Create the bar chart
    fig = px.bar(average_aqi_by_county_df, x='State', y='Average Median AQI',
                 labels={'Average Median AQI': 'Average Median AQI', 'State': 'State'},
                 color='Average Median AQI',
                 color_continuous_scale='Viridis',
                 title='Average Median AQI Across Different States')
    fig.update_layout(xaxis={'categoryorder': 'total ascending'}, xaxis_title='State', yaxis_title='Average Median AQI')
    fig.update_xaxes(tickangle=45)
    
    return fig

# Average Median AQI Across Different States
median_aqi_trend_section = html.Div(
    [
        html.H2('Average Median AQI Across Different States', className='text-center my-3'),
        dcc.Graph(figure=avg_median_aqi(), id='bar-chart'),
    ],
    className="my-4",
)

def create_aqi_distribution_chart():
    # Import or recreate the dataset
    df['Year'] = df['Year'].astype(str)
    
    # Aggregate the data to get total days in each AQI category per year
    aqi_categories = ['Good_Days', 'Moderate_Days', 'Unhealthy_for_Sensitive_Groups_Days', 'Unhealthy_Days', 'Very_Unhealthy_Days', 'Hazardous_Days']
    total_days_by_category_and_year = df.groupby('Year')[aqi_categories].sum()
    
    # Transpose for easier plotting
    total_days_transposed = total_days_by_category_and_year.T
    
    # Convert to long format for bar plotting
    df_long = total_days_transposed.reset_index().melt(id_vars='index', value_vars=total_days_transposed.columns, var_name='Year', value_name='Total Days')
    df_long.rename(columns={'index': 'AQI Category'}, inplace=True)
    
    # Create the bar chart
    fig = px.bar(df_long, x='AQI Category', y='Total Days', color='Year', barmode='group',
                 title='Comparison of AQI Category Distribution Across Different Years')
    fig.update_layout(xaxis_title='AQI Category', yaxis_title='Total Days', xaxis={'categoryorder': 'total descending'}, legend_title='Year')
    fig.update_xaxes(tickangle=45)
    
    return fig

# Comparison of AQI Category Distribution Across Different Years
aqi_distribution_section = html.Div(
    [
        html.H2('Comparison of AQI Category Distribution Across Different Years', className='text-center my-3'),
        dcc.Graph(figure=create_aqi_distribution_chart(), id='aqi-distribution-graph'),
    ],
    className="my-4",
)

# Function to generate the AQI distribution by county graph
def create_aqi_days_by_county_chart():
    # Aggregate data by county and AQI categories
    categories_of_interest = ['Good_Days', 'Moderate_Days', 'Unhealthy_for_Sensitive_Groups_Days', 'Unhealthy_Days', 'Very_Unhealthy_Days', 'Hazardous_Days']
    county_aqi_days = df.groupby('County')[categories_of_interest].sum()
    
    df_long = county_aqi_days.reset_index().melt(id_vars=['County'], value_vars=categories_of_interest, var_name='AQI Category', value_name='Total Days')
    counties = df_long['County'].unique()
    
    fig = go.Figure()
    
    for county in counties:
        subset = df_long[df_long['County'] == county]
        trace = go.Bar(
            x=subset['Total Days'],
            y=subset['AQI Category'],
            name=county,
            orientation='h',
            hoverinfo='text',
            text=subset.apply(lambda row: f"County: {row['County']}<br>AQI Category: {row['AQI Category']}<br>Total Days: {row['Total Days']}", axis=1)
        )
        fig.add_trace(trace)
    
    fig.data[0].visible = True
    
    # Create steps for the slider
    steps = []
    for i, county in enumerate(counties):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)},
                  {"title": f"Distribution of AQI Days by {county}"}],
            label=county)
        step["args"][0]["visible"][i] = True
        steps.append(step)
    
    sliders = [dict(
        active=0,
        currentvalue={"prefix": "County: "},
        pad={"t": 50},
        steps=steps
    )]
    
    fig.update_layout(
        sliders=sliders,
        title="Distribution of AQI Days by County Selection",
        xaxis_title="Total Days",
        yaxis_title="AQI Category",
        height=600,
        width=1000
    )
    
    return fig

# Create a new section for the county AQI distribution graph
county_aqi_days_section = html.Div(
    [
        html.H2('Distribution of AQI Days by County', className='text-center my-3'),
        dcc.Graph(figure=create_aqi_days_by_county_chart(), id='county-aqi-graph'),
    ],
    className="my-4",
)


AQI_map = html.Div(
    [
        html.H1('Map of Median AQI in the United States', className='text-center'),
        html.Iframe(src="https://www.google.com/maps/d/embed?mid=1MxO7WEcaoCNLPdGaXYSI3Del_lwdex4&ehbc=2E312F", width="100%", height="480", className='center'),
    ],
    className="my-4",
)

# Overall App Layout
app.layout = html.Div(
    [
        navbar,
        dbc.Container(
            [
                jumbotron,
                data_table_section,
                median_aqi_trend_section,
                median_aqi_section,
                pm_section,
                days_distribution_section,
                aqi_distribution_section,
                county_aqi_days_section,
                pca_section,
                AQI_map,
            ],
            fluid=True,
        ),
    ],
)

# Add controls for interactions
@callback(
    [
        Output('average-pm-graph', 'figure'),
        Output('state-graph', 'figure'),
        Output('PCA-graph', 'figure'),
        Output('days-dist-graph', 'figure'),
    ],
    [
        Input('radio-buttons-pm', 'value'),
        Input('switches-input', 'value'),
        Input('radio-buttons-days', 'value'),
    ],
)
def update_graph(col_chosen, switches_chosen, dist_col_chosen):
    # Filter by chosen states and aggregate data
    mask = df.State.isin(switches_chosen)
    subset = df[mask].groupby(['State', 'Year'], as_index=False).agg({'Median_AQI': 'median'})

    # Create plots
    avg_fig = px.histogram(df, x='State', y=col_chosen, histfunc='avg')
    line_aqi_fig = px.line(subset, x='Year', y='Median_AQI', color='State')
    pca_fig = px.scatter(df, title='Dimensionality Reduction using PCA', x='PC1', y='PC2', color='Overall_Quality')
    dist_fig = px.box(df, y=dist_col_chosen)

    return avg_fig, line_aqi_fig, pca_fig, dist_fig

if __name__ == '__main__':
    app.run(debug=False)