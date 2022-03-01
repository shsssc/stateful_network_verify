#ifndef {{name_snake.upper()}}_H
#define {{name_snake.upper()}}_H

#include "common.h"

class {{name}} {
  public:
    static uint8_t hash(Header header) {
        uint8_t h = 0;
        h ^= (header.src_address & 255);
        h ^= ((header.src_address >> 8) & 255);
        return h;
    }

    PktState forward(PktState stateIn) {
        int node = stateIn.node;
        int portIn = stateIn.port;
        Header &header = stateIn.header;
        int portOut = forwardTable(header.dst_address, hash(header)); //generated-comment: [reached] {{name}}
        if (!acl(header, portIn, portOut)) return {header, node, -1};
        return {header, node, portOut};
    }

	int forwardTable(uint32_t dst, uint8_t hashVal) {
	    {% for row in table %}
            {% if row.prefix_len == 0 %}
	    if (true) { // {{row.str_address}}/0
            {% else %}
        if ((dst >> {{32 - row.prefix_len}}) == ({{row.hex_address}} >> {{32 - row.prefix_len}})) { // {{row.str_address}}/{{row.prefix_len}}
			{% endif %}
            {% for i,p in enumerate(row.ports) %}
            if (hashVal % {{row.ports_len}} == {{i}})
			    return {{p}};
            {% endfor %}
        }
        {% endfor %}
        return -1;
        //negative as drop
	}

    bool acl(Header header, int ingress, int egress) {
        {% for row in acl_table %}
        if (
            {% if row.ingress >= 0 %}
                ingress == {{row.ingress}} &&
            {% endif %}
            {% if row.egress >= 0 %}
                egress == {{row.egress}} &&
            {% endif %}
            {% if row.src_prefix_len > 0 %}
                (header.src_address >> {{32 - row.src_prefix_len}}) == ({{row.src_hex_address}} >> {{32 - row.src_prefix_len}}) && // {{row.src_str_address}}/{{row.src_prefix_len}}
            {% endif %}
            {% if row.src_port >= 0 %}
                header.src_port == {{row.src_port}} &&
            {% endif %}
            {% if row.dst_prefix_len > 0 %}
                (header.dst_address >> {{32 - row.dst_prefix_len}}) == ({{row.dst_hex_address}} >> {{32 - row.dst_prefix_len}}) && // {{row.dst_str_address}}/{{row.dst_prefix_len}}
            {% endif %}
            {% if row.dst_port >= 0 %}
                header.dst_port == {{row.dst_port}} &&
            {% endif %}
            {% if row.protocol >= 0 %}
                header.protocol == {{row.protocol}} &&
            {% endif %}
                true)
            return {{'true' if row.is_allowed else 'false'}}; // {{row.name}}
        {% endfor %}
        return true; // false as drop
    }
};

#endif
