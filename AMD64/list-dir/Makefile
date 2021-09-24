bin: getdents.asm
	nasm -fbin getdents.asm -o getdents.bin

elf: getdents.asm
	nasm -felf64 -o getdents.o getdents.asm
	ld -o getdents.out getdents.o

clean: 
	rm getdents.out getdents.o getdents.bin