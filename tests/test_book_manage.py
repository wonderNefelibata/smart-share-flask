import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from manager.bookManage import BookManage
from app import create_app  # 假设你的应用创建函数在 app.py 中

class TestBookManage(unittest.TestCase):
    def setUp(self):
        # 创建 Flask 应用实例
        self.app = create_app()  # 假设你有一个测试配置
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_getBookList(self):
        book_list = BookManage.getBookList()
        self.assertIsNotNone(book_list)
        self.assertIsInstance(book_list, list)

if __name__ == '__main__':
    unittest.main()