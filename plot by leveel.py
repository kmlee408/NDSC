
# coding: utf-8

# In[5]:


import pandas as pd
import os


def data_merge(fpath):#fpath : ...../NDSC/datasets/
    file_name = ['CAvideos', 'DEvideos','FRvideos','GBvideos','USvideos']

    pieces = []
    for fn in file_name:    
        df = pd.read_csv(fpath+'/'+fn+'.csv')
        print(fn +  ' ' + 'transfer to DataFrame')
        pieces.append(df)
    

    df_ver1 = pd.concat(pieces, ignore_index = True)
    return df_ver1 


if __name__ == '__main__':

    _cur_dir = os.path.abspath('.')+'/datasets'
    dataset_df = data_merge(_cur_dir)

    _views = dataset_df['views']
    sorted_Series_by_view = _views.sort_values()
    #print(sorted_Series_by_view)


    _div = 9 
    _len = len(sorted_Series_by_view)
    
    _pct = [0.04, 0.07, 0.12, 0.17, 0.20, 0.17, 0.12, 0.07, 0.04]

    #각 레벨별 데이터 개수
    _view_cnts_by_pct = [ int(_len * pct) +1 for pct in _pct ]

    #각 레벨별 데이터 포인트 리스트가 저장되어 있다
    _dfs_by_level = [] #9등급
    _st = 0 
    for vcnt in _view_cnts_by_pct:
        _et = _st + vcnt

        _lst = sorted_Series_by_view[_st:_et]
        _dfs_by_level.append(_lst)

        _st = _et 
    
    final_list = []
    for lst in _dfs_by_level:
        final_list.extend(lst)
        
    #print(final_list)


# In[6]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[43]:



#_dfs_by_level

#print(_data)

plt.subplots(1,9)

for g in range(9):
    plt.scatter(x=range(len(_dfs_by_level[g])),y=_dfs_by_level[g])


# In[15]:




