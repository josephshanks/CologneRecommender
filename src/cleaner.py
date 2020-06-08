import pandas as pd
import numpy as np
import ast

def cleaner(df):
    
    #Initial clean of scraped dataframe
    df=df.drop(columns='Unnamed: 0')
    duplicates=df[df.duplicated('name')].index
    df=df.drop(duplicates)
    df=df.reset_index()
    df=df.drop(columns=['index'])
    
    for i in range(len(df.columns)):
        try:
            df.iloc[:,i]=df.iloc[:,i].apply(lambda x: ast.literal_eval(x))
        except:
            continue
    
    return df
