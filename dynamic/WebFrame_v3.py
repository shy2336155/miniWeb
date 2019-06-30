''' 在frame 文件中定义一个函数 , 用来接收服务器传过来的访问地址，并返回响应数据 '''
import re
def application(environ, start_response):

    # 从字典中将 访问地址取出来
    file_name = environ['PATH_INFO']

    # 通过取出的地址来找到对应的数据
    if file_name == '/index.py':
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


    elif file_name == '/center.py':

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


    else:
        file_content = '<h1>Other Page Run ...</h1>'

    # 执行传入函数，进行回调，将响应状态码和响应头信息返回服务
    start_response('200 OK', [('Content-Type', 'text/html')])

    # 返回 body 数据
    return file_content


