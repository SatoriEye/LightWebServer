from flask import Blueprint,request,session,jsonify
import json
from models import UserModel
from exts import db
bp = Blueprint('user', __name__, url_prefix="/user")


@bp.route('/register',methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        data = request.get_data()
        data =json.loads(data)
        name = data['name']
        email= data['email']
        password = data['password']
        user = UserModel(name=name,email=email,password=password)
        db.session.add(user)
        db.session.commit()
        message ={
            'error_code':0,
            'status':"ok"
        }
        return jsonify(message)
    else:
        error_message ={
            "error_code":1,
            "status":"请求错误"
        }
        return jsonify(error_message)


@bp.route('/login',methods = ['POST'])
def login():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        email = data['email']
        password = data['password']
        user =UserModel.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user_id'] = user.id
            message = {
                "error_code":0,
                "status":"登陆成功"
            }
            return jsonify(message)
        else:
            message = {
                "error_code": 1,
                "data": {
                    "status": "密码或用户名错误"
                }
            }
            return jsonify(message)
    else:
        return "请求错误"







