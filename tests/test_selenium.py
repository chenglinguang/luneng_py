import re
import threading
import time
import unittest
from app import create_app,db
from app.models import Role,User,Post
from selenium import webdriver

class SeleniumTestCase(unittest.TestCase):
    client=None
    
    @classmethod
    def setUpClass(cls):
        #启动Firefox
        try:
            cls.client=webdriver.FireFox()
        except:
            pass
        #如果无法启动浏览器，则跳过这些测试
        if cls.client:
            #创建程序
            cls.app=create_app('testing')
            cls.app_context=cls.app.app_context()
            cls.app_context.push()
 
            #禁止日志，保持输出整洁
            import logging
            logger=logging.getlogger('werkzeug')
            logger.setLevel("ERROR")

            #创建数据库，并使用一些虚拟数据填充
            db.create_all()
            Role.insert_roles()
            User.generate_fake(10)
            Post.generate_fake(10)
            #添加管理员
            admin_role=Role.query.filter_by(permission=0xff).first()
            admin=User(email='853059006@qq.com',username='chris', password='123456',role=admin_role)
            db.session.add(admin)
            db.session.commit()
            
            #在一个线程中启动FLask服务器
            threading.Thread(target=cls.app.run).start()

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            #关闭Flask服务器和浏览器
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.close()

            #销毁数据库
            db.drop_all()
            db.session.remove()

            #删除程序上下文
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')
    def tearDown(self):
        pass

    def test_admin_home_page(self):
        #进入首页
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('您好，新用户！',self.client.page_source))
        
        #进入登陆页面
        self.client.find_element_by_link_text('Log In').click()
        self.assertTrue('<h1>Login</h1>' in self.client.page_source)
 
        #登陆
        self.client.find_element_by_name('email').send_keys('853059006@qq.com')
        self.client.find_element_by_name('password').send_keys('123456')
        self.client.find_element_by_name('submit').click()
        self.assertTrue(re.search('您好，印第安酋长',self.client.page_source))

        #进入用户个人资料页面
        self.client.find_element_by_link_text('个人资料').click()
        self.assertTrue('<h1>印第安酋长</h1>' in self.client.page_source)



        







