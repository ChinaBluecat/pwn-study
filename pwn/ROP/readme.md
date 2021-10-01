### ROPchain

ROP是一项传统的利用技术, 之前已经提到过, 现代进程运行通常会有很多保护编译选项, 而NX(No Execute)就是阻止我们在栈上进行代码执行的一项关键保护。系统在编译时将存储空间和代码空间区分, 设定了不可执行。因此我们需要在可执行页上想办法进行代码执行。

前面的题也有提示, 如果能控制RIP指针, 即可控制程序走到程序本身的任何代码段。因此ROP概念便有此而来。Return Oriented Programing, 返回本有编程。通过利用程序本身存在的代码块, 重组合后执行我们想要的目标功能。


1. 魔法gadget
魔法gadget主要指的是只用调用这一个gadget就可以获得shell(或者完成需求任务)。
类似有system(commend), 该函数会调用execve("/bin/sh", {"/bin/sh", "-c", commend}, env), 成功执行后我们会获得一个目标进程的shell。通常有些程序代码中可能存在system()的系统调用, 我们可以布置好寄存器的传参, 然后跳转到system函数调用的地址(通常是一个call地址到plt表中), 来获得。
execve本身也是一个魔法gadget。

当然通常有些东西会被ban, 所以需要找到你想要, 或者说比较合适的gadget。

2. AntiROP

通常有以下几种对抗ROP的方法。
2.1 移除ROPgadget
编译时将pop x; ret; 这类的代码段变化, 或者填充许多的干扰汇编代码。
通常非常繁琐, 且编译消耗大时间长。代表: G-Free
2.2 检测ROP
学术界比较多研究, 现在也有机器学习的方法来进行检测。通常是通过观察在堆栈上的布置是否指向许多的ret。有对抗方法, 比如混入许多正常的执行, 只要没达到检测阈值就不会被发现。
代表:
kBouncer, ROPecker

2.3 Control Flow Integrity
控制流完整性检查。是目前比较主流的ROP对抗, 以及其他控制流劫持检查的方法。
思想: 当控制流劫持发生时, 保证该控制流的返回地址是一个被允许的返回地址。
从2015年起, 一直有学术论文在这方面进行对抗性研究。
B(lock)OP: 谨慎使用ROP链, 并平衡掉ROP链的副作用, 即堆栈平衡, 额外的寄存器等。
J(ump)OP: 代替ret, 使用间接jump来控制程序流
C(all)OP: 代替ret, 使用间接的call来控制程序流(return to asm)
S(igreturn)OP: 代替ret, 使用sigreturn来实现系统调用(去学一下https://zhuanlan.zhihu.com/p/85892044, 非常有用)
D(ata)OP: 通过控制数据值, 根据程序本身的设计来达到控制流的目的, 比较依赖目标程序本身的设计。

2.4 Control-flow Enforcement Technology(CET)
区别于其他方法, CET增加了endbr64指令, 这个指令并不进行任何操作, 但所有间接跳转(jmp, ret, call等)必须以endbr64指令作为结尾, 否则进程就会结束。虽然该技术可以被绕过, 但也增加了利用的难度和复杂性。


### Hacking Blind

是否可以在不知道目标进程的状态下进行利用呢? 从事实上来看, 这是可能的。
直觉: 程序只会在运行的时候进行地址随机化。

一个标准的盲打过程如下:
1. 一字节一字节的破坏ASLR和canary, 这样我们可以获得目标进程的一定程度上的重定向。(True or False Check out)
2. 设置目标内存直到获得一个存活的信号(比如布置了一个正确的返回地址, 填充了正确的数据报文)
3. 利用这个存活的交互来发现一些不会崩溃的ROPgadget(真难啊=。=)
4. 找到可以进行信息回馈的一些函数
5. 泄露整个程序(memory leak and dump program)
6. hack it

论文: Hacking Blind: http://www.scs.stanford.edu/brop/bittau-brop.pdf
