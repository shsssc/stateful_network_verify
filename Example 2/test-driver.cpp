#include "topology.h"

int main() {
	uint32_t node;
	Header header;
	klee_make_symbolic(&node, sizeof(node), "node");
	klee_make_symbolic(&header, sizeof(header), "header");

	Topology t;
	klee_assume(node >= 0 && node <= t.get_node_max());
	Location port = t.forward(node, header);
	return 0;
}
