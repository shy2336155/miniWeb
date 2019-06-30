"""
在frame 文件中定义一个函数 , 用来接收服务器传过来的访问地址，并返回响应数据
"""

import re
from pymysql import *

# 准备一个空的路由字典，用来保存访问地址和功能函数的对应关系，由装饰器自动进行添加键值关系
router_table = {}


def application(environ, start_response):

    # 从字典中将 访问地址取出来
    file_name = environ['PATH_INFO']

    # 查找对应函数
    # 先给一个默认的函数
    func = other

    # 根据传入的地址，来到路由表中去找到对应的函数
    if file_name in router_table:
        func = router_table[file_name]

    # 执行得到的对应的功能函数
    file_content = func()

    # 执行传入函数，进行回调，将响应状态码和响应头信息返回服务
    start_response('200 OK', [('Content-Type', 'text/html')])

    # 返回 body 数据
    return file_content


# 定义一个带参数的装饰器
def router(url_path):
    def set_func(func):
        def wrapper(*args, **kwargs):
            print('装饰语句...')
            return func(*args, **kwargs)

        # 将内函数和访问地址加入到路由表中去
        router_table[url_path] = wrapper
        return wrapper
    return set_func


# 因为这个函数是用来匹配所有不存在页面的函数，所以不能加一个固定的路径
def other():
    file_content = '<h1>Other Page Run ... v6</h1>'
    return file_content


@router('/center.html')
def center():
    # 拼接模板路径
    path = './templates/center.html'
    # 读取模块文件内容
    with open(path, 'r') as f:
        file_content = f.read()

    # 准备假数据
    row_str = """ 
             <tr>
                 <td>%s</td>
                 <td>%s</td>
                 <td>%s</td>
                 <td>%s</td>
                 <td>%s</td>
                 <td>%s</td>
                 <td>%s</td>
                 <td>
                     <a type="button" class="btn btn-default btn-xs" href="/update/000426.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
                 </td>
                 <td>
                     <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="000426">
                 </td>
             </tr> 
             """

    conn = Connection(host='localhost', port=3306, user='root', password='123123', database='stock_db', charset='utf8')
    cur = conn.cursor()
    sql_str = ''' select info.code,info.short,info.chg,info.turnover,info.price,info.highs,focus.note_info from focus inner join info on focus.info_id = info.id '''
    cur.execute(sql_str)
    result = cur.fetchall()
    cur.close()
    conn.close()

    all_data = ''
    for t in result:
        all_data += row_str % (t[0], t[1], t[2], t[3], t[4], t[5], t[6])

    # 替换模板文件中的占位符
    file_content = re.sub(r'\{%content%\}', all_data, file_content)
    return file_content


@router('/index.html')
def index():
    # 拼接模块文件的路径
    path = './templates/index.html'
    # 读取模板文件中的内容
    with open(path, 'r') as f:
        file_content = f.read()

    # 准备一条假数据
    row_str = """ 
                <tr>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>
                        <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="%s">
                    </td>
                </tr>  """
    
    # 从数据库中读取数据
    conn = Connection(host='localhost', port=3306, user='root', password='123123', database='stock_db', charset='utf8')
    cur = conn.cursor()
    sql_str = ''' select * from info'''
    cur.execute(sql_str)
    result = cur.fetchall()
    cur.close()
    conn.close()

    # 多准备几条数据
    all_data = ''
    for t in result:
        all_data += row_str % (t[0],t[1],t[2],t[3],t[4],t[5],t[6],t[7],t[1])
        # <td>%s</td> <td>%s</td>  % t

    # 替换模板文件中的占位变量
    file_content = re.sub(r'\{%content%\}', all_data, file_content)
    return file_content


@router('/login.html')
def login():
    return 'Login Page Run ....'


