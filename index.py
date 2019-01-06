from flask import Flask, request,jsonify, json, render_template,redirect, url_for, Response, current_app , make_response
from werkzeug.utils import secure_filename  
import os, string, requests
import base64,pymysql
from app import db
from models import db,Uploads,FaceObject,ObjRelation,HostInfo,Stutest
from flask_cors import *
import operator,logging,threading
from contextlib import contextmanager
from datetime import datetime
from time import ctime,sleep
import time
# from gevent.wsgi import WSGIServer
 
app = Flask(__name__)  
# app.config['UPLOAD_FOLDER'] = 'static/uploads/'  
# app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])
 
# For a given file, return whether it's an allowed type or not
# def allowed_file(filename):  
	# return '.' in filename and \
		# filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
 
 #support chinese view 
 
# import contextlib
app.config['JSON_AS_ASCII']=False
# logging.basicConfig(filename="C:\\flaskLog\\log.txt",format='%(asctime)s-%(name)s-%(levelname)s-%(message)s')




#定义上下文管理器，连接后自动关闭连接
@contextmanager
def mysql(host='localhost', port=3306, user='root', passwd='123456', db='schoolsh002',charset='utf8'):
	conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
	cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
	try:
		yield cursor
	finally:
		conn.commit()
		cursor.close()
		conn.close()


# db1=pymysql.connect("localhost","root","123456","schoolsh001")
# cursor=db1.cursor()
# cursor.execute("select * from parent")
# data=cursor.fetchone()
# data1=data[3]
# print(data1)
# db1.commit()
# cursor.close()
# db1.close()
 
@app.route('/hello', methods=['POST','GET'])
def hello():  
		print (request.headers)	
		try:
			val=request.form.get('msgId')
			if val=='4':
				print(val)
				return jsonify({'msgId':'8','code':'0', 'message':'success'})
		except Exception as e:
			print('error:',e)
		else:
			return jsonify({'msgId':'8','code':'1', 'message':'success'})
		finally:
			# stuId1='27'
			id='27'
			
			with mysql() as cursor:
				print(cursor)
				username = cursor.execute("select parent_name from(select parent_id from schoolsh001.parent_to_student where student_id =%s)as a join schoolsh001.parent as b on a.parent_id = b.userid",(id))
				data = cursor.fetchall()
				print(data)
				# return "successCallback"+"("+json.dumps(data)+")"
				for name in data:
					if name['parent_name'] !='':
						print(name['parent_name'])
						str='收到消息孩子被家长接走了'
						url='http://127.0.0.1:8080/WebReport/ReportServer?cmd=send_messages&op=fs_mobile_main'
						stuId1='27'
						pid='dpt'
						sid='schoolsh001'
						data={'user':name['parent_name'],'text':str,'url':'http://47.98.107.94:8080/WebReport/ReportServer?reportlet=schoolmain%2Fparent%2F%5B51fa%5D%5B5165%5D%5B8bb0%5D%5B5f55%5D%5B67e5%5D%5B8be2%5D%5B76f4%5D%5B63a5%5D%5B67e5%5D%5B770b%5D%5B7248%5D.cpt&op=write&stuId='+stuId1+'&pat_id='+pid+'&dbname='+sid}
						r=requests.post(url,json=data)
						# return jsonify({'msgId':'7','code':'0','message':'sendmessage ok'})
						
				
				

			# conn.commit()
			# cursor.close()
			# conn.close() 
@app.route('/stutest', methods=['POST','GET'])
def stutest():
	try:
		print (request.headers)	
		print(request.form)
		msgId1=request.form.get('msgId')
		print(msgId1)
		schoolId1=request.form.get('schoolId')
		print(schoolId1)
		inOutType1=request.form.get('inOutType')
	
	
		stuId1=request.form.get('stuId')
		
		
		
		patId1=request.form.get('patId')
		stuImage1=request.form.get('stuImage')
		patImage1=request.form.get('patImage')
		time1=request.form.get('time')
		timeStamp1=request.form.get('timeStamp')
		
		stutest1=Stutest(msgId=msgId1,schoolId=schoolId1,stuId=stuId1,patId=patId1,inOutType=inOutType1,stuImage=stuImage1,patImage=patImage1,time=time1,timeStamp=timeStamp1,flag=0)
		db.session.add(stutest1)
		db.session.commit()
		
	except:
		db.session.rollback()
		rasise
	finally:
		return jsonify({'msgId':'30','code':'0', 'message':'success','stuImage':stuImage1,'patImage':patImage1,'stuId':stuId1,'patId':patId1})

		
			
	
@app.route('/message', methods=['POST','GET'])
def message():
	# return 'okokok'
	if request.method=='POST':
		print (request.headers)	
		print(request.form.get('msgId'))
		msgid1=int(request.form.get('msgId'))
		# msgid1=1
		if msgid1==1:#judge msgId is 1
			print(request.form.get('msgId'))
			print(request.form.get('schoolId'))
			print(request.form.get('hostInfo'))
			
			
			# hostdata=json.loads(request.form.get('hostInfo'))
			# print(hostdata)
			# ip1=hostdata['ip']
			# mac1=hostdata['mac']
			
			global schoolid
			schoolid=request.form.get('schoolId')
			print(schoolid)
			
			# hostInfo1=HostInfo(ip=ip1,mac=mac1,schoolId=schoolid,time=datetime.now())
			# db.session.add(hostInfo1)
			# db.session.commit()
			
			
			return redirect(url_for('faceobjects'))
			
		if msgid1==6:
			print (request.headers)	
			print(request.form.get('msgId'))
			print(request.form.get('schoolId'))
			print(request.form.get('code'))
			recode=request.form.get('code')
			if recode=='0':
				print(request.form.get('successList'))
				print(request.form.get('failedList'))
				data=json.loads(request.form.get('successList'))
				
				for i in range(len(data)):
					print(data[i]['stuId'])
					db.session.query(ObjRelation).filter_by(stuId=data[i]['stuId']).delete()
					db.session.commit()
				return jsonify({'msgId':'2','code':'0'})
			else:
				return jsonify({'msgId':'2','code':'1','message':'分析主机故障'})
		
			
		if msgid1==4:
			print (request.headers)	
			print(request.form.get('msgId'))
			print(request.form.get('schoolId'))
			print(request.form.get('code'))
			recode=request.form.get('code')
			if recode=='0':
				print(request.form.get('success'))
				print(request.form.get('failed'))
				data=json.loads(request.form.get('success'))
				
				for i in range(len(data)):
					print(data[i]['objId'])
					db.session.query(FaceObject).filter_by(objId=data[i]['objId']).delete()
					db.session.commit()
				return redirect(url_for('objectrelation'))
				
				# return jsonify({'msgId':'2','code':'0'})
			else:
				return jsonify({'msgId':'2','code':'1','message':'分析主机故障'})
			
		# else:
			# return 'request msgId  error!'
	
		
		# if msgid1==7:
			# print(request.form)
			# schoolId1=request.form.get('schoolId')
			# print(schoolId1)
			
			# data=json.loads(request.form.get('inOutRecord'))
			
			# inOutType1=data['inOutType']
			# print(inOutType1)
			
			# stuId1=data['stuId']
			# patId1=data['patId']
			# stuImage1=data['stuImage'].replace(' ','+')
			# patImage1=data['patImage'].replace(' ','+')
			# time1=data['time']
			# timeStamp1=data['timeStamp']
			
			# global upload1
			# upload1=Uploads(msgId=msgId1,schoolId=schoolId1,stuId=stuId1,patId=patId1,inOutType=inOutType1,stuImage=stuImage1,patImage=patImage1,time=time1,timeStamp=timeStamp1)
			# try:
				# db.session.add(upload1)
				# return jsonify({'msgId':'8','code':'0', 'message':'success'})	 
			# finally:
				# db.session.commit()
			
		# return 'hello word'
	else:
		return jsonify({'method':'error'})


@app.route('/faceobjects', methods=['POST','GET'])
def faceobjects(): 
	# faceobjects=db.session.query(FaceObject).all()
	print (request.headers)
	# print(faceobjects)
	global renumber
	
	renumber=db.session.query(FaceObject).filter_by(schoolId=schoolid).count()
	print(renumber)
	objrenumber=db.session.query(ObjRelation).filter_by(schoolId=schoolid).count()
	print(objrenumber)
	
	if renumber!=0:
		
		faceObject1=db.session.query(FaceObject).filter_by(schoolId=schoolid).all()
		print(faceObject1)
		objectList=[]
		# faceObject2={}
		for i in range(len(faceObject1)):
		# dataType1=faceObject1.dataType
			
			schoolId1=faceObject1[i].schoolId
			objId1=faceObject1[i].objId
			patId1=faceObject1[i].patId
			objName1=faceObject1[i].objName
			objType1=faceObject1[i].objType
			objClass1=faceObject1[i].objClass
			objSex1=faceObject1[i].objSex
			objAge1=faceObject1[i].objAge
			objPhone1=faceObject1[i].objPhone
			objAddr1=faceObject1[i].objAddr
			# objImage1=faceObject1[i].objImage
			objImage1=str(base64.b64encode(faceObject1[i].objImage),'utf-8')
			# print(objImage1)
			# relImage1=str(base64.b64encode(faceObject1.relImage),'utf-8')
			
			
			# objectList=[]
			imageList1=[]
			
			# imageList1.append({'objImage':objImage1},{'relImage':relImage1})
			imageList1.append({'objImage':objImage1})
			objectList.append({'objId':objId1,'patId':patId1,'objName':objName1,'objType':objType1,'objClass':objClass1,'objSex':objSex1,'objAge':objAge1,'objPhone':objPhone1,'objAddr':objAddr1,'imageList':imageList1})
			
		faceObject2={'msgId':'3','schoolId':schoolId1,'objectList':objectList}
			
			# dateType1=1
			# db.session.commit()
		return jsonify(faceObject2),200
	# elif objrenumber!=0:
		# return redirect(url_for('objectrelation'))
	else:
		# return jsonify({'msgId':'2','message':'no record in database'})
		return redirect(url_for('objectrelation'))
	
	#delrecord=db.session.delete(FaceObject).one()
	#print(delrecord)
	
	
	
	
	
@app.route('/objectrelation', methods=['POST','GET'])
def objectrelation():
	print(request.headers)
	objrenumber=db.session.query(ObjRelation).filter_by(schoolId=schoolid).count()
	print(objrenumber)
	if objrenumber!=0:
		objrelation1=db.session.query(ObjRelation).filter_by(schoolId=schoolid).all()
		print(objrelation1)
		forelationList=[]
		objrelation2={}	
		for i in range(len(objrelation1)):	
			schoolId1=objrelation1[i].schoolId
			stuId1=objrelation1[i].stuId
			patId1=objrelation1[i].patId
			
			forelationList.append({'stuId':stuId1,'patId':patId1})
			
			objrelation2={'msgId':'5','schoolId':schoolId1,'forelationList':forelationList}
		return jsonify(objrelation2)
	else:
		return jsonify({'msgId':'2','code':'0'})
		
 
@app.route('/upload', methods=['POST','GET'])
def upload():  
	
	if request.method=='POST': 
		print (request.headers)	
		# print(request.form)
		msgId1=request.form.get('msgId')
		
		print(msgId1)
		
		schoolId1=request.form.get('schoolId')
		
		data=json.loads(request.form.get('inOutRecord'))
		
		inOutType1=data['inOutType']
		print(inOutType1)
	
	
		stuId1=data['stuId']
		
		
		patId1=data['patId']
		stuImage1=data['stuImage'].replace(' ','+')
		patImage1=data['patImage'].replace(' ','+')
		time1=data['time']
		timeStamp1=data['timeStamp']
		
		
		try:
			upload1=Uploads(msgId=msgId1,schoolId=schoolId1,stuId=stuId1,patId=patId1,inOutType=inOutType1,stuImage=stuImage1,patImage=patImage1,time=time1,timeStamp=timeStamp1,flag=0)
			db.session.add(upload1)
			db.session.commit()
			
		except:
			db.session.rollback()
			rasise
		finally:
			return jsonify({'msgId':'8','code':'0', 'message':'success'})
		
			# if inOutType1==0:		
				
				# if patId1=='':	
					# sid=schoolId1
					# print(sid)
					# with mysql(host='localhost', port=3306, user='root', passwd='123456', db=schoolId1,charset='utf8') as cursor:
						# print(cursor)
						# username = cursor.execute("select parent_name from(select parent_id from "+sid+".parent_to_student where student_id =%s)as a join "+sid+".parent as b on a.parent_id = b.userid",(stuId1[3:]))
						# data = cursor.fetchall()
						# teaname1=cursor.execute("select username from(select classteacher_id from(select class_id from "+sid+".student where id = "+stuId1[3:]+")as a join "+sid+".class_to_classteacher as b on a.class_id = b.class_id)as c join fr_server.fr_t_user as d on c.classteacher_id = d.id")
						# teadata=cursor.fetchall()
						# print(data)
						# print(teadata)		
						# for name in data:
							# if name['parent_name'].strip():
								# print(name['parent_name'])
								# str='孩子进校了'
								# url='http://127.0.0.1:8080/WebReport/ReportServer?cmd=send_messages&op=fs_mobile_main'	
								# data={'user':name['parent_name'],'text':str,'url':'http://47.98.107.94:8080/WebReport/ReportServer?reportlet=schoolmain%2Fparent%2F%5B51fa%5D%5B5165%5D%5B8bb0%5D%5B5f55%5D%5B67e5%5D%5B8be2%5D%5B76f4%5D%5B63a5%5D%5B67e5%5D%5B770b%5D%5B7248%5D.cpt&op=write&stuId='+stuId1[3:]+'&dbname='+sid}
								# r=requests.post(url,json=data)
								# print('ok0')		
						# for teaname in teadata:
							# if teaname['username'] !='':
								# print(teaname['username'])
								# str='孩子进校了'
								# url='http://127.0.0.1:8080/WebReport/ReportServer?cmd=send_messages&op=fs_mobile_main'
											
								# data={'user':teaname['username'],'text':str,'url':'http://47.98.107.94:8080/WebReport/ReportServer?reportlet=schoolmain%2Fparent%2F%5B51fa%5D%5B5165%5D%5B8bb0%5D%5B5f55%5D%5B67e5%5D%5B8be2%5D%5B76f4%5D%5B63a5%5D%5B67e5%5D%5B770b%5D%5B7248%5D.cpt&op=write&stuId='+stuId1[3:]+'&dbname='+sid}
								# r=requests.post(url,json=data)
								# print('ok2')
								# return jsonify({'msgId':'8','code':'0', 'message':'success'})
				# else:
					# sid=schoolId1
					# print(sid)
					# with mysql(host='localhost', port=3306, user='root', passwd='123456', db=schoolId1,charset='utf8') as cursor:
						# print(cursor)
						# teaname1=cursor.execute("select username from(select classteacher_id from(select class_id from(select student_id from "+sid+".parent_to_student where parent_id = "+patId1[3:]+") as a join "+sid+".student as b on a.student_id = b.id)as c join "+sid+".class_to_classteacher as d on c.class_id = d.class_id)as e join fr_server.fr_t_user as f on e.classteacher_id = f.id")
						# teadata=cursor.fetchall()
						# print(teadata)
						# for teaname in teadata:
							# if teaname['username'] !='':
								# print(teaname['username'])
								# str='家长进校了'
								# url='http://127.0.0.1:8080/WebReport/ReportServer?cmd=send_messages&op=fs_mobile_main'
											
								# data={'user':teaname['username'],'text':str,'url':'http://47.98.107.94:8080/WebReport/ReportServer?reportlet=schoolmain%2Fclassteacher%2F%5B5bb6%5D%5B957f%5D%5B5165%5D%5B6821%5D%5B67e5%5D%5B8be2%5D.cpt&patId='+patId1[3:]+'&dbname='+sid}
								# r=requests.post(url,json=data)
								# print ('ok3')
								# return jsonify({'msgId':'8','code':'0', 'message':'success'})
			# if inOutType1==1:
				
				# if patId1=='':
					# sid=schoolId1
					# print(sid)
					# print(patId1)
					# with mysql() as cursor:
						# print(cursor)
						# username = cursor.execute("select parent_name from(select parent_id from "+sid+".parent_to_student where student_id =%s)as a join "+sid+".parent as b on a.parent_id = b.userid",(stuId1[3:]))
						# usrdata = cursor.fetchall()		
						# print(usrdata)
						# for name in usrdata:
							# if name['parent_name'] !='':
								# print(name['parent_name'])
								# str='孩子单独出校'
								# url='http://127.0.0.1:8080/WebReport/ReportServer?cmd=send_messages&op=fs_mobile_main'
										
								# data={'user':name['parent_name'],'text':str,'url':'http://47.98.107.94:8080/WebReport/ReportServer?reportlet=schoolmain%2Fparent%2F%5B51fa%5D%5B5165%5D%5B8bb0%5D%5B5f55%5D%5B67e5%5D%5B8be2%5D%5B76f4%5D%5B63a5%5D%5B67e5%5D%5B770b%5D%5B7248%5D.cpt&op=write&stuId='+stuId1[3:]+'&dbname='+sid}
								
								# r=requests.post(url,json=data)
								# print('ok4')
						
						# teaname=cursor.execute("select username from(select classteacher_id from(select class_id from "+sid+".student where id = "+stuId1[3:]+")as a join "+sid+".class_to_classteacher as b on a.class_id = b.class_id)as c join fr_server.fr_t_user as d on c.classteacher_id = d.id")
						# teadata=cursor.fetchall()
						# print(teadata)
						# for teaname in teadata:
							# if teaname['username'] !='':
							
							
								# print(teaname['username'])
								# str='孩子单独出校'
								# url='http://127.0.0.1:8080/WebReport/ReportServer?cmd=send_messages&op=fs_mobile_main'		
								# data={'user':teaname['username'],'text':str,'url':'http://47.98.107.94:8080/WebReport/ReportServer?reportlet=schoolmain%2Fparent%2F%5B51fa%5D%5B5165%5D%5B8bb0%5D%5B5f55%5D%5B67e5%5D%5B8be2%5D%5B76f4%5D%5B63a5%5D%5B67e5%5D%5B770b%5D%5B7248%5D.cpt&op=write&stuId='+stuId1[3:]+'&dbname='+sid}
								# r=requests.post(url,json=data)
								# print('ok6')
								
						# adminname=cursor.execute("select username from (select * from fr_server.fr_t_user where project = '"+sid+"')as a join fr_server.fr_t_customrole_user as b on a.id = b.Userid where customRoleId = 3")
						# admdata = cursor.fetchall()
						# print(admdata)
						# for admname in admdata:
							# if admname['username'] !='':
								# print(admname['username'])	
								# str='孩子单独出校'
								# url='http://127.0.0.1:8080/WebReport/ReportServer?cmd=send_messages&op=fs_mobile_main'
								# data={'user':admname['username'],'text':str,'url':'http://47.98.107.94:8080/WebReport/ReportServer?reportlet=schoolmain%2Fparent%2F%5B51fa%5D%5B5165%5D%5B8bb0%5D%5B5f55%5D%5B67e5%5D%5B8be2%5D%5B76f4%5D%5B63a5%5D%5B67e5%5D%5B770b%5D%5B7248%5D.cpt&op=write&stuId='+stuId1[3:]+'&dbname='+sid}
								# r=requests.post(url,json=data)
								# print('ok5')
								# return jsonify({'msgId':'8','code':'0', 'message':'success'})
						
					
				# else:
					# sid=schoolId1
					# with mysql() as cursor:
						# print(cursor)
						# username = cursor.execute("select parent_name from(select parent_id from "+sid+".parent_to_student where student_id =%s)as a join "+sid+".parent as b on a.parent_id = b.userid",(stuId1[3:]))
						# data = cursor.fetchall()
						# teaname=cursor.execute("select username from(select classteacher_id from(select class_id from "+sid+".student where id = "+stuId1[3:]+")as a join "+sid+".class_to_classteacher as b on a.class_id = b.class_id)as c join fr_server.fr_t_user as d on c.classteacher_id = d.id")
						# teadata=cursor.fetchall()
						
						# print(data)
						# for name in data:
							# if name['parent_name'] !='':
								# print(name['parent_name'])
								# str='孩子有家长陪同'
								# url='http://127.0.0.1:8080/WebReport/ReportServer?cmd=send_messages&op=fs_mobile_main'	
								# data={'user':name['parent_name'],'text':str,'url':'http://47.98.107.94:8080/WebReport/ReportServer?reportlet=schoolmain%2Fparent%2F%5B51fa%5D%5B5165%5D%5B8bb0%5D%5B5f55%5D%5B67e5%5D%5B8be2%5D%5B76f4%5D%5B63a5%5D%5B67e5%5D%5B770b%5D%5B7248%5D.cpt&op=write&stuId='+stuId1[3:]+'&dbname='+sid}
								# r=requests.post(url,json=data)
								
						# print(teadata)
						# for teaname in teadata:
							# if teaname['username'] !='':
								# print(teaname['username'])
								# str='孩子有家长陪同'
								# url='http://127.0.0.1:8080/WebReport/ReportServer?cmd=send_messages&op=fs_mobile_main'
										
								# data={'user':teaname['username'],'text':str,'url':'http://47.98.107.94:8080/WebReport/ReportServer?reportlet=schoolmain%2Fparent%2F%5B51fa%5D%5B5165%5D%5B8bb0%5D%5B5f55%5D%5B67e5%5D%5B8be2%5D%5B76f4%5D%5B63a5%5D%5B67e5%5D%5B770b%5D%5B7248%5D.cpt&op=write&stuId='+stuId1[3:]+'&dbname='+sid}
								# r=requests.post(url,json=data)
								# print('ok8')
								
						
								# print('ok7')
								# return jsonify({'msgId':'8','code':'0', 'message':'success'})
						# for teaname in teadata:
							# if teaname['username'] !='':
								# print(teaname['username'])
								# str='孩子有家长陪同'
								# url='http://127.0.0.1:8080/WebReport/ReportServer?cmd=send_messages&op=fs_mobile_main'
										
								# data={'user':teaname['username'],'text':str,'url':'http://47.98.107.94:8080/WebReport/ReportServer?reportlet=schoolmain%2Fparent%2F%5B51fa%5D%5B5165%5D%5B8bb0%5D%5B5f55%5D%5B67e5%5D%5B8be2%5D%5B76f4%5D%5B63a5%5D%5B67e5%5D%5B770b%5D%5B7248%5D.cpt&op=write&stuId='+stuId1[3:]+'&dbname='+sid}
								# r=requests.post(url,json=data)
								# print('ok8')
								# return jsonify({'msgId':'8','code':'0', 'message':'success'})
		
			
	else:			
		return jsonify({'method':'error'})

#@app.route('/sendmess', methods=['POST','GET'])
def sendmess(): 
	
	while True:
		upnumber=db.session.query(Uploads).filter_by(flag=0).count()
		print(upnumber)
		if upnumber!=0:
			uprecord=db.session.query(Uploads).filter_by(flag=0).all()
			print(uprecord)
			for i in range(len(uprecord)):
				inOutType1=uprecord[i].inOutType
				schoolId1=uprecord[i].schoolId
				stuId1=uprecord[i].stuId
				patId1=uprecord[i].patId
				uprecord[i].flag=1
				db.session.commit()
				if inOutType1==0:		
							
					if patId1=='':	
						sid=schoolId1
						print(sid)
						with mysql(host='localhost', port=3306, user='root', passwd='123456', db=schoolId1,charset='utf8') as cursor:
							print(cursor)
							username = cursor.execute("select parent_name from(select parent_id from "+sid+".parent_to_student where student_id =%s)as a join "+sid+".parent as b on a.parent_id = b.userid",(stuId1[3:]))
							data = cursor.fetchall()
							teaname1=cursor.execute("select username from(select classteacher_id from(select class_id from "+sid+".student where id = "+stuId1[3:]+")as a join "+sid+".class_to_classteacher as b on a.class_id = b.class_id)as c join fr_server.fr_t_user as d on c.classteacher_id = d.id")
							teadata=cursor.fetchall()
							print(data)
							print(teadata)		
							for name in data:
								if name['parent_name'] !='':
									print(name['parent_name'])
									str='孩子进校了'
									url='http://127.0.0.1:8080/WebReport/ReportServer?cmd=send_messages&op=fs_mobile_main'
											
											
									data={'user':name['parent_name'],'text':str,'url':'http://47.98.107.94:8080/WebReport/ReportServer?reportlet=schoolmain%2Fparent%2F%5B51fa%5D%5B5165%5D%5B8bb0%5D%5B5f55%5D%5B67e5%5D%5B8be2%5D%5B76f4%5D%5B63a5%5D%5B67e5%5D%5B770b%5D%5B7248%5D.cpt&op=write&stuId='+stuId1[3:]+'&dbname='+sid}
									r=requests.post(url,json=data)
									print('ok0')
									
							for teaname in teadata:
								if teaname['username'] !='':
									print(teaname['username'])
									str='孩子进校了'
									url='http://127.0.0.1:8080/WebReport/ReportServer?cmd=send_messages&op=fs_mobile_main'
												
									data={'user':teaname['username'],'text':str,'url':'http://47.98.107.94:8080/WebReport/ReportServer?reportlet=schoolmain%2Fparent%2F%5B51fa%5D%5B5165%5D%5B8bb0%5D%5B5f55%5D%5B67e5%5D%5B8be2%5D%5B76f4%5D%5B63a5%5D%5B67e5%5D%5B770b%5D%5B7248%5D.cpt&op=write&stuId='+stuId1[3:]+'&dbname='+sid}
									r=requests.post(url,json=data)
									print('ok1')
							# return jsonify({'msgId':'8','code':'0', 'message':'success'})
					else:
						sid=schoolId1
						print(sid)
						with mysql(host='localhost', port=3306, user='root', passwd='123456', db=schoolId1,charset='utf8') as cursor:
							print(cursor)
							teaname1=cursor.execute("select username from(select classteacher_id from(select class_id from(select student_id from "+sid+".parent_to_student where parent_id = "+patId1[3:]+") as a join "+sid+".student as b on a.student_id = b.id)as c join "+sid+".class_to_classteacher as d on c.class_id = d.class_id)as e join fr_server.fr_t_user as f on e.classteacher_id = f.id")
							teadata=cursor.fetchall()
							print(teadata)
							for teaname in teadata:
								if teaname['username'] !='':
									print(teaname['username'])
									str='家长进校了'
									url='http://127.0.0.1:8080/WebReport/ReportServer?cmd=send_messages&op=fs_mobile_main'
												
									data={'user':teaname['username'],'text':str,'url':'http://47.98.107.94:8080/WebReport/ReportServer?reportlet=schoolmain%2Fclassteacher%2F%5B5bb6%5D%5B957f%5D%5B5165%5D%5B6821%5D%5B67e5%5D%5B8be2%5D.cpt&patId='+patId1[3:]+'&dbname='+sid}
									r=requests.post(url,json=data)
									print ('ok3')
							# return jsonify({'msgId':'8','code':'0', 'message':'success'})
				if inOutType1==1:
					
					if patId1=='':
						sid=schoolId1
						print(sid)
						print(patId1)
						with mysql() as cursor:
							print(cursor)
							username = cursor.execute("select parent_name from(select parent_id from "+sid+".parent_to_student where student_id =%s)as a join "+sid+".parent as b on a.parent_id = b.userid",(stuId1[3:]))
							usrdata = cursor.fetchall()
							adminname=cursor.execute("select username from (select * from fr_server.fr_t_user where project = '"+sid+"')as a join fr_server.fr_t_customrole_user as b on a.id = b.Userid where customRoleId = 3")
							admdata = cursor.fetchall()
							teaname=cursor.execute("select username from(select classteacher_id from(select class_id from "+sid+".student where id = "+stuId1[3:]+")as a join "+sid+".class_to_classteacher as b on a.class_id = b.class_id)as c join fr_server.fr_t_user as d on c.classteacher_id = d.id")
							teadata=cursor.fetchall()
							
							print(usrdata)
							print(admdata)
							print(teadata)

							for name in usrdata:
								if name['parent_name'] !='':
									print(name['parent_name'])
									str='孩子单独出校'
									url='http://127.0.0.1:8080/WebReport/ReportServer?cmd=send_messages&op=fs_mobile_main'
											
									data={'user':name['parent_name'],'text':str,'url':'http://47.98.107.94:8080/WebReport/ReportServer?reportlet=schoolmain%2Fparent%2F%5B51fa%5D%5B5165%5D%5B8bb0%5D%5B5f55%5D%5B67e5%5D%5B8be2%5D%5B76f4%5D%5B63a5%5D%5B67e5%5D%5B770b%5D%5B7248%5D.cpt&op=write&stuId='+stuId1[3:]+'&dbname='+sid}
									
									r=requests.post(url,json=data)
									print('ok4')
									
							
										
							for admname in admdata:
								if admname['username'] !='':
									print(admname['username'])	
									str='孩子单独出校'
									url='http://127.0.0.1:8080/WebReport/ReportServer?cmd=send_messages&op=fs_mobile_main'
											
									data={'user':admname['username'],'text':str,'url':'http://47.98.107.94:8080/WebReport/ReportServer?reportlet=schoolmain%2Fparent%2F%5B51fa%5D%5B5165%5D%5B8bb0%5D%5B5f55%5D%5B67e5%5D%5B8be2%5D%5B76f4%5D%5B63a5%5D%5B67e5%5D%5B770b%5D%5B7248%5D.cpt&op=write&stuId='+stuId1[3:]+'&dbname='+sid}
									r=requests.post(url,json=data)
									print('ok5')
								
							for teaname in teadata:
								if teaname['username'] !='':
									print(teaname['username'])
									str='孩子单独出校'
									url='http://127.0.0.1:8080/WebReport/ReportServer?cmd=send_messages&op=fs_mobile_main'
											
									data={'user':teaname['username'],'text':str,'url':'http://47.98.107.94:8080/WebReport/ReportServer?reportlet=schoolmain%2Fparent%2F%5B51fa%5D%5B5165%5D%5B8bb0%5D%5B5f55%5D%5B67e5%5D%5B8be2%5D%5B76f4%5D%5B63a5%5D%5B67e5%5D%5B770b%5D%5B7248%5D.cpt&op=write&stuId='+stuId1[3:]+'&dbname='+sid}
									r=requests.post(url,json=data)
									print('ok6')
							
							# return jsonify({'msgId':'8','code':'0', 'message':'success'})
						
					else:
						sid=schoolId1
						with mysql() as cursor:
							print(cursor)
							# username = cursor.execute("select parent_name from(select parent_id from "+sid+".parent_to_student where student_id =%s)as a join "+sid+".parent as b on a.parent_id = b.userid",(stuId1[3:]))
							# data = cursor.fetchall()
							teaname1=cursor.execute("select username from(select classteacher_id from(select class_id from "+sid+".student where id = "+stuId1[3:]+")as a join "+sid+".class_to_classteacher as b on a.class_id = b.class_id)as c join fr_server.fr_t_user as d on c.classteacher_id = d.id")
							teadata=cursor.fetchall()
							username = cursor.execute("select parent_name from(select parent_id from "+sid+".parent_to_student where student_id =%s)as a join "+sid+".parent as b on a.parent_id = b.userid",(stuId1[3:]))
							data = cursor.fetchall()
							
							print(teadata)		
							for teaname in teadata:
								if teaname['username'] !='':
									print(teaname['username'])
									str='孩子有家长陪同'
									url='http://127.0.0.1:8080/WebReport/ReportServer?cmd=send_messages&op=fs_mobile_main'
											
									data={'user':teaname['username'],'text':str,'url':'http://47.98.107.94:8080/WebReport/ReportServer?reportlet=schoolmain%2Fparent%2F%5B51fa%5D%5B5165%5D%5B8bb0%5D%5B5f55%5D%5B67e5%5D%5B8be2%5D%5B76f4%5D%5B63a5%5D%5B67e5%5D%5B770b%5D%5B7248%5D.cpt&op=write&stuId='+stuId1[3:]+'&dbname='+sid}
									r=requests.post(url,json=data)
									print('ok8')
										
							print(data)	
							for name in data:
								if name['parent_name'] !='':
									print(name['parent_name'])
									str='孩子有家长陪同'
									url='http://127.0.0.1:8080/WebReport/ReportServer?cmd=send_messages&op=fs_mobile_main'
											
									data={'user':name['parent_name'],'text':str,'url':'http://47.98.107.94:8080/WebReport/ReportServer?reportlet=schoolmain%2Fparent%2F%5B51fa%5D%5B5165%5D%5B8bb0%5D%5B5f55%5D%5B67e5%5D%5B8be2%5D%5B76f4%5D%5B63a5%5D%5B67e5%5D%5B770b%5D%5B7248%5D.cpt&op=write&stuId='+stuId1[3:]+'&dbname='+sid}
									r=requests.post(url,json=data)
									print('ok7')
							# print(teadata)		
							# for teaname in teadata:
								# if teaname['username'] !='':
									# print(teaname['username'])
									# str='孩子有家长陪同'
									# url='http://127.0.0.1:8080/WebReport/ReportServer?cmd=send_messages&op=fs_mobile_main'
											
									# data={'user':teaname['username'],'text':str,'url':'http://47.98.107.94:8080/WebReport/ReportServer?reportlet=schoolmain%2Fparent%2F%5B51fa%5D%5B5165%5D%5B8bb0%5D%5B5f55%5D%5B67e5%5D%5B8be2%5D%5B76f4%5D%5B63a5%5D%5B67e5%5D%5B770b%5D%5B7248%5D.cpt&op=write&stuId='+stuId1[3:]+'&dbname='+sid}
									# r=requests.post(url,json=data)
									# print('ok8')
		else:
			time.sleep(0.1)
	
# threads=[]
# t1=threading.Thread(target=upload)
# threads.append(t1)
# t2=threading.Thread(target=sendmess)
# threads.append(t2)
# t2.start()
# t2=threading.Thread(target=sendmess)	
 
if __name__ == '__main__':  
	# print('sendmess start ...........')
	app.run(debug=True,threaded=True)
	# t2=threading.Thread(target=sendmess)
	# t2.start()
	# t2.join()
	# app.run(debug=True,threaded=True)
	# print(t2.isAlive())
	# print(t2.name)
	# t2.start()
	# print(' send message end')
	
	# for t in threads:
		# t.setDaemon(True)
		# t.start()
		
	# t.join()
	# print("all over %s" %ctime())
	# app.logger.name="appLogger"
	# app.logger.info("my logging")
# WSGIServer(('127.0.0.1',5000),app).serve_forever()