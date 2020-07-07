from socket import *
from threading import Thread
import sys
import os
from time import *

HOST = '0.0.0.0'
PORT = 8088
ADDR = (HOST,PORT)

FTP = '/home/tarena/FTP/'#文件库

class FTPServer(Thread):
    def __init__(self,connfd):
        self.connfd = connfd
        super().__init__()

    def do_list(self):
        file_list = os.listdir(FTP)
        if not file_list:
            self.connfd.send(b'FALS')
            return
        else:
            self.connfd.send(b'OK')
            file_str = '\n'.join(file_list)
            self.connfd.send(file_str.encode())
            sleep(0.1)
            self.connfd.send('##'.encode())

    def do_get(self,filename):
        file_list = os.listdir(FTP)
        if filename not in file_list:
            self.connfd.send(b'NONE')
            return
        else:
            self.connfd.send(b'OK')
            sleep(0.1)
            fr = open(FTP+filename,'rb')
            while True:
                data = fr.read(1024)
                if not data:
                    sleep(0.1)
                    self.connfd.send(b'##')
                    break
                self.connfd.send(data)
            fr.close()

    def do_put(self,filename):
        if os.path.exists(FTP+filename):
            self.connfd.send(b'FALS')
            return
        else:
            self.connfd.send(b'OK')
            fw = open(FTP+filename,'wb')
            while True:
                data = self.connfd.recv(1024)
                if data == b'##':
                    break
                fw.write(data)
            fw.close()

    def run(self):
        while True:
            data = self.connfd.recv(1024).decode()
            msg = data.split(' ',2)
            #无论是正常或者异常退出客户端
            if not data or msg[0] == 'EXIT':
                self.connfd.close()
                return
            elif msg[0] == 'LIST':
                self.do_list()
            elif msg[0] == 'GET':
                self.do_get(msg[1])
            elif msg[0] == 'PUT':
                self.do_put(msg[1])


def main():
    #创建套接字 默认tcp
    sock = socket()
    #绑定地址
    sock.bind(ADDR)
    #设置监听
    sock.listen(5)
    while True:
        try:
            #循环等待客户连接
            c,addr = sock.accept()
            print('客户端地址：',addr)
        except KeyboardInterrupt:
            sock.close()
            sys.exit('客户端退出')

        #有客户端连进来创建新的线程
        t = FTPServer(c)
        t.start()



if __name__ == '__main__':
    main()