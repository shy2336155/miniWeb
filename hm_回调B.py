# ''' 定义一个函数 函数有一个参数，有返回值 '''
#
# # 简单调用
# def application(string):
#     print('传入的参数是:', string)
#     return 'Hello ' + string



# 版本二：加入回调

''' 定义一个函数 函数有两个参数，参数一：普通参数，参数二：函数引用，有返回值 '''

# 简单调用
def application(string, func):
    # 普通打印
    print('传入的参数是:', string)
    # 调用函数，将application 函数传入参数又传给func函数
    func(string)
    # 拼接字符串返回
    return 'Hello ' + string