import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app


class TestDel(unittest.TestCase):

    def setUp(self) -> None:
        app = create_app()
        app.testing = True
        self.client = app.test_client()

    def test_client(self):
        """
        测试是否能访问
        :return:
        """
        rp = self.client.get('/')
        self.assertEqual(rp.status_code, 200)

    def test_delBook_admin_not_exists(self):
        """
        测试管理员信息不存在
        :return:
        """
        rp = self.client.get("/admin/book/del", query_string={'admin_id': "123", 'type': "A", 'book_id': "9787010062208"})
        
        # 打印响应状态码
        print(f"响应状态码: {rp.status_code}")
        
        # 打印响应数据
        data = rp.json
        print(f"获得的data是: {data}")

        # 确保响应数据不是 None
        if data is None:
            self.fail("响应数据为 None")

        # 检查期望的结果
        self.assertEqual(data["data"], "管理员不存在，无法删除书籍")
    
    
    def test_delBook_book_exists_borrowed(self):
        """
        测试书籍存在且已借出
        """
        rp = self.client.get("/admin/book/del", query_string={'admin_id': "27", 'type': "A", 'book_id': "9787010062208"})
        
        # 打印响应状态码
        print(f"响应状态码: {rp.status_code}")
        
        # 打印响应数据
        data = rp.json
        print(f"获得的data是: {data}")

        # 确保响应数据不是 None
        if data is None:
            self.fail("响应数据为 None")

        # 检查期望的结果
        self.assertEqual(data["data"], "该书籍借阅中无法删除")


    def test_delBook_success(self):
        """
        测试删除书籍成功
        :return:
        """
        rp = self.client.get("/admin/book/del", query_string={'admin_id': "27", 'type': "E", 'book_id': "123"})
        
        # 打印响应状态码
        print(f"响应状态码: {rp.status_code}")
        
        # 打印响应数据
        data = rp.json
        print(f"获得的data是: {data}")

        # 确保响应数据不是 None
        if data is None:
            self.fail("响应数据为 None")

        # 检查期望的结果
        self.assertEqual(data["data"], "该书籍已删除")

    def test_delBook_book_not_exists(self):
        """
        测试书籍不存在的情况
        """
        rp = self.client.get("/admin/book/del", query_string={'admin_id': "27", 'type': "E", 'book_id': "234"})
        
        # 打印响应状态码
        print(f"响应状态码: {rp.status_code}")
        
        # 打印响应数据
        data = rp.json
        print(f"获得的data是: {data}")

        # 确保响应数据不是 None
        if data is None:
            self.fail("响应数据为 None")

        # 检查期望的结果
        self.assertEqual(data["data"], "找不到指定书籍")


if __name__ == '__main__':
    unittest.main(verbosity=2)

