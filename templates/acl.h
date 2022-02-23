#ifndef {{name_snake.upper()}}_H
#define {{name_snake.upper()}}_H

#include "common.h"

class {{name}} {
  public:
	bool isAllowed(Header header) {
	    {% for row in acl_table %}
	    if (
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
	        return {{row.is_allowed}} // {{row.name}}
        {% endfor %}
		return true; // false as drop
	}
};

#endif
