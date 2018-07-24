import requests
import json


class YouTube():
    
    def __init__(self, _api_key):
        self.api_key = _api_key #string
        self.url = 'https://www.googleapis.com/youtube/v3/videos?'
        self.session = requests.Session()

    def _get_ContentDetails(self,_vid, _fields=None):
        _url = self.url + 'id=' + str(_vid) \
                        + '&key=' + self.api_key \
                        + '&part=contentDetails'

        if not(_fields):
            if _fields in ['duration', 'dimension', 'definition', \
                           'caption', 'licensedContent', 'projection']:
                _url += '&fields=items(contentDetails(' + _fields + '))'    
        
        if not(self.session):
            response = session.get(_url)
        else:
            self.session = requests.Session()
            response = self.session.get(_url)

        try:
            _tries = 0
            while(response.status_code > 204):
                if _tries > 5:
                    print("ERROR : BAD REQUESTS CANNOT BE HANDLED")
            
                response = self.session.get(_url)
                _tries += 1

        except requests.ConnectionError as e:
            raise ValueError(1)
            

        try:
            _ret = json.loads(response.content)
            if len(_ret['items']) != 0:
                _ret = _ret['items'][0]['contentDetails']['duration']
            else:
                _ret = -1
        except Exception as e:
            raise ValueError(2)

        return _ret #returns in ISO 8601 format


    def _iso8601_to_seconds(self, code):
        _hours = 0
        _mins = 0
        _seconds = 0
          
        _h_idx = code.find('H')
        _m_idx = code.find('M')
        _s_idx = code.find('S')

        if code == '':
            return 0
        if code[2:] == '':
            return 0
        if code[0:2] != 'PT':
            return 0

        try:
            if _h_idx != -1:
                _hours = int(code[2:_h_idx])
                if _m_idx != -1:
                    _mins = int(code[_h_idx+1:_m_idx])
                if _s_idx != -1:
                    if _m_idx != -1:
                        _seconds = int(code[_m_idx+1:_s_idx])
                    else:
                        _seconds = int(code[_h_idx+1:_s_idx])

            else:#no hour
                if _m_idx != -1:
                    _mins = int(code[2:_m_idx])
                    if _s_idx != -1:
                        _seconds = int(code[_m_idx+1:_s_idx])
                    else:
                        if code[_m_idx+1:] != '':
                            _seconds = int(code[_m_idx+1:])
                else:#no minutes
                    if _s_idx != -1:
                        _seconds = int(code[2:_s_idx])
                    else:
                        if code[_m_idx+1:] != '':
                            _seconds = int(code[2:])

        except Exception as e:
            raise ValueError(3)
            


        return _hours*60*60 + _mins*60 + _seconds


    def get_duration(self, _vid):
        _duration_iso8601 = self._get_ContentDetails(_vid,'duration')
        print(_duration_iso8601)

        if _duration_iso8601 != -1:
            _duration_seconds = self._iso8601_to_seconds(_duration_iso8601)
        else:
            _duration_seconds = 0

        return _duration_seconds


    
if __name__ == '__main__':
    _api_key = 'AIzaSyDdPiRW0lXGtY_s188gr6tIZ8WY_ZqAglM'
    yt = YouTube(_api_key)

    #get duration of a video with id = 2kyS6SvSYSE
    _vid = '2kyS6SvSYSE'
    
    _duration = yt.get_duration(_vid)
    print(_duration)


