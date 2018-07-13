#zhangpengxuan
import json
import requests

class oAuth_QQ():
    def __init__(self,client_id,client_key,redirect_uri):
        self.client_id=client_id
        self.client_key=client_key
        self.redirect_uri=redirect_uri

    def get_auth_url(self):
        """获取授权页面的网址"""
        params = {'client_id': self.client_id,
                  'response_type': 'code',
                  'redirect_uri': self.redirect_uri,
                  'scope': 'get_user_info',
                  'state': 1}
        url = 'https://graph.qq.com/oauth2.0/authorize'

        r=requests.post(url,params)
        return r.url

    #获取access_token
    def get_access_token(self, code):
        """根据code获取access_token"""
        params = {'grant_type': 'authorization_code',
                  'client_id': self.client_id,
                  'client_secret': self.client_key,
                  'code': code,
                  'redirect_uri': self.redirect_uri}
        url = 'https://graph.qq.com/oauth2.0/token'

        # 访问该网址，获取access_token
        response = requests.post(url,params)
        data=response.text
        result=data.split('&')[0]
        access_token=result.split("=")[1]
        self.access_token=access_token
        return self.access_token
    #通过获得的access_token获得openID
    def get_open_id(self):
        params={
            "access_token":self.access_token,
        }
        url="https://graph.qq.com/oauth2.0/me"
        response=requests.post(url,params)
        data=response.text
        data=data.split("(")[1].split(")")
        result=json.loads(data[0])
        openid=result['openid']
        self.openid=openid
        return  self.openid

    def get_qq_info(self):
        """获取QQ用户的资料信息"""
        params = {'access_token': self.access_token,
                  'oauth_consumer_key': self.client_id,
                  'openid': self.openid
                  }
        url = 'https://graph.qq.com/user/get_user_info'
        response = requests.post(url,params)
        result=response.text
        return json.loads(result)

# h=oAuth_QQ('101481408','aa0e473a9192ee0c1a0a87e33774434c','http://www.zhangpengxuan.com/oauth/qq_check',)
# print(h.get_auth_url())
# print(h.get_qq_info('DD86EE284BF05D2E1EC9226DABDB132A','9F0E62A6492BBB3DC3320155EE76D9DA'))
