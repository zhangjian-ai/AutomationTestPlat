from django import dispatch

# 计数器+1信号
plus_one = dispatch.Signal()
