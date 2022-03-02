#ifndef TOPOLOGY_H
#define TOPOLOGY_H

{% for class_name, _ in nodes.items() %}
#include "{{snake_case(class_name)}}.h"
{% endfor %}

#include <cstdio>

class Topology {
public:
    PktState node_execute(PktState pktState) {
        int node = pktState.node;
        Header &header = pktState.header;
        int port = pktState.port;
        {% for class_name, id in nodes.items() %}
        if (node == {{id}}) {
            return node{{id}}.forward(pktState);
        }
        {% endfor %}

        assert(0); //generated-comment: [node-dispatch-failed] packet existing
    }

    //negative as un-linked port
    static PktState link_function(PktState in) {
        int node = in.node;
        int port = in.port;
        Header &header = in.header;
        {% for row in links %}
        if (node == {{row.n_from}} && port == {{row.p_from}})
            return {header, {{row.n_to}}, {{row.p_to}}};
        {% endfor %}
        return {header, -1, -1};
    }

    void forward(PktState pktState) {
        for (int hop = 0; hop < {{hop}}; hop++) {
	    if (klee_is_replay())
            	printf("%d %d\n", pktState.node, pktState.port);
            pktState = node_execute(pktState);
            if (pktState.port == PORT_DROP) return;
            pktState = link_function(pktState);
            if (pktState.port == PORT_DROP) return;
        }
	assert(0); //generated-comment: [TTL-Drop] potential loop
        return;
    }

public:
    {% for class_name, id in nodes.items() %}
    {{class_name}} node{{id}};
    {% endfor %}
};

#endif
