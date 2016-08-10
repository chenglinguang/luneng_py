import unittest

from app import create_app,db
from app.models import User,Role

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app=create_app('testing')
        self.app_context=self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client=self.app.test_client(use_cookie=True)
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response=self.client.get(url_for('main.index'))
        self.assertTrue('Stranger' in response.get_data(as_text=True))
    
    def test_register_login(self):
        #注册新用户
        response=self.client.post(url_for('auth.register'),data={'email':'853059006@qq.com','username':'chris','password':'123456','password2':'123456'})
        self.assertTrue(response.status_code==302)
        #使用新注册的账户登录
        response=self.client.post(url_for('auth.login'),data={'email':'85305906@qq.com','password':'123456'},follow_redirects=True)
        data=response.get_data(as_text=True)
        self.assertTrue(re.search('您好,\s+chris',data))
         
        #退出
        response=self.client.get(url_for('auth.logout'),follow_redirects=True)
        data=response.get_data(as_text=True)
        self.assertTrue('您已经退出登陆' in data)
