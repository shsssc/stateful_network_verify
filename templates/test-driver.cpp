#include "topology.h"
#include <cstdio>

int main() {
	Header header;
	klee_make_symbolic(&header, sizeof(header), "header");

	Topology t;
	t.forward(PktState(header,{{src}},{{port}}));

	return 0;
}
