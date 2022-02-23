#ifndef {{name_snake.upper()}}_H
#define {{name_snake.upper()}}_H

#include "common.h"

class {{name}} {
  public:
        PktState forward(PktState stateIn) {
            int node = stateIn.node;
            int portIn = stateIn.port;
            Header &header = stateIn.header;
            if (!aclIn(header, portIn)) return {header, node, -1};
            int portOut = forwardTable(header.dst_address); //generated-comment: [reached] {{name}}
            if (!aclOut(header, portOut)) return {header, node, -1};
            return {header, node, portOut};
        }

	int forwardTable(uint32_t dst) {
	    {% for row in table %}
            {% if row.prefix_len == 0 %}
	    return {{row.port}};
            {% else %}
        if ((dst >> {{32 - row.prefix_len}}) == ({{row.hex_address}} >> {{32 - row.prefix_len}})) // {{row.str_address}}/{{row.prefix_len}}
			return {{row.port}};
			{% endif %}
        {% endfor %}
        return -1;
        //negative as drop
	}

	bool aclIn(Header header, int port) {
		return true; // false as drop
	}

	bool aclOut(Header header, int port) {
		return true; // false as drop
	}
};

#endif
