elf: small.asm
	nasm -fbin -o small.out small.asm
	chmod +x small.out

test: elf
	echo 'echo "hello, world!"; exit' | ./small.out 
	wc small.out
clean: 
	rm small.out