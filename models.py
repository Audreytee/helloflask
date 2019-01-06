from app import db
from sqlalchemy.orm import class_mapper
# from datetime import datetime
#创建模型对象
class FaceObject(db.Model):
	__tablename__='face_object'
	id = db.Column(db.Integer, primary_key=True)
	objId=db.Column(db.String(45))
	patId=db.Column(db.String(45))
	objName = db.Column(db.String(80))
	objType = db.Column(db.Integer)
	objClass = db.Column(db.String(80))
	schoolId = db.Column(db.String(80))
	objSex = db.Column(db.Integer)
	objAge = db.Column(db.Integer)
	objPhone = db.Column(db.String(80))
	objAddr = db.Column(db.String(120))
	objImage=db.Column(db.LargeBinary)
	# staFlag=db.Column(db.Integer)
	# relImage=db.Column(db.TEXT)
	# dataType=db.Column(db.Integer)
	
	def to_json(self):
		dict=self.__dict__
		if "_sa_instance_state" in dict:
			del dict["_sa_instance_state"]
		return dict
	
	# def as_dict(obj):
		# return dict((col.name,getattr(obj,col.name))\
					# for col i class_mapper(obj.__class__).mapped_table.c)
	
	
	
	def __repr__(self):
		return '<FaceObject %r>' % self.objId

	
	
class ImageFile(db.Model):
	__tablename__ = 'ImageFile'
	id = db.Column(db.Integer, primary_key=True)
	image_name = db.Column(db.String(30), index=True)
	image = db.Column(db.LargeBinary(length=2048))
	
	
	def __repr__(self):
		return '<User %r>' % image_name

		
class Uploads(db.Model):
	__tablename__='uploadfile'
	id = db.Column(db.Integer, primary_key=True)
	msgId=db.Column(db.Integer,nullable=False)
	schoolId=db.Column(db.String(80),nullable=False)
	stuId=db.Column(db.String(20),nullable=False)
	patId=db.Column(db.String(20),nullable=True)
	inOutType=db.Column(db.Integer)
	stuImage=db.Column(db.TEXT)
	patImage=db.Column(db.TEXT)
	time=db.Column(db.String(45))
	timeStamp=db.Column(db.String(45))
	flag= db.Column(db.Integer)
	
	
	def __repr__(self):
		return '<usr %r>' % self.stuId
		
class ObjRelation(db.Model):
		__tablename__='object_relation'
		id = db.Column(db.Integer, primary_key=True)
		stuId=db.Column(db.String(45))
		patId=db.Column(db.String(45))
		schoolId=db.Column(db.String(45))
		
class HostInfo(db.Model):
		__tablename__='hostinfo'
		id = db.Column(db.Integer, primary_key=True)
		ip = db.Column(db.String(45))
		mac = db.Column(db.String(45))
		schoolId = db.Column(db.String(45))
		time = db.Column(db.DateTime)
		
class Stutest(db.Model):
	__tablename__='stu_test'
	id = db.Column(db.Integer, primary_key=True)
	msgId=db.Column(db.Integer,nullable=False)
	schoolId=db.Column(db.String(80),nullable=False)
	stuId=db.Column(db.String(20),nullable=False)
	patId=db.Column(db.String(20),nullable=True)
	inOutType=db.Column(db.Integer)
	stuImage=db.Column(db.TEXT)
	patImage=db.Column(db.TEXT)
	time=db.Column(db.String(45))
	timeStamp=db.Column(db.String(45))
	flag= db.Column(db.Integer)
	
	
db.create_all()
# db.drop_all()
	
	
	
	
	
	
	
	
	
	
	
	
	
# 1.创建表

# # 2.增加记录
# admin = User(username='admin', email='admin@example.com')
# guest = User(username='guest', email='guest@example.com')
# db.session.add(admin)
# db.session.add(guest)
# db.session.commit()

# #3.查询记录,注意查询返回对象，如果查询不到返回None
# User.query.all() #查询所有
# User.query.filter_by(username='admin').first()#条件查询
# User.query.order_by(User.username).all()#排序查询
# User.query.limit(1).all()#查询1条
# User.query.get(id = 123)#精确查询

# # 4.删除
# user = User.query.get(id = 123)
# db.session.delete(user)
# db.session.commit()