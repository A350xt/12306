from whole.Flask import app
from flask import request, make_response, render_template
from program.login import Route as LoginRoute
from program.search import Route as SearchRoute
from program.scheduler import Route as SchedulerRoute
from program.train_schedule import Route as TrainScheduleRoute
from plugins.get_station import Station


@app.errorhandler(Exception)
def handle_generic_error():
    return "Internal Server Error", 500


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ui/login')
def ui_login():
    """登录页面"""
    return render_template('login.html')


@app.route('/ui/search')
def ui_search():
    """车票查询页面"""
    return render_template('search.html')


@app.route('/ui/schedule')
def ui_schedule():
    """定时抢票页面"""
    return render_template('schedule.html')


@app.route('/ui/my_tickets')
def ui_my_tickets():
    """我的车票页面"""
    return render_template('index.html')


@app.route('/login/<name>', methods=['GET', 'POST'])
def login(name):
    """
    判断用户登录的类型
    :param name:
    :return:
    """
    return LoginRoute().login(name, request, make_response)


@app.route('/search', methods=['GET', 'POST'])
def search():
    """
    查询车票,车站,本人车票,车站大屏
    :return:
    """
    return SearchRoute().search(request)


@app.route('/scheduler', methods=['GET', 'POST'])
def scheduler():
    """
    定时抢票任务管理
    :return:
    """
    return SchedulerRoute().scheduler(request)


@app.route('/train_schedule', methods=['GET', 'POST'])
def train_schedule():
    """
    列车时刻表查询
    :return:
    """
    return TrainScheduleRoute().schedule(request)


@app.route('/update_station', methods=['GET', 'POST'])
def update_station():
    """
    更新车站信息
    :return:
    """
    return Station().process()


@app.route('/favicon.ico', methods=['GET', 'POST'])
def favicon():
    """
    返回favicon
    :return:
    """
    return 'favicon'
