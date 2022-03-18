#include "topology.h"
#include <cstdio>

class Network : public Topology {
  public:
	PktState forward(PktState pktState) {
		if (klee_is_replay())
			printf("Starting port: %d %d\n", pktState.node, pktState.port);
		for (int hop = 0; hop < {{hop}}; hop++) {
			PktState forwardedPktState = node_execute(pktState);
			if (forwardedPktState.port == PORT_DROP) {
				if (klee_is_replay())
					printf("Drop by: %d %d\n", forwardedPktState.node, forwardedPktState.port);
				return pktState;
			}
			pktState = link_function(forwardedPktState);
			if (klee_is_replay())
				printf("Forward to: %d %d => %d %d\n", forwardedPktState.node, forwardedPktState.port, 
							pktState.node, pktState.port);
			if (pktState.port == PORT_DROP) return forwardedPktState;
		}
		assert(0); //generated-comment: [TTL-Drop] potential loop
		return pktState;
	}
};

int main() {
	Header header;
	klee_make_symbolic(&header, sizeof(header), "header");
	klee_make_symbolic(&shared_symbolic_state, sizeof(shared_symbolic_state), "shared_symbolic_state");

	Network n;
	PktState h_out = n.forward(PktState(header,{{src}},{{port}}));
	h_out.header.reverse();
	if (klee_is_replay())
		printf("------reverse packet------");
	n.forward(h_out);
	if (klee_is_replay())
		printf("------resent packet------");
	n.forward(PktState(header,{{src}},{{port}}));
	return 0;
}
