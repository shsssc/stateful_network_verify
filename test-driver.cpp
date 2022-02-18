#include "topology.h"

int main() {
	uint32_t node;
	uint32_t dst;
	klee_make_symbolic(&node, sizeof(node), "node");
	klee_make_symbolic(&dst, sizeof(dst), "dst");
	int port = Topology().forward(node, dst);
	return 0;
}
