#ifndef ROUTER3_H
#define ROUTER3_H

#include "common.h"

class Router3 {
  public:
        PktState forward(PktState stateIn) {
            int node = stateIn.node;
            int portIn = stateIn.port;
            Header &header = stateIn.header;
            if (aclIn(header, portIn)) return {header, node, -1};
            int portOut = forwardTable(header.dst_address);
            if (aclOut(header, portOut)) return {header, node, -1};
            return {header, node, portOut};
        }

	int forwardTable(uint32_t dst) {
        if ((dst >> 24) == (0xa000000 >> 24)) // 10.0.0.0/8
			return 2;
        return -1;
        //negative as drop
	}

	bool aclIn(Header header, int port) {
		return false; // true as drop
	}

	bool aclOut(Header header, int port) {
		return false; // true as drop
	}
};

#endif