CC=clang
CFLAGS=-emit-llvm -c -g -O0 -Xclang -disable-O0-optnone
OBJ=test-router.bc

all: test-router.bc

test-router.bc: test-router.cpp
	$(CC) $(CFLAGS) $<

klee: $(OBJ)
	klee $(OBJ)

show-tests: klee-last
	echo klee-last/test*.ktest | xargs ktest-tool 

clean:
	rm -rf *.bc *.o a.out klee-last klee-out-*

