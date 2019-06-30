''' 在frame 文件中定义一个函数 , 用来接收服务器传过来的访问地址，并返回响应数据 '''

def application(environ, start_response):

    # 从字典中将 访问地址取出来
    file_name = environ['PATH_INFO']

    # 通过取出的地址来找到对应的数据
    if file_name == '/index.py':
        body = '<h1>Index Page Run v2...</h1>'
    elif file_name == '/center.py':
        body = '<h1>Center Page Run ...</h1>'
    else:
        body = '<h1>Other Page Run ...</h1>'

    # 执行传入函数，进行回调，将响应状态码和响应头信息返回服务
    start_response('200 OK', [('Content-Type', 'text/html')])

    # 返回 body 数据
    return body


