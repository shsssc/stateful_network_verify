#ifndef ROUTER1_H
#define ROUTER1_H

#include "common.h"

class Router1 {
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
        if ((dst >> 16) == (0xa000000 >> 16)) // 10.0.0.0/16
			return 1;
        if ((dst >> 16) == (0xa010000 >> 16)) // 10.1.0.0/16
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