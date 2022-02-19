#ifndef ROUTER3_H
#define ROUTER3_H

#include "common.h"

class Router3 {
  public:
	Egress forward (Header header) {
		if (accessList(header)) return Egress(header, -1);
		int port = forwardTable(header.dst_address);
		return Egress(header, port);
	}

	int forwardTable(uint32_t dst) {
        if ((dst >> 24) == (0xa000000 >> 24)) // 10.0.0.0/8
			return 8;
        return -1;
        //negative as drop
	}

	bool accessList(Header header) {
		return false; // true as drop
	}
};

#endif