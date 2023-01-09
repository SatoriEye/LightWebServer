

#--------------------------库import------------------------------#

import socket
import concurrent.futures
import re
import time
import os

#--------------------------库import结束--------------------------#

#--------------------------参数配置--------------------------#

#HTML文件路径
DOCUMENTS_ROOT = "D:\workingflows\LightWebServer\PyLightWebServer\html"  #windows
# DOCUMENTS_ROOT = "home\ubuntu\PyLightServer\html"  #Linux 
#因为文件都放在当前路径下的html文件夹里，所以这里定义一个固定路径，存放的是提前写好的网页文件。

# 文件体解码格式
DECODING_FORMAT = "gbk"
# DECODING_FORMAT = "utf-8"

#--------------------------参数配置结束--------------------------#
#-------------------------功能函数定义----------------------------#

#处理服务端请求

def handle_client(client_socket):
    "为一个客户端进行服务"
    recv_data = client_socket.recv(1024).decode('gbk', errors="ignore") #报错忽略
    '''
    注意尽管客户端可以根据返回的HTML里的链接发送二次请求，但是要想正确返回请求内容，需要服务器能够解析
    这些请求内容，找到这些内容读取后send给客户端。所以下面要做的就是解析客户端的请求如下格式：
    b'GET /images/qt-logo.png HTTP/1.1\r\nHost: 127.0.0.1:7890\r\nConnection: keep-alive\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36\r\nAccept: image/webp,image/apng,image/*,*/*;q=0.8\r\nReferer: http://127.0.0.1:7890/\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: zh-CN,zh;q=0.9\r\n\r\n'
    '''
    request_header_lines = recv_data.splitlines() #1.将服务器接收的数据按HTTP格式进行切分，模式分割符就是\r\n
    for line in request_header_lines:   #打印是为了测试使用
        print(line)
    if len(request_header_lines) > 0:
        http_request_line = request_header_lines[0]  #2.获取请求数据的第一行，比如：GET /images/qt-logo.png HTTP/1.1
        get_file_name = re.match("[^/]+(/[^ ]*)", http_request_line).group(1)  #3.获取客户端请求的文件名images/qt-logo.png
    else:
        response_headers = "HTTP/1.1 404 not found\r\n"
        response_body = "====sorry ,file not found, 请你刷新下界面，这只是小问题(doge)===="
    print("file name is ===>%s" % get_file_name)  # for test
    
    # 如果没有指定访问哪个页面。例如index.html
    # GET / HTTP/1.1
    if get_file_name == "/":
        get_file_name = DOCUMENTS_ROOT + "/index.html"
    else:
        get_file_name = DOCUMENTS_ROOT + get_file_name

    print("file name is ===2>%s" % get_file_name) #for test

    try:
        f = open(get_file_name, "rb")
    except IOError: #如果没有该文件，则返回404 not found
        # 404表示没有这个页面
        response_headers = "HTTP/1.1 404 not found\r\n"
        response_headers += "\r\n"
        response_body = "====sorry ,file not found===="
    else:  #注意这里else的使用,找到了该文件返回200 OK
        response_headers = "HTTP/1.1 200 OK\r\n"
        response_headers += "\r\n"
        response_body = f.read() #读取用户请求的文件，注意这里如果文件很大，可以循环读取
        f.close()

    finally:# 在这里将读取的文件发送给客户端。
        # 因为头信息在组织的时候，是按照字符串组织的，不能与以二进制打开文件读取的数据合并，因此分开发送
        # 先发送response的头信息
        client_socket.send(response_headers.encode(DECODING_FORMAT)) #注意如果在linux上测试的话，改成utf-8
        # 再发送body
        if type(response_body) == type(str()):
            client_socket.send(response_body.encode('utf-8'))
        else:
            client_socket.send(response_body)
        client_socket.close()


#-------------------------功能函数定义结束----------------------------#

def main():
    "作为程序的主控制入口"
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置当服务器先close 即服务器端4次挥手之后资源能够立即释放，这样就保证了，下次运行程序时 可以立即绑定16686端口
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", 16686))
    server_socket.listen(128)

    #主体运行域
    while True:
        try:
            client_socket, clien_cAddr = server_socket.accept()
            handle_client(client_socket)
        except IndexError:
            continue



if __name__ == "__main__":
    main()