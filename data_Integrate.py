
# coding: utf-8

# In[11]:


import pandas as pd

file_name = ['CAvideos', 'DEvideos','FRvideos','GBvideos','USvideos']

pieces = []
for fn in file_name:    
    df = pd.read_csv(fn+'.csv')
    print(fn +  ' ' + 'transfer to DataFrame')
    pieces.append(df)
    

df_ver1 = pd.concat(pieces, ignore_index = True)
df_ver1

