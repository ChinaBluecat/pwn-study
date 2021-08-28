strace 一个动态调试工具
用label_0:之类的分段, 可以在gdb中方便地下断点
int 3 硬件断点

不同的字节数:

mov [rax], bl   # 1字节
mov [rax], bx   # 2字节
mov [rax], ebx  # 4字节
mov [rax], rbx  # 8字节

mov BYTE PTR[rax], 5    # 向rax地址写入1字节
mov WORD PTR[rax], 5    # 2字节
mov DWORD PTR[rax], 5   # 4字节
mov QWORD PTR[rax], 5   # 8字节

用
mov   rbx, data
push  rbx
mov   rbx, rsp
可以获得一个字符串指针

不同的输入函数, 以及会被截断的字节:

| bytes        | func                        |
| ------------ | --------------------------- |
| \0(0x00)     | strcpy                      |
| \n(0x0a)     | scanf, gets, getline, fgets |
| \r(0x0d)     | scanf                       |
| space(0x20)  | scanf                       |
| tab \t(0x09) | scanf                       |
| del(0x7f)    | telnet, etc..               |

|63..32|31..16|15-8|7-0|
              | AH.|AL.|
              | AX.....|
       |EAX............|
|RAX...................|

可以使用许多技巧避免, 可以用加法来使得某些值达到目标值
或者用xor之类函数来对变量清0
数据本身也是代码, 所以某些取值可以从代码上获得

shellcode的注意事项:

1. 尽可能短
2. 可以进行压缩解压
3. 可以进行加密解密


对于其他平台架构(非x86/x64), 可以用qemu来仿真, 需要查相关内容

sendfile(1, open('/flag', NULL), 0, 1000)打印到输出
用objdump -M intel -d target_elf查看汇编
用objcopy --dump-section .text=target_elf.txt target_elf 来对二进制代码dump

在 /root/proc下是所有进程的map, 以文件形式存在
可以用
grep -l rwx */maps
grep -l rwx */maps | parallel "ls -l {//}/exe"
来找到具有可写可执行的内存段区, 及对应的应用程序

checksec 查看保护

cat self/maps
vmmap 查看段表

x64函数调用规定:

rdi, rsi, rdx, r10, r8, r9对应参数从左到右
函数返回会交给rax


文件描述符, 0是输入, 1是输出, 2是异常(error), 之后的数字代表打开的文件返回。
在打开时返回-1则发生异常, 具体查表


gcc -nostdlib -static /tmp/test.s -o /tmp/test
objcopy --dump-section .text=/tmp/test.md /tmp/test

ROPGenerator/ROPgadget

run < filename_with_input 从gdb中以文件作为参数输入
run $( cat arg.txt )
step 单步步入
