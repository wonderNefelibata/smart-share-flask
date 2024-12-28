from sqlalchemy import func

from model import Book, BorrowedInfo, Adminer
from model import Reader
from config import db

class DataManage():

    # 获取
    @staticmethod
    def getData(admin_id):
        existing_adminId = Adminer.query.filter_by(adminer_id=admin_id).first()
        if existing_adminId:
            # 获取每月借阅量
            total_borrowed_book = db.session.query(func.sum(BorrowedInfo.borrowed_num)).scalar()
            # 获取馆藏书籍量
            total_library_book = db.session.query(func.sum(Book.inventory)).filter(Book.admin_id == '图书馆').scalar()
            # 获取读者分享量
            total_share_book = db.session.query(func.sum(Book.inventory)).filter(Book.admin_id != '图书馆').scalar()
            # 获取未归还书籍量
            not_return = db.session.query(func.sum(BorrowedInfo.borrowed_num)).filter(BorrowedInfo.is_returned == 0 ).scalar()

            result = {
                'total_borrowed_book': total_borrowed_book,
                'total_library_book': total_library_book,
                'total_share_book': total_share_book,
                'not_return': not_return
            }

            return result
        else:
            return "管理员不存在，无法显示数据"

    # # 获取不同类型书籍借阅量
    # @staticmethod
    # def getTypeData(admin_id):
    #     existing_adminId = Adminer.query.filter_by(adminer_id=admin_id).first()
    #     if existing_adminId:
    #         result = db.session.query(func.substr(BorrowedInfo.book_id, 1, 1), func.count(BorrowedInfo.book_id)).group_by(
    #             func.substr(BorrowedInfo.book_id, 1, 1)).all()
    #         category_counts = {row[0]: row[1] for row in result}
    #         print(category_counts)
    #         return category_counts
    #     else:
    #         return "管理员不存在，无法查看数据"
    @staticmethod
    def getTypeData(admin_id):
        existing_adminId = Adminer.query.filter_by(adminer_id=admin_id).first()
        if existing_adminId:
            result = db.session.query(func.substr(BorrowedInfo.book_id, 1, 1),
                                      func.count(BorrowedInfo.book_id)).group_by(
                func.substr(BorrowedInfo.book_id, 1, 1)
            ).all()

            category_mapping = {
                "A": "马列主义、毛泽东思想类",
                "B": "哲学、宗教类",
                "C": "社会科学总论类",
                "D": "政治、法律类",
                "E": "军事类",
                "F": "经济类",
                "G": "文化、科学、教育、体育类",
                "H": "语言、文字类",
                "I": "文学类",
                "J": "艺术类",
                "K": "历史、地理类",
                "N": "自然科学总论类",
                "O": "数理科学和化学类",
                "P": "天文学、地球科学类",
                "Q": "生物科学类",
                "R": "医药、卫生类",
                "S": "农业科学类",
                "T": "工业技术类",
                "U": "交通运输类",
                "V": "航空、航天类",
                "X": "环境科学、安全科学类",
                "Z": "综合性图书类",
            }

            category_list = [
                {"name": category_mapping.get(row[0], row[0]), "value": row[1]}
                for row in result
            ]

            # 将查询结果转换为所需的对象数组形式
            # category_list = [{"name": row[0], "value": row[1]} for row in result]

            # print(category_list)
            return  category_list  # 将列表包装在"data"键下，以符合接口文档要求
        else:
            # 如果没有找到对应的管理员，可以返回一个错误信息或者空列表
            return "管理员不存在，无法查看数据"  # 或者可以返回一个包含错误信息的字典，例如 {"error": "Admin not found"}
