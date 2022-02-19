#ifndef ROUTER2_H
#define ROUTER2_H

#include "common.h"

class Router2 {
  public:
	Egress forward (Header header) {
		if (accessList(header)) return Egress(header, -1);
		int port = forwardTable(header.dst_address);
		return Egress(header, port);
	}

	int forwardTable(uint32_t dst) {
        if ((dst >> 8) == (0xa000000 >> 8)) // 10.0.0.0/24
			return 5;
	    return 6;
        return -1;
        //negative as drop
	}

	bool accessList(Header header) {
		return false; // true as drop
	}
};

#endif