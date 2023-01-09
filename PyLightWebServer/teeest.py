

import socket

#---------------------------------#
"""
状态参数
"""
#---------------------------------#


sk = socket.socket()
host = socket.gethostname()
port = 14147
sk.bind((host,port))
sk.listen(5)

path = r"D:\workingflows\LightWebServer\PyLightWebServer\html\index.html"
while True:
    c,addr = sk.accept()     # 建立客户端连接
    c.recv(1024)
    c.send(b'HTTP/1.1 200 ok\r\n\r\n')
    print ('连接地址：', addr)
    with open(path, 'rb') as f:
        buf = f.read()
    c.send(buf)
    c.close()                # 关闭连接
