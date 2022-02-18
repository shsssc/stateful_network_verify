#include "topology.h"

int main() {
	uint32_t node;
	uint32_t dst;
	klee_make_symbolic(&node, sizeof(node), "node");
	klee_make_symbolic(&dst, sizeof(dst), "dst");

	Topology t;
	klee_assume(node >= 0 && node <= t.get_node_max());
	int port = t.forward(node, dst);
	return 0;
}
