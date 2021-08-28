#include <stdio.h>

void main(){
  page = mmap(addr, size, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_PRIVATE|MAP_ANON, 0, 0);
  read(0, page, size)
  ((void(*)())page)();  // 调用page地址函数的写法
}
