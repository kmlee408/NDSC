import os
import sys
import time
import datetime
import multiprocessing as mp
_sys_add_path = os.path.abspath('../YT_api')
sys.path.insert(1,_sys_add_path)

import numpy as np
import pandas as pd
import YouTube

import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob

def _runner_get_duration(yt,vid_list):
    print('Process Started')
    _duration = []
    _errors_vid_numbers = []

    for vid in vid_list:
        _vid_len = yt.get_duration(vid)
        if _vid_len == -1:
            _errors_vid_numbers.append(vid)
        _duration.append(_vid_len)
            
    return (_duration, _errors_vid_numbers)

def data_format(dataframe):
    #csv 파일을 dataframe한 df_ver1 을 input함
    #전체 전처리 모듈임 이것만 실행하면 됨
    
    dataframe = drop_not_ints(dataframe, 'views')
    dataframe = drop_not_ints(dataframe, 'likes')
    dataframe['views'] = dataframe['views'].astype('int64')
    dataframe['likes'] = dataframe['likes'].astype('int64')
    del dataframe['Unnamed: 17']
    del dataframe['Unnamed: 18']
    dataframe = dataframe.reset_index(drop=True)
    print('formating....')
     
    
    df_ver2 = gap_time(dataframe) # 올린지 얼마만에 인기동영상이 됐는지
    print('gap_time format complete')
    df_ver3 = sentiment_analysis(df_ver2 , 'description') # 감정 분석
    print('Sentiment format complete')
    df_ver4 = time_devide(df_ver3) # 시간 6개 구간으로 나눔
    print('Time devide format complete')
    
    cols =['category_id','publish_time_devide']
    df_ver5 = one_hot_encoding(df_ver4, cols) # 원 핫 인코딩
    print('one-hot-encoding is complete')
    df_ver6 = topic_find(df_ver5) # 제목이랑 태그에서 키워드 추출
    print('Title,Tags topic Find is complete')
    df_ver7 = make_grade_columns(df_ver6) # 등급 매기기
    print('Grade format complete')
    
    #cleaning data
    df_ver8 = col_del(df_ver7) # 불필요한 feature 제거
    print('Delete col complete')
    df_ver9 =df_ver8.dropna() #nan 
    
    return df_ver9


def get_video_len(fpath, multi=0):
    
    _dt = pd.read_csv(fpath)
    _vids = _dt['video_id']
    _vids_len = len(_vids)

    yt = YouTube.YouTube('AIzaSyDdPiRW0lXGtY_s188gr6tIZ8WY_ZqAglM')
    
    
    _duration = []
    _errors = []

    _start_tm = time.time()
    if multi != 0:
        result = []
        pool = mp.Pool(processes=multi)
        _div = int(_vids_len / multi) + 1

        try:
            for idx in range(multi):
                _s = idx * _div
                _e = _s + _div

                _lst = _vids[_s:_e]
                result.append(pool.apply_async(_runner_get_duration, args=(yt,_lst,)))
        except Exception as e:
            print('Multiprocessing Error')
            print(e)
            sys.exit()
        finally:
            pool.close()
            pool.join()

        try:
            for rst in result:
                _returned_val = rst.get() # tuple (_durationlist, errlist)
                _duration.extend(_returned_val[0])
                _errors.extend(_returned_val[1])
        except Exception as e:
            print('Multiprocessing Error : rst.get()')
            sys.exit()

    else:
        for vid in _vids:
            try:
                _tm = yt.get_duration(vid)
                _duration.append(_tm)

            except ValueError as e:
                if e.args[0] == 1: #connection error
                    pass
                elif e.args[0] == 2: #json erro
                    pass
                else: #convert time error
                    pass
                _count_error += 1

    _end_tm = time.time()
    print('TIME ELAPSED : '+str(_start_tm - _end_tm))
    
    _vids_len_series = pd.Series(_duration)

    return (_vids_len_series, _errors)


def merge_data():
    '''
    ver1 데이터프레임을 1개의 데이터프레임으로 합쳐서 리턴 
    '''
    _dir = os.path.abspath('.')+'/datasets/datasets_ver1/'
    _file_names = ['CAvideos','GEvideos','USvideos']

    _pieces = []
    for fn in _file_names:
        df = pd.read_csv(_dir+fn+'_ver1.csv')
        print(fn +  ' ' + 'transfer to DataFrame')
        _pieces.append(df)


    _merged_df = pd.concat(_pieces, ignore_index = True)
    return _merged_df

def divide_by_level(levels=9, value='views'):
    '''
    주어진 값(values 매개변수)을 기준으로 데이터프레임을 9개등급으로 분할하여 리턴한다
    리턴값 : ( [각 등급 구간별 value개수], [각 등급 구간별 values] )
    '''
    _merged_df = merge_data()

    _views_series = dataset_df[value]
    _views_series_sorted = _views_series.sort_values() #in ascending order

    _div = levels
    _len = len(_views_series_sorted)

    #percentage of level 9 ~ 1
    _pct = [0.04, 0.07, 0.12, 0.17, 0.20, 0.17, 0.12, 0.07, 0.04]

    #list of ( no. of datapoints in level9 ~ 1 )
    _dps_cnts_levels = [ int(_len * pct) +1 for pct in _pct ]

    #list of lists (each list is datapoints in level9 ~ 1)
    _dps_vals_levels = []

    #divide dps operation
    _st = 0
    for vcnt in _view_cnts_by_pct:
        _et = _st + vcnt

        _lst = _views[_st:_et]
        _dps_vals_levels.append(_lst)

        _st = _et

    #dps_cnts_levels : list of cnts in each level
    #dps_vals_levels : list of views in each level
    return (dps_cnts_levels,_dps_vals_levels)    


def get_df_sorted_by_values(dataframe, _by='views'):
    '''
    returns a dataframe that is sorted by number of views
    '''
    _len_dataframe = len(dataframe)

    _dataframe = dataframe.sort_values(by=[_by],ascending=True)
    _dataframe.index = range(_len_dataframe)

    return _dataframe


def to_epoch(real_time):

    stime = "%s/%s/%s" %(real_time[8:10], real_time[5:7], real_time[0:4])
    sec = int(real_time[11:13])*60*60 + int(real_time[14:16])*60 +int(real_time[17:19])

    unixday = time.mktime(datetime.datetime.strptime(stime, "%d/%m/%Y").timetuple())
    unixtime = int(unixday + sec)
    return unixtime



def group_by_categoryid(dataframe):
    #_min_categoryid = min(int(dataframe['category_id']))
    #_max_categoryid = max(int(dataframe['category_id']))

    _category_ids = dataframe['category_id']
    _video_ids = dataframe['video_id']

    _categorized_videos = { k:v for k,v in zip(_category_ids, _video_ids) }

    return _categorized_videos


def group_by_duration(dataframe):
    _min_duration = min(int(dataframe['duration'])) 
    _max_duration = max(int(dataframe['duration']))

    _div = (_max_duration - _min_duration) / 9 #levels
    
    

    
def make_grade_columns(dataframe):
    '''
    데이터프레임 등급 매기기 모듈임 (굿)
    'Grade' 칼럼 붙여서 return
    
    '''
    dataframe = drop_not_ints(dataframe, 'views')
    df = get_df_sorted_by_values(dataframe)
    
    _len = len(df)
    #percentage of level 9 ~ 1
    _pct = [0.04, 0.07, 0.12, 0.17, 0.20, 0.17, 0.12, 0.07, 0.04]

    #list of ( no. of datapoints in level9 ~ 1 )
    _dps_cnts_levels = [ int(_len * pct) +1 for pct in _pct ]
    _st = 0
    Count = 9
    for vcnt in _dps_cnts_levels:

        _et = _st + vcnt
        df.loc[_st:_et, 'Grade'] = Count###+' grade'
        print(Count)

        Count= Count -1
        _st = _et

    return df


def make_graph(dataframe, column_name):
    '''
    DataFrame과 값을 알 고싶은 Column 이름을 쓰셈
    그럼 그래프랑 등급별 평균 산출됨!
    numeric columns = ['views','likes','dislikes','category_id','comment_count','duration']
    '''
    _max = max(dataframe[column_name])
    _min = min(dataframe[column_name])

    scaler = _max - _min 

    df_ = dataframe.reset_index()
    df_[column_name] = df_[column_name] / scaler
    graph = sns.lmplot(data = df_ , x='index', y=column_name, hue ='Grade', fit_reg=False, size= 8)   
    # fit_reg = 회귀선 표기할꺼냐
    # hue = 구분하는 기준을 뭘로 할꺼냐

def get_means(dataframe, column_name):    
    
    _max = max(dataframe[column_name])
    _min = min(dataframe[column_name])

    scaler = _max - _min 

    df_ = dataframe.reset_index()
    df_[column_name] = df_[column_name] / scaler

    # 등급별 평균값 산출
    _pct = [0.04, 0.07, 0.12, 0.17, 0.20, 0.17, 0.12, 0.07, 0.04]
    _len=len(dataframe)
    _dps_cnts_levels = [ int(_len * pct) +1 for pct in _pct ]
    
    _st= 0
    Count = 9

    values = []
    for vcnt in _dps_cnts_levels:
        
        _et = _st + vcnt
        value = sum(df_.loc[_st:_et, column_name])/(_et-_st)
        values.append(value)
        #print(Count , ' 등급 별 평균 값 : %f' % (value))
        Count= Count -1
        _st = _et
    
    
    return values #from 9-1 level of a feature

def make_dt_feats_by_levels(dataframe, feature_names):
    #feature names : 특성명

    _list_of_values = [] #특성별 리스트
    for feat in feature_names:
        _values = get_means(dataframe, feat) #1~9등급까지의 평균값들 리스트
        _list_of_values.append(_values)

    _len_lv = 9
    _len_feat = len(feature_names)

    _list_of_values = np.array(_list_of_values)

    print(np.array(_list_of_values).shape)

    dt = pd.DataFrame(_list_of_values, columns = range(9,0,-1), index = feature_names)

    dt['diff(9-1)']=dt[9]-dt[1]

    return dt


            
            
        
    


def drop_not_ints(dataframe, feat):
    '''
        dataframe의 feat특성열의 값 중에 -1인 값을 찾아서 해당 행을 제거한 dataframe을 리턴 
    '''
    def _to_ints(val):
        try:
            v = int(val)
        except ValueError:
            return -1
        else:
            return v

    _idx_of_rows_to_delete = pd.Series(list(map(_to_ints, dataframe[feat])))

    _d_idx = _idx_of_rows_to_delete[_idx_of_rows_to_delete == -1].index
    
    return dataframe.drop(_d_idx)

def get_merged_dataframe_by_columns(list_of_dataframes):
    return pd.concat(list_of_dataframes, axis=1)

def time_devide(df):
    '''
    시간을 6가지 등급으로 나누어 column 생성해서 값넣고 return
    '''
    df_ = df
    for i in range(len(df_)): 
        
        time_devide = int(df_.loc[i,'publish_time'][11:13])
        val =  int(time_devide / 4 ) + 1
        df_.loc[i,'publish_time_devide'] = val
       
    return df_


def sentiment_analysis(df,col):
    '''    
    from textblob import TextBlob
    
    Dataframe과 column 이름을 넣어주면, 해당 column의 text 감성을 분석 하여 (긍정(1), 부정(-1))
    'senti_mark'라는 column을 생성한 뒤 값 넣음
    
    '''
    df_ = df
    for i in range(len(df_)):

        text = df_.loc[i,col]
        try:
            wiki = TextBlob(text)
        except:
            continue

        mark = wiki.sentiment.polarity
        df_.loc[i,'senti_mark'] = mark
        
    return df_
 
    
    
def one_hot_encoding(df,cols):
    '''
    Dataframe이랑 원핫인코딩 할 column 이름 넣으면, 기존 column은 없어지고 인코딩된 column 생성
    중요한건 cols 가 list타입의 columns name이여야함 ex) cols =['category_id','publish_time_devide']
    '''   
    df_ = df
    for col in cols:
        df_ = pd.concat([df_, pd.get_dummies(df_[col], prefix = col)], axis = 1)
        df_ = df_.drop(col, axis = 1)
        
    return df_


def categorize_dataset_by_grade(dataframe):
    grades_feature = []
    for i in range(1,10):
        grades_feats.append(dataframe['Grade'][:] == i)

    return grades_feats

def get_feature_values_in_grade(dataframe, feature, grade):
    grades_feats = categorize_dataset_by_grade(dataframe)
    
    ret_values = np.array(grades_feats[grade-1][feature])

    return ret_values

def col_del(df):
    
    df_=df
    cols = ['video_id','trending_date','title','tags','publish_time','description','channel_title','thumbnail_link','comments_disabled','ratings_disabled','video_error_or_removed'] 

    for col in cols:

        try:
            del df_[col]
        except:
            continue
            
    return df_

def gap_time(df):
    
    df_ = df
    for i in range(len(df_)):

        trend = '20'+df_.loc[i,'trending_date']
        trend_date = datetime.datetime.strptime(trend, "%Y.%d.%m")
        trend_epoch = time.mktime(trend_date.timetuple())

        pub_date= datetime.datetime.strptime(df_.loc[i,'publish_time'][:-13], '%Y-%m-%dT')
        pub_epoch = time.mktime(pub_date.timetuple())
        
        gap = trend_epoch - pub_epoch
        df_.loc[i,'gap_time'] = gap

    return df_

def SelectKBest(df):
    '''
    format data후 DataFrame 넣으면 Grade와의 분산 분석한다. 분산의 정도가 유사한 1등부터 차례대로 나열
    '''
    df_= df.dropna()

    X, y = df_.iloc[:,0:9], df_.iloc[:,9:10]

    for k in range(1,10):

        X_new = SelectKBest(f_classif, k=k).fit(X, y)
        SFcolumns=X_new.get_support(indices=True)    

        print(k ,'등' ,df_.columns[SFcolumns])

        
def topic_find(df):
    '''
    DataFrame입력하면, 아래 Topic 워드들이 포함됐는지 원-핫-인코딩을 자동으로 해서
    새로운 칼럼 생성한 뒤, DataFrame return한다.
    '''   
    df_ = df
    topic_title = ['|','official', 'video', '2018']
    topic_tags = ['vs', 'new', 'music' ,'you']
    
    tp = topic_title
    col_name = 'title'
    for num in range(0,2):
        
        for i in range(len(df_)):
            
            Text = df_.loc[i,col_name]
            
            for char in '-.,\n()':
                Text = Text.replace(char,' ')
                
            Text = Text.lower()
            word_list = Text.split()

            for j in range(len(word_list)):

                if word_list[j] in tp:
                    df_.loc[i, word_list[j]+'_count'] = 1
                
        tp = topic_tags
        col_name = 'tags'
        
        
    df_temp = df_.iloc[:,-8:]
    col = df_temp.columns
    
    for i in col:
        temp_col = df_[i]
        temp_col[temp_col!=1] = 0
        del df_[i]
        df_ = pd.concat([df_,temp_col], axis =1)
    
    return df_
    
def move_Grade(df):
    '''
    Grade 칼럼을 맨 끝으로 보내는 모듈
    특징: 
    '''
    grd = df.copy()['Grade']
    del df['Grade']
    df['Grade']=grd
    
def word_find(df,col)
    '''
    DataFrame과 column명을 써넣으면 그 column에 가장 많이 나온 단어 추출함
    '''
    df_=df
    tp = df_[col]
    word_freq = []
    str_ =''
    for i in range(len(tp)):
        str_ = str_ + tp[i]


    Text = str_
    for char in '-.,\n()':
        Text = Text.replace(char,' ')

    Text = Text.lower()
    word_list = Text.split()

    d= {}
    for word in word_list:
        d[word] = d.get(word, 0) +1


    for key, value in d.items():
        word_freq.append((value,key))

    word_freq.sort(reverse = True )
    
    return word_freq
