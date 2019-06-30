#   代码实现:
import socket
import re
import multiprocessing
from dynamic import WebFrame_v5 as WebFrame

# 封装一个服务器类
class WebServer(object):
    # 重写init 方法，在init 方法中去实例socket连接
    def __init__(self):
        """用来完成整体的控制"""
        # 1. 创建套接字
        self.__tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 用来重新启用占用的端口
        self.__tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 2. 绑定IP和端口号
        self.__tcp_server_socket.bind(("", 7890))

        # 3. 设置套接字监听连接数(最大连接数)
        self.__tcp_server_socket.listen(128)

    # 实现启动服务器方法
    def start(self):
        while True:
            # 4. 等待新客户端的链接
            new_socket, client_addr = self.__tcp_server_socket.accept()

            # 5. 为连接上来的客户端去创建一个新的进程去运行
            p = multiprocessing.Process(target=self.__service_client, args=(new_socket,))
            p.start()
            # 因为新进程在创建过程中会完全复制父进程的运行环境,所以父线程中关闭的只是自己环境中的套接字对象
            # 而新进程中因为被复制的环境中是独立存在的,所以不会受到影响
            new_socket.close()

        # 关闭监听套接字
        self.__tcp_server_socket.close()

    # 再实现一个多任务处理方法
    def __service_client(self, new_socket):
        """为客户端返回数据"""

        # 1. 接收浏览器发送过来的请求 ，即http请求相关信息
        # GET / HTTP/1.1
        # .....
        request = new_socket.recv(1024).decode("utf-8")
        # 将请求头信息进行按行分解存到列表中
        request_lines = request.splitlines()
        # GET /index.html HTTP/1.1
        file_name = ""
        # 正则:  [^/]+ 不以/开头的至少一个字符 匹配到/之前
        #      (/[^ ]*) 以分组来匹配第一个字符是/,然后不以空格开始的0到多个字符,也就是空格之前
        #      最后通过匹配可以拿到 请求的路径名  比如:index.html
        ret = re.match(r"[^/]+(/[^ ]*)", request_lines[0])
        # 如果匹配结果 不为none,说明请求地址正确
        if ret:
            # 利用分组得到请求地址的文件名,正则的分组从索引1开始
            file_name = ret.group(1)
            print('FileName:  ' + file_name)
            # 如果请求地址为 / 将文件名设置为index.html,也就是默认访问首页
            if file_name == "/":
                file_name = "/index.html"

        # 加入判断，通过访问地址的后缀来判断请的数据是静态还是动态
        if file_name.endswith('.py'):
            # 要请求动态数据
            # 因为后期代码中，需要访问两个页面，在这里直接判断


            # 获取响应体中的数据
            # 准备一个字典，将访问地址存入
            env = {'PATH_INFO': file_name}
            body = WebFrame.application(env,self.start_response)

            # 响应行
            line = 'HTTP/1.1 %s \r\n' % self.__status
            # 响应头
            header = 'Server: MiniWebServer v1.0\r\n'
            # 拼接返回的响应头信息
            for t in self.__params:
                header += '%s: %s\r\n' %t


            # 将访问之后不同的数据进行拼接返回
            data = line + header + '\r\n' + body
            new_socket.send(data.encode())

        else:
            # 请求静态数据, 返回的是API文档中的数据
            # 2. 返回http格式的数据，给浏览器
            try:
                # 拼接路径,在当前的html目录下找访问的路径对应的文件进行读取
                f = open("./static" + file_name, "rb")
            except:
                # 如果没找到,拼接响应信息并返回信息
                response = "HTTP/1.1 404 NOT FOUND\r\n"
                response += "\r\n"
                response += "------file not found-----"
                new_socket.send(response.encode("utf-8"))
            else:
                # 如果找到对应文件就读取并返回内容
                html_content = f.read()
                f.close()
                # 2.1 准备发送给浏览器的数据---header
                response = "HTTP/1.1 200 OK\r\n"
                response += "\r\n"
                # 如果想在响应体中直接发送文件内的信息,那么在上面读取文件时就不能用rb模式,只能使用r模式,所以下面将响应头和响应体分开发送
                # response += html_content
                # 2.2 准备发送给浏览器的数据
                # 将response header发送给浏览器
                new_socket.send(response.encode("utf-8"))
                # 将response body发送给浏览器
                new_socket.send(html_content)

        # 关闭套接
        new_socket.close()

    # 定义一个回调函数，用来接收状态信息
    def start_response(self,status, params):
        # 什么都不做，直接将数据保存下来
        self.__status = status
        self.__params = params



def main():
    # 创建一个服务器对象
    server = WebServer()
    # 启动服务器
    server.start()

if __name__ == "__main__":
    main()