#ifndef TOPOLOGY_H
#define TOPOLOGY_H

{% for class_name, _ in nodes.items() %}
#include "{{snake_case(class_name)}}.h"
{% endfor %}

enum Node {
    {% for class_name, id in nodes.items() %}
    {{class_name}}Id={{id}},
    {% endfor %}
};


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

public:
    {% for class_name, id in nodes.items() %}
    {{class_name}} node{{id}};
    {% endfor %}
};

#endif
