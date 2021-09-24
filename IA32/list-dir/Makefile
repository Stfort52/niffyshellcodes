bin: getdents.asm
	nasm -fbin getdents.asm -o getdents.bin

elf: getdents.asm
	nasm -felf32 -o getdents.o getdents.asm
	ld -o getdents.out getdents.o -melf_i386

clean: 
	rm getdents.out getdents.o getdents.bin