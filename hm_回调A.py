# ''' 想在A模块中，使用B模块里的函数  '''
#  版本一， 简单调用
# import hm_回调B as B
#
# print(B.application('World'))




# 版本二 ，加入回调
''' 想在A模块中，使用B模块里的函数  '''

import hm_回调B as B

# 定义一个func函数
def show(string):
    print('Show ', string)


print(B.application('World', show))