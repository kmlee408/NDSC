import os
import sys
import time
import datetime
import multiprocessing as mp
_sys_add_path = os.path.abspath('../YT_api')
sys.path.insert(1,_sys_add_path)

import pandas as pd
import YouTube

import matplotlib.pyplot as plt
import seaborn as sns

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
    _dir = os.path.abspath('..')+'/datasets/datasets_ver1/'
    _file_names = ['CAvideos','GBvideos','USvideos']

    _pieces = []
    for fn in _file_names:
        df = pd.read_csv(_dir+fn+'.csv')
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
    dataframe[_by].astype(np.int64)

    _len_dataframe = len(dataframe)

    _dataframe = dataframe.sort_values(by=[_by])
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
        df.loc[_st:_et, 'Grade'] = str(Count)+' grade'

        Count= Count -1
        _st = _et

    return df


def make_graph(dataframe, column_name):
    '''
    DataFrame과 값을 알 고싶은 Column 이름을 쓰셈
    그럼 그래프랑 등급별 평균 산출됨!
    numeric columns = ['views','likes','dislikes','category_id','comment_count','duration']
    '''

    df_ = dataframe.reset_index()
    graph = sns.lmplot(data = df_ , x='index', y=column_name, hue ='Grade', fit_reg=False, size= 8)   
    # fit_reg = 회귀선 표기할꺼냐
    # hue = 구분하는 기준을 뭘로 할꺼냐
    
    print(column_name + ' Graph')
    
    
    # 등급별 평균값 산출
    _pct = [0.04, 0.07, 0.12, 0.17, 0.20, 0.17, 0.12, 0.07]
    _len=len(dataframe)
    _dps_cnts_levels = [ int(_len * pct) +1 for pct in _pct ]
    
    _st= 0
    Count = 8
    for vcnt in _dps_cnts_levels:
        
        _et = _st + vcnt
        print(Count , ' 등급 별 평균 값 : %d' % (sum(df_.loc[_st:_et,column_name])/(_et-_st)))
        Count= Count -1
        _st = _et
    
    print('\n')
    
    return graph
    



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

