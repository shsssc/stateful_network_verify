#include "topology.h"
#include <cstdio>

int main() {
	Header header;
	klee_make_symbolic(&header, sizeof(header), "header");

	Topology t;
	std::list<PktState> history = t.forward(PktState(header,{{src}},{{port}}));
	
	//uncomment below when replaying to show test result
	/*
	for (const auto& i : history)
		printf("%d %d\n", i.node, i.port);
	printf("\n");
	*/

	return 0;
}
