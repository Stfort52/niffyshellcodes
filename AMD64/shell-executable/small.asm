BITS 64

        org	0x100000000

        db	0x7F, "ELF"
        db	2, 1, 1, 1, 0
        db  0
_fini:
        push rbx
        mov rdi, rsp
        syscall         ; e_pad
        dw	2
        dw	62			; e_machine
        dd	1			; e_version
        dd	_gogo		; e_entry
phdr:		dd	1					; p_type
        dd	phdr - $$		; e_phoff	; p_flags
        dd	0					; p_offset
        dd	0			; e_shoff
        dq	$$					; p_vaddr
                        ; e_flags
        dw	0x40			; e_ehsize	; p_paddr
        dw	0x38			; e_phentsize
        dw	1			; e_phnum
        dw	0			; e_shentsize
        dq	filesz			; e_shnum	; p_filesz
                        ; e_shstrndx
        dq	filesz					; p_memsz
        dq	0x00400000				; p_align

_gogo:
    mov al, 0x3b
    mov rbx, 0x0068732f6e69622f
    jmp _fini
    
filesz		equ	$ - $$