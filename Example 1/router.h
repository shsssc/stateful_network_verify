#ifndef ROUTER_H
#define ROUTER_H

#include "common.h"

class Router {
  public:
	Egress forward (Header header) {
		if (accessList(header)) return Egress(header, -1);
		int port = forwardTable(header.dst_address);
		return Egress(header, port);
	}

	int forwardTable(uint32_t dst) {
		if ((dst >> (32 - 16)) == (0xC0A80000 >> (32 - 16))) {
			return 1;
		} else if ((dst >> (32 - 8)) == (0x0A000000 >> (32 - 8))) {
			return 2;
		} else {
			return 0;
		}
        //negative as drop
	}

	bool accessList(Header header) {
		return false;
	}
};

#endif