import json
from pwn import remote

HOST = "socket.cryptohack.org"
PORT = 13399
TOKEN = "00" * 28

def attack():
    attempts = 0
    while True:
        try:
            r = remote(HOST, PORT, level='error')
            r.recvline()
            
            for _ in range(50):
                attempts += 1                
                r.sendline(json.dumps({'option': 'reset_password', 'token': TOKEN}).encode())
                r.recvline()
                
                r.sendline(json.dumps({'option': 'authenticate', 'password': ''}).encode())
                res = json.loads(r.recvline().decode())
                
                if 'flag' in res['msg']:
                    print("FLAG:", res['msg'])
                    r.close()
                    return
                
                r.sendline(json.dumps({'option': 'reset_connection'}).encode())
                r.recvline()
                
            r.close()
            
        except EOFError:
            r.close()
            pass
        except Exception as e:
            break

attack()