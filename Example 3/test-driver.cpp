#include "topology.h"

int main() {
	Header header;
	klee_make_symbolic(&header, sizeof(header), "header");

	Topology t;
	int outPort = t.forward(PktState(header,0,3));
	return outPort<0;
}
