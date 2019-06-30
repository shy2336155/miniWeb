''' 在frame 文件中定义一个函数 , 用来接收服务器传过来的访问地址，并返回响应数据 '''

def application(file_name):# /index.py

    # 通过接收的地址来找到对应的数据
    if file_name == '/index.py':
        body = '<h1>Index Page Run v1...</h1>'
    elif file_name == '/center.py':
        body = '<h1>Center Page Run ...</h1>'
    else:
        body = '<h1>Other Page Run ...</h1>'
    # 返回 body 数据
    return body
