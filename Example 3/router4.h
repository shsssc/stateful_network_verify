#ifndef ROUTER4_H
#define ROUTER4_H

#include "common.h"

class Router4 {
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
        if ((dst >> 8) == (0xa000100 >> 8)) // 10.0.1.0/24
			return -1;
	    return 3;
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