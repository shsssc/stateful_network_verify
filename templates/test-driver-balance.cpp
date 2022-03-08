#include "topology.h"
#include <cstdio>
#include <cstring>

#define MAX(a,b) ((a) < (b) ? (b) : (a))
#define MIN(a,b) ((a) < (b) ? (a) : (b))

class Network : public Topology {
  public:
	Network() {
		memset(counts, 0, sizeof(counts));
	}

	void forward(PktState pktState) {
		for (int hop = 0; hop < {{hop}}; hop++) {
			PktState forwardedPktState = node_execute(pktState);
			if (forwardedPktState.port == PORT_DROP) return;
			switch (pktState.node){
                {% for i,n in enumerate(equivlent_nodes) %}
                case {{n}}:
					counts[{{i}}] ++;
					return;
                {% endfor %}
            }
			pktState = link_function(forwardedPktState);
			if (pktState.port == PORT_DROP) return;
		}
		assert(0); //generated-comment: [TTL-Drop] potential loop
		return;
	}
  public:
	int counts[{{equivlent_nodes_len}}];
};

int main() {
	Header header;
	klee_make_symbolic(&header, sizeof(header), "header");
	klee_assume((header.src_port & 255) == 0);
	klee_assume((header.dst_port & 255) == 0);

	Network n;

	for (int s = 0; s < 256; s ++) {
		klee_open_merge();
		header.dst_address = (header.dst_address & ~255) | s;
		n.forward(PktState(header,{{src}},{{port}}));
		klee_close_merge();
	}
	
	int count_max = -1;
	int count_min = 1 << 24;
	{% for i,n in enumerate(equivlent_nodes) %}
	count_max = MAX(count_max, n.counts[{{i}}]);
	count_min = MIN(count_min, n.counts[{{i}}]);
	if (klee_is_replay())
		printf("Count for node {{n}}: %d\n", n.counts[{{i}}]);
	{% endfor %}

	klee_assert(count_max <= count_min * 2);

	return 0;
}
