''' 在frame 文件中定义一个函数 , 用来接收服务器传过来的访问地址，并返回响应数据 '''
import re

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

@router('/center.py')
def center():
    # 拼接模板路径
    path = './templates/center.html'
    # 读取模块文件内容
    with open(path, 'r') as f:
        file_content = f.read()

    # 准备假数据
    row_str = """ 
             <tr>
                 <td>000426</td>
                 <td>兴业矿业</td>
                 <td>0.41%</td>
                 <td>2.17%</td>
                 <td>9.71</td>
                 <td>9.67</td>
                 <td>今天的涨幅不错,希望每天如此</td>
                 <td>
                     <a type="button" class="btn btn-default btn-xs" href="/update/000426.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
                 </td>
                 <td>
                     <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="000426">
                 </td>
             </tr> """
    all_data = ''
    for i in range(5):
        all_data += row_str

    # 替换模板文件中的占位符
    file_content = re.sub(r'\{%content%\}', all_data, file_content)
    return file_content

@router('/index.py')
def index():
    # 拼接模块文件的路径
    path = './templates/index.html'
    # 读取模板文件中的内容
    with open(path, 'r') as f:
        file_content = f.read()

    # 准备一条假数据
    row_str = """ 
                <tr>
                    <td>1</td>
                    <td>000007</td>
                    <td>全新好</td>
                    <td>10.01%</td>
                    <td>4.40%</td>
                    <td>16.05</td>
                    <td>14.60</td>
                    <td>2017-07-18</td>
                    <td>
                        <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="000007">
                    </td>
                </tr>  """
    # 多准备几条数据
    all_data = ''
    for i in range(50):
        all_data += row_str

    # 替换模板文件中的占位变量
    file_content = re.sub(r'\{%content%\}', all_data, file_content)
    return file_content

@router('/login.py')
def login():
    return 'Login Page Run ....'


