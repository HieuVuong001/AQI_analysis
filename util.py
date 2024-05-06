import pandas as pd
from sklearn.decomposition import PCA

def preprocess(df):
    cond_1 = (df['Max_AQI'] <= 500)
    cond_2 = (df['90th_Percentile_AQI'] <= 500)
    cond_3 = (df['Median_AQI'] <= 500)

    df = df[cond_1 & cond_2 & cond_3]
    
    return df

def perform_PCA(df):
    # Choose numerical values in the dataset
    df_numeric = df.select_dtypes(include='number')
    df_numeric = df_numeric.drop(columns='Year')
    df_numeric

    # Fit PCA and reduce dimension to 2
    pca = PCA(n_components=2)
    pca.fit(df_numeric)

    # Add new PCA columns into df
    df_pca = pca.transform(df_numeric)
    df.insert(0, "PC1", df_pca[:, 0])
    df.insert(0, "PC2", df_pca[:, 1])

    # Create a categorical column for graphing
    df['Good_Percentage'] = df.loc[:, 'Good_Days'] / df.loc[:, 'Days_with_AQI']
    df['Overall_Quality'] = df['Good_Percentage'].apply(
        lambda x: 'Good' if x >= 0.80 else 'Bad'
    )

    return df
