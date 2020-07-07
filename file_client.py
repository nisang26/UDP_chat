from socket import *
from time import *
import sys

HOST = '127.0.0.1'
PORT = 8088
ADDR = (HOST,PORT)

#将具体的发送请求的方法放在类里
class FPTClient:
    def __init__(self,sock):
        self.sock = sock

    #请求文件列表
    def do_list(self):
        self.sock.send(b'LIST')
        result = self.sock.recv(128).decode()
        if result == 'OK':
            while True:
                files = self.sock.recv(1024).decode()
                if files == '##':
                    break
                print(files)
        elif result == 'FALS':
            print("文件库为空")

    def do_get_file(self):
        filename = input('下载文件名：')
        msg = 'GET '+filename
        self.sock.send(msg.encode())
        result = self.sock.recv(128).decode()
        if result == 'OK':
            fw = open(filename,'wb')
            while True:
                data = self.sock.recv(1024)
                if data == b'##':
                    break
                fw.write(data)
            fw.close()
        elif result == 'NONE':
            print('该文件不存在')

    def do_put_file(self):
        filename = input('上传文件名：')
        try:
            fr = open(filename, 'rb')
        except:
            print('要上传的文件不存在')
            return
        #提取真正的文件名 filename可以是路径
        filename = filename.split('/')[-1]
        msg = 'PUT '+filename
        self.sock.send(msg.encode())
        result = self.sock.recv(128).decode()
        if result == 'OK':
            while True:
                data = fr.read(1024)
                if not data:
                    sleep(0.1)
                    self.sock.send(b'##')
                    break
                self.sock.send(data)
            fr.close()
        elif result == 'FALS':
            print('该文件在文件库中已经存在')

    def do_exit(self):
        self.sock.send(b'EXIT')
        self.sock.close()
        sys.exit('谢谢使用')

def main():
    sock = socket()
    sock.connect(ADDR)

    ftp = FPTClient(sock)

    while True:
        print('===========命令选项===========')
        print('-------------list------------')
        print('-----------get file----------')
        print('-----------put file----------')
        print('-------------exit------------')
        print('=============================')

        cmd = input('请输入选项:')
        if cmd == 'list':
            ftp.do_list()
        elif cmd == 'get':
            ftp.do_get_file()
        elif cmd == 'put':
            ftp.do_put_file()
        elif cmd == 'exit':
            ftp.do_exit()
        else:
            print('请正确输入')

if __name__ == '__main__':
    main()