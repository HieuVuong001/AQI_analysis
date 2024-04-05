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
# Usage

To be updated...

# Roadmap
- [x] Data Acquisition and Processing
  - [x] Acquire the data from the site.
  - [x] Store the data on Google Cloud's Big Query.
- [ ] EDA and Visualization (<ins>Ongoing</ins>)
  - [ ] Cleaning Data 
    - [x] Handle missing values.
    - [ ] Handle outliers.
    - [ ] Improve data consistency (fix typos and/or units of measurements).
    - [ ] Remove non-relevant information.
    - [ ] Quality check.
  - [ ]  Exploring and visualizing data
    - [ ] Get to know the data (types, dimensions, ...)
    - [ ] Distributions 
    - [ ] Relationships
    - [ ] Patterns 
- [ ] Question/Problem Formulation
- [ ] Data Modeling and Data App

The list will be updated accordingly throughout the development cycle.

# Explanation of baseline modules
- Data Ingestion and Preprocessing Module
  - In this module, it acts as the entry point for our data into the analysis pipeline, setting the foundation for accurate and meaningful insights. This module is responsible for importing the dataset from various sources like CSV files and performing initial preprocessing steps like cleaning, normalization, and transformation. We used Google Colab and pandas for manual data processing and transformation and save the processed dataframe to BigQuery.

To be updated.

# Challenges / Solutions

To be updated.

# References
- [Data](https://aqs.epa.gov/aqsweb/airdata/download_files.html#Annual)




