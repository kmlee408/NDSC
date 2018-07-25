import sys
import os

_YOUTUBE = os.path.abspath('./YT_api')
_UNITS = os.path.abspath('./units')
sys.path.insert(1,_YOUTUBE)
sys.path.insert(1,_UNITS)

dataset_dir = './datasets/datasets_ver1'

print('library path added : Preprocessing')
print('library path added : YouTube')
print('Dataset path = '+ dataset_dir + ' : access by API.dataset_dir')


