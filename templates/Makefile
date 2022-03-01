CC=clang++
CFLAGS=-emit-llvm -c -g -O0 -Xclang -disable-O0-optnone
REPLAY_CFLAGS=-L ../../klee_build/lib/ -lkleeRuntest -DRUN_REPLAY
OBJ=test-driver.bc

all: $(OBJ)

test-driver.bc: test-driver.cpp
	$(CC) $(CFLAGS) $<

klee: klee-last
klee-last: $(OBJ)
	klee --optimize $(OBJ)

show-tests: klee-last
	echo klee-last/test*.ktest | xargs ktest-tool 

show-stats: klee-last
	python ../reachedGeneratedComment.py -d ./klee-last/ -s ./ || python3 ../reachedGeneratedComment.py -d ./klee-last/ -s ./

test-driver: test-driver.cpp
	$(CC) $(REPLAY_CFLAGS) -o $@ $<

clean:
	rm -rf *.bc *.o a.out klee-last klee-out-*

