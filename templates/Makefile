CC=clang++
CFLAGS=-emit-llvm -c -g -O0 -Xclang -disable-O0-optnone
REPLAY_CFLAGS=-L ../../klee_build/lib/ -lkleeRuntest -DRUN_REPLAY
OBJ=test-driver.bc

all: $(OBJ)

test-driver.bc: test-driver.cpp
	$(CC) $(CFLAGS) $<

klee: klee-last
klee-last: $(OBJ)
	klee --optimize --write-cov $(OBJ)

klee-cov: klee-last
	cat klee-last/*.cov |sort | uniq|grep "\./" >  klee-last/all-tests.cov

show-tests: klee-last
	echo klee-last/test*.ktest | xargs ktest-tool 

show-stats: klee-cov
	python3 ../reachedGeneratedComment.py -c ./klee-last/all-tests.cov -s ./

test-driver: test-driver.cpp
	$(CC) $(REPLAY_CFLAGS) -o $@ $<

clean:
	rm -rf *.bc *.o a.out klee-last klee-out-*

