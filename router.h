#ifndef ROUTER_H
#define ROUTER_H

#include "common.h"

class Router {
  public:
	Egress forward (Header header) {
		if ((header.dst_address >> (32 - 16)) == (0xC0A80000 >> (32 - 16))) {
			return Egress(header, 1);
		} else if ((header.dst_address >> (32 - 8)) == (0x0A000000 >> (32 - 8))) {
			return Egress(header, 2);
		} else {
			return Egress(header, 0);
		}
        //negative as drop
	}
};

#endif