from config import db


class BorrowedInfo(db.Model):
    __tablename__ = 'borrowed_info'
    reader_id = db.Column(db.String(255), primary_key=True, nullable=False)
    book_id = db.Column(db.String(255), primary_key=True, nullable=False)
    book_name = db.Column(db.String(255), nullable=False)
    borrowed_time = db.Column(db.Date, nullable=False,primary_key=True)
    is_returned = db.Column(db.Boolean, nullable=False)
    returned_time = db.Column(db.Date, nullable=True)
    author = db.Column(db.String(255), nullable=False)
    is_lost = db.Column(db.Boolean, nullable=False)
    publisher = db.Column(db.String(255), nullable=False)
    is_code = db.Column(db.Boolean, nullable=False)
    doer_id = db.Column(db.String(255), nullable=False)
    borrowed_num = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.String(255), nullable=False)


class Book(db.Model):
    __tablename__ = 'book'
    book_id = db.Column(db.String(255), primary_key=True, nullable=False)
    book_name = db.Column(db.String(255), nullable=False)
    inventory = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    admin_id = db.Column(db.String(255), nullable=False)
    picture = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    publisher = db.Column(db.String(255), nullable=False)
    publish_time = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(255), nullable=False)
    share_time = db.Column(db.Date, nullable=True)
    # borrow_infos = db.relationship('BorrowedInfo', backref='book', lazy='dynamic')


class Reader(db.Model):
    __tablename__ = 'reader'
    reader_id = db.Column(db.String(255), primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    identity = db.Column(db.Boolean, nullable=False)
    borrowed_num = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    money = db.Column(db.Float, nullable=False)
    receive_code = db.Column(db.String(255), nullable=False)
    job_number = db.Column(db.String(255), nullable=False)


class User(db.Model):
    __tablename__ = 'user'
    username = db.Column(db.String(255), primary_key=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)


class Information(db.Model):
   __tablename__ ='information'
   info_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   adminer_id = db.Column(db.String(255),nullable=False)
   create_time = db.Column(db.Date, nullable=False)
   public_time = db.Column(db.Date)
   information = db.Column(db.String(255),  nullable=False)
   phone = db.Column(db.String(255))
   email = db.Column(db.String(255))
   title = db.Column(db.String(255))
   status = db.Column(db.Boolean, nullable=False)


class Adminer(db.Model):
    __tablename__ ='adminer'
    adminer_id = db.Column(db.String(255),  primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    number = db.Column(db.String(255), nullable=False)
    # profile = db.Column(db.String(255), nullable=False)


class Money(db.Model):
    __tablename__ = 'money'
    reader_id = db.Column(db.String(255), primary_key=True, nullable=False)
    book_id = db.Column(db.String(255), primary_key=True, nullable=False)
    type = db.Column(db.String(255), nullable=False)
    money = db.Column(db.Float, nullable=False)
    is_cost = db.Column(db.Boolean, nullable=False)
    owner = db.Column(db.String(255), nullable=False)
    time=db.Column(db.Date, nullable=False,primary_key=True)

    def __repr__(self):
        return f'<BorrowedInfo(book_id={self.book_id}, book_name={self.book_name}, reader_id={self.reader_id})>'



