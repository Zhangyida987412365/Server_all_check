import subprocess
import platform
import socket


def ping(host):

    param = '-n'
    command = ['ping',param,'4', host]
    
    try:
        output = subprocess.run(command, stdout=subprocess.PIPE ,
                                stderr=subprocess.PIPE,text=True,check=True)
        return output.stdout
    except subprocess.CalledProcessError as e:
        return f'无法Ping {host},错误：{e.returncode}:\n{e.output}'



def is_host_online(host,port=80,timeout=5):
    try:
        socket.setdefaulttimeout(timeout)
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.connect((host,port))
            return True
    except OSError:
        return False

print(ping('1'))
print(ping('1'))
