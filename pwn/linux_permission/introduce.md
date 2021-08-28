### introduce

每个进程均有一个USER ID和GID
所有文件具有其USER用户和GROUP组
子进程的GID与父进程一致

有效effective eUID/eGID   一个进程的有效ID, 用于进行大部分检查, 用geteuid()获得
真实real UID/GID          用于简单检查, 通常是进程的所有者, 用getuid()获得
保存saved UID/GID         保存的ID, 可以在某些场合进行切换提升权限或者降低权限(也就是提权)

用sudo chown root.root target 可以改变某个文件的所属者
具有rws特性的root所属应用, 如果发生了安全问题, 启用了sh, 则可以让用户进行提权
因为rws具有root所属属性, 所以执行时会被认作root用户通过检查

rwxrwxrwx user/group/others
r 可读  100
w 可写  010
x 可执行001

chmod 777 xxx



100种打印/查看文件的方法/修改UID方法
vim
cat
tail
less
chmod
tac
head
more
nl
chown
