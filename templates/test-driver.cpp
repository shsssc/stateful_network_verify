#include "topology.h"

int main() {
	Header header;
	klee_make_symbolic(&header, sizeof(header), "header");

	Topology t;
	int outPort = t.forward(PktState(header,{{src}},{{port}}));
	return outPort < 0;
}
