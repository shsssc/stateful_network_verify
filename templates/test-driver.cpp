#include "topology.h"
#include <cstdio>

int main() {
	Header header;
	klee_make_symbolic(&header, sizeof(header), "header");

	Topology t;
	std::list<PktState> history = t.forward(PktState(header,{{src}},{{port}}));
	
#ifdef RUN_REPLAY
	for (const auto& i : history)
		printf("%d %d\n", i.node, i.port);
	printf("\n");
#endif
	

	return 0;
}
