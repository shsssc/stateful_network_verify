#ifndef ROUTER1_H
#define ROUTER1_H

#include "common.h"

class Router1 {
  public:
	Egress forward (Header header) {
		if (accessList(header)) return Egress(header, -1);
		int port = forwardTable(header.dst_address);
		return Egress(header, port);
	}

	int forwardTable(uint32_t dst) {
        if ((dst >> 16) == (0xa000000 >> 16)) // 10.0.0.0/16
			return 1;
        if ((dst >> 16) == (0xa010000 >> 16)) // 10.1.0.0/16
			return 3;
        return -1;
        //negative as drop
	}

	bool accessList(Header header) {
		return false; // true as drop
	}
};

#endif