import os
import sys
import time
import multiprocessing as mp
_sys_add_path = os.path.abspath('../YT_api')
sys.path.insert(1,_sys_add_path)

import pandas as pd
import YouTube

def _runner_get_duration(vid_list):
    _duration = [ yt.get_duration(vid) for vid in vid_list ]
    return _duration

def get_video_len(fpath, multi=0):
    
    _dt = pd.read_csv(fpath)
    _vids = _dt['video_id']
    _vids_len = len(_vids)

    yt = YouTube.YouTube('AIzaSyDdPiRW0lXGtY_s188gr6tIZ8WY_ZqAglM')
    
    
    _duration = []
    _count_error = 0

    _start_tm = time.time()
    if multi != 0:
        result = []
        pool = mp.Pool(processces=muti)
        _div = int(_vids_len / multi) + 1

        try:
            for idx in range(multi):
                _s = idx * _div
                _e = _s + _div

                _lst = _vids[_s:_e]
                result.append(pool.apply_async(_runner_get_duration, args=(lst,)))
        except Exception as e:
            print('Multiprocessing Error')
            print(e)
            exit()
        finally:
            pool.close()
            pool.join()

        try:
            for rst in result:
                _duration.extend(rst.get())
        except Exception as e:
            print('Multiprocessing Error : rst.get()')
            exit()

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

    return _vids_len_series


def merge_data():
    _dir = os.path.abspath('..')+'/datasets/'
    _file_names = ['CAvideos', 'DEvideos','FRvideos','GBvideos','USvideos']

    _pieces = []
    for fn in _file_names:
        df = pd.read_csv(_dir+fn+'.csv')
        print(fn +  ' ' + 'transfer to DataFrame')
        _pieces.append(df)


    _merged_df = pd.concat(_pieces, ignore_index = True)
    return _merged_df

def divide_by_level(levels=9):
    _merged_df = merge_data()

    _views_series = dataset_df['views']
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
        _dps_vals_level.append(_lst)

        _st = _et

    #dps_cnts_levels : list
    #dps_vals_levels : list
    return (dps_cnts_levels,_dps_vals_levels)    

     
