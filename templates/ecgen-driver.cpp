#include "topology.h"
#include <cstdio>

class Network : public Topology {
  public:
    void forward(PktState& pktState) {
        for (int hop = 0; hop < {{hop}}; hop++) {
            pktState = node_execute(pktState);
            if (pktState.port == PORT_DROP) return;
            PktState oldState = pktState;
            pktState = link_function(pktState);
            switch (pktState.node){
                {% for node in nodes %}
                case {{node}}Id:
                {% endfor %}
                break;
                default:
                    pktState = oldState;
                    return;
            }
            if (pktState.port == PORT_DROP) return;
        }
    return;
    }
};

int main() {
	Header header;
	Network n;
    PktState pkt(header, 0, 0);
    {% for node in nodes %}
        {% for ec in ecs %}
    header.dst_address = {{ec['concrete']}};
    pkt = PktState(header, {{node}}Id, 0);
    n.forward(pkt);
    printf("%s,%s,%d,%d\n","{{node}}", "{{ec['prefix']}}", pkt.node, pkt.port);
    //printf("inNode: %s,prefix: %s,outNode: %d, outPort: %d\n","{{node}}", "{{ec['prefix']}}", pkt.node, pkt.port);
        {% endfor %}
    {% endfor %}

	return 0;
}
