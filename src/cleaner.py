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
    
    #removes json string types
    for i in range(len(df.columns)):
        try:
            df.iloc[:,i]=df.iloc[:,i].apply(lambda x: ast.literal_eval(x))
        except:
            continue
    
    return df

def create_columns_from_dic(df,column):
    '''
    INPUT(dataframe, column(STRING) to unpack)
    OUTPUT(dataframe)
    
    This function unpacks a column containing dictionary types.
    Creates a new colulmn for each unique key in the dataframe and assigns a value
    '''
    
    data=[]
    for i in df[column]:
        for key in i.keys():
            data.append(key)
            
    #Check for loose data in dic caused from webscraping
    for idx,acc in enumerate(data):
        if acc == 'Pictures':
            data.pop(idx)
        if acc == 'Videos':
            data.pop(idx)
    #Unique key values
    x=set(data)
    data=list(x)
    #Assign new column for each unique key
    for d in data:
            df[d]=0
            
    #Assign value for each new column        
    for idx,i in enumerate(df[column]):
        for key,value in i.items():
            if key == 'Pictures':
                continue
            elif key == 'Videos':
                continue
            else:
                df[key].iloc[idx]=value
                
    #drop original column            
    df.drop(columns=column,inplace=True)
    
    return df

def notes_unpack(df):
    '''
    INPUT: dataframe containing columns: top notes,bottom notes, base notes
    OUTPUT: dataframe of new note columns with values 1 or 0
    '''
    
    all_notes=[]
    for notes in df['top notes']:
        for note in notes:
            all_notes.append(note)
    for notes in df['mid notes']:
        for note in notes:
            all_notes.append(note)
    for notes in df['base notes']:
        for note in notes:
            all_notes.append(note)
    
    #Create list of all notes in given fragrences
    an=set(all_notes)
    all_notes=list(an)
    
    #Assign new column to given df for each note, set value to 0
    for note in all_notes:
        df[note]=0
    
    top_notes = df['top notes']
    mid_notes= df['mid notes']
    base_notes= df['base notes']
    
    #Assign 1 if fragrence contains a note
    for idx,notes in enumerate(top_notes):
        for note in notes:
            df[note][idx]=1
    for idx,notes in enumerate(mid_notes):
        for note in notes:
            df[note][idx]=1
    for idx,notes in enumerate(base_notes):
        for note in notes:
            df[note][idx]=1
            
    #drop original column from df
    df.drop(columns=['top notes','mid notes','base notes'], inplace=True)
    
    return df


def rating_unpack(item_item):
    '''
    INPUT: dataframe containing ratings dictionary
    OUTPUT: dataframe with new columns and associated values for each fragrence
    '''
    
    #Assign new columns
    item_item['winter']=0
    item_item['spring']=0
    item_item['summer']=0
    item_item['autumn']=0
    item_item['day']=0
    item_item['night']=0
    item_item['avg rating']=0
    item_item['female love u25']=0
    item_item['female love o25']=0
    item_item['male love u25']=0
    item_item['male love o25']=0
    item_item['female like u25']=0
    item_item['female like o25']=0
    item_item['male like u25']=0
    item_item['male like o25']=0
    item_item['female dislike u25']=0
    item_item['female dislike o25']=0
    item_item['male dislike u25']=0
    item_item['male dislike o25']=0
    
    #Assign values to each new column
    for idx,frag in enumerate(item_item['frag rating']):
        for k,v in sorted(frag.items()):
            if k=='clswinter':
                item_item['winter'][idx]= v
            if k=='clsspring':
                item_item['spring'][idx]= v
            if k=='clssummer':
                item_item['summer'][idx]= v
            if k=='clsautumn':
                item_item['autumn'][idx]= v
            if k=='clsday':
                item_item['day'][idx]= v
            if k=='clsnight':
                item_item['night'][idx]= v
            if k=='clslove_female25under':
                item_item['female love u25'][idx]= v
            if k=='clslove_male25under':
                item_item['male love u25'][idx]= v
            if k=='clslove_female25older':
                item_item['female love o25'][idx]= v
            if k=='clslove_male25older':
                item_item['male love o25'][idx]= v
            if k=='clslike_female25under':
                item_item['female like u25'][idx]= v
            if k=='clslike_male25under':
                item_item['male like u25'][idx]= v
            if k=='clslike_female25older':
                item_item['female like o25'][idx]= v
            if k=='clslike_male25older':
                item_item['male like o25'][idx]= v
            if k=='clsdislike_female25under':
                item_item['female dislike u25'][idx]= v
            if k=='clsdislike_male25under':
                item_item['male dislike u25'][idx]= v
            if k=='clsdislike_female25older':
                item_item['female dislike o25'][idx]= v
            if k=='clsdislike_male25older':
                item_item['male dislike o25'][idx]= v
            if k=='average_rating':
                item_item['avg rating'].iloc[idx]=float(v)
    
    #Drop original column after unpacking
    item_item.drop(columns='frag rating',inplace=True)
    
    return item_item