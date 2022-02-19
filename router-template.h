#ifndef {{name.upper()}}_H
#define {{name.upper()}}_H

#include "common.h"

class {{name}} {
  public:
	Egress forward (Header header) {
		if (accessList(header)) return Egress(header, -1);
		int port = forwardTable(header.dst_address);
		return Egress(header, port);
	}

	int forwardTable(uint32_t dst) {
	    {% for row in table %}
            {% if row.prefix_len == 0 %}
	    return {{row.port}};
            {% else %}
        if ((dst >> {{32 - row.prefix_len}}) == ({{row.hex_address}} >> {{32 - row.prefix_len}})) { // {{row.str_address}}/{{row.prefix_len}}
			return {{row.port}};
			{% endif %}
        {% endfor %}
        return -1;
        //negative as drop
	}

	bool accessList(Header header) {
		return false; // true as drop
	}
};

#endif