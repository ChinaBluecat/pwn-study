.global _start
_start:
.intel_syntax noprefix
        # read(3, *buf, 100)
        xor rax, rax
        xor rdi, rdi
        xor rsi, rsi
        xor rdx, rdx
        mov rax, 0
        mov rdi, 3
        lea rsi, [rip+data]
        mov rdx, 100
        syscall
        # nanosleep(struct timespec*)
        mov rax, 35
        mov edi, dword ptr [rsi]
        push 0
        and rdi, 0x000000ff
        push rdi
        mov rdi, rsp
        mov rsi, rsp
        syscall
data:
        .string ""
