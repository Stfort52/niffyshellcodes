elf: tiny.asm
	nasm -fbin -o tiny.out tiny.asm
	chmod +x tiny.out

test: elf
	echo 'echo "hello, world!"; exit' | ./tiny.out 
	wc tiny.out
	
clean: 
	rm tiny.out