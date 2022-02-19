#ifndef ROUTER4_H
#define ROUTER4_H

#include "common.h"

class Router4 {
  public:
	Egress forward (Header header) {
		if (accessList(header)) return Egress(header, -1);
		int port = forwardTable(header.dst_address);
		return Egress(header, port);
	}

	int forwardTable(uint32_t dst) {
        if ((dst >> 8) == (0xa000100 >> 8)) { // 10.0.1.0/24
			return -1;
	    return 10;
        return -1;
        //negative as drop
	}

	bool accessList(Header header) {
		return false; // true as drop
	}
};

#endif