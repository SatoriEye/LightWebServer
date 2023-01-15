from flask import Flask,session,g
import config
from exts import db
from flask_migrate import Migrate
from blueprints import user_bp
from models import UserModel
from flask_cors import CORS

app = Flask(__name__)
# 配置
app.config.from_object(config)
cors = CORS(app)
# 绑定数据库
db.init_app(app)
migrate = Migrate(app, db)



app.register_blueprint(user_bp)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # 给全局绑定一个user的变量，它的值是user这个变量
            g.user = user
        except:
            g.user = None


@app.context_processor
def context_processeer():
    if hasattr(g, 'user'):
        return {"user": g.user}
    else:
        return {}

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    CORS(app)
