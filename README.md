# AQI_analysis

A project for Data Mining at San Jose State University.

Analyzing the AQI trend for different areas in United States from 2013 to 2023.

# Getting Started

## Data

The orignal data can be downloaded using this [link](https://aqs.epa.gov/aqsweb/airdata/download_files.html#Annual).

##  Packages

Using your favorite virtual environment, install the required packages using

```
pip install -r requirements.txt
```
# Dashboard
The dashboard is created in Google Looker Studio and it can connect directly to the BigQuery. The tool allows the stakeholders to interact with the data through dashboards and reports.

[AQI Analysis Dashboard](https://lookerstudio.google.com/reporting/bd0f226a-dc71-4aea-98ef-08cf99882120)

# Usage

Before running the following command, please get the data (`data.csv`) [here](https://drive.google.com/drive/u/0/folders/1a2SAtQaBHfKAMgpy2Z2GQUpNbJoPWSId
) and move it to the current folder: 

```
python3 dashboard.py
```

The app will be hosted on localhost. Head there to see the dashboard

# Roadmap
- [x] Data Acquisition and Processing
  - [x] Acquire the data from the site.
  - [x] Store the data on Google Cloud's Big Query.
- [x] EDA and Visualization
  - [x] Cleaning Data 
    - [x] Handle missing values.
    - [x] Handle outliers.
    - [x] Improve data consistency (fix typos and/or units of measurements).
    - [x] Remove non-relevant information.
    - [x] Quality check.
  - [x]  Exploring and visualizing data
    - [x] Get to know the data (types, dimensions, ...)
    - [x] Distributions 
    - [x] Relationships
    - [x] Patterns
  - [x] PCA  
- [x] Question/Problem Formulation
- [x] Data Modeling and Data App
- [ ] Dashboard App

The list will be updated accordingly throughout the development cycle.

# Explanation of baseline modules
- Data Ingestion and Preprocessing Module
  - In this module, it acts as the entry point for our data into the analysis pipeline, setting the foundation for accurate and meaningful insights. This module is responsible for importing the dataset from various sources like CSV files and performing initial preprocessing steps like cleaning, normalization, and transformation. We used Google Colab and pandas for manual data processing and transformation and save the processed dataframe to BigQuery.

- Analysis and Computation Module
  - This is the heart of the project and the most important module where we transform the raw data into actionable insights by uncovering patterns and trends in AQI and pollutant levels. In this module, we performed statistical analyses, trend detection and pollutant-specific evaluations. It would leverage the data science libraries to compute averages, trends, correlations and other statistical measures.

- Visualization Module
  -  This module mainly enhances the understanding and communication of the data analysis findings and allows the user to explore the trends and correlations in an intuitive manner. It enables the creation of interactive charts, graphs and maps to visually represent the analysis results. We implemented the time series plots of AQI trends for specific state or county, geographical heatmaps of pollutant concentrations and histograms or scatter plots for comparing different pollutants.
 
- Data Export and Reporting Module
  - In this module, we will facilitate the dissemination and sharing of findings with the stakeholders and provide a consolidated view of the analysis outcomes. We offer the capability to export the analyzed data and visualizations into reports and dashboards. For visualizing the data and generating reports, we used tools like Google Data Studio and PowerBI that can connect directly to BigQuery. These tools allow stakeholders to interact with the data through dashboards and reports.
    
# Challenges / Solutions
- Challenges Encountered:
  - Data Quality and Consistency:
     - Environmental datasets often suffer from inconsistencies, or errors due to the vast array of sources and collection methods which can complicate analysis and lead to inaccurate conclusions.
     - Many of our analyses rely in statistical measures found in the dataset like Median AQI and Days_CO among others. However, the number of analyzed days per year is different from counties to counties. This is a classic case of sample size mismatch. In other words, the statisical measures of counties with less sample size might be skewed, which, as mentioned, could lead to inaccurate conclusions.  
  - Complexity in Data Integration:
    - Integrating data from multiple years can be challenging especially when formats or measurement standards change over time.
  - Visualization Complexity:
    - Effectively visualizing environmental data, which might include multi-dimensional analyses and geographic information, requires sophisticated visualization tools that can be challenging to implement.

- Solutions to overcome challenges
  - Improving Data Quality and Consistency:
    - Implement robust data cleaning and preprocessing pipelines using automated scripts to identify and correct inconsistencies and fill in missing values where possible.
    - Use statistical methods or machine learning to impute missing data accurately.
  - Facilitating Data Integration:
    - Standardize data formats and units of measurement as part of the preprocessing stage to simplify integration.
  - Simplifying Visualization Complexity:
    - Utilizing PCA for dimensionality reduction.
    - Employ high-level visualization tools like PowerBI or Google Data Studio to abstract away some of the complexity.
    - Engage with end-users to understand their needs and preferences, designing intuitive and interactive visualizations based on user feedback.

# References
- [Data](https://aqs.epa.gov/aqsweb/airdata/download_files.html#Annual)



