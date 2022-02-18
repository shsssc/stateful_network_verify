#ifndef ROUTER_H
#define ROUTER_H

#include "common.h"

class Router {
  public:
	int forward (uint32_t dst) {
		if ((dst >> (32 - 16)) == (0xC0A80000 >> (32 - 16))) {
			return 1;
		} else if ((dst >> (32 - 8)) == (0x0A000000 >> (32 - 8))) {
			return 2;
		} else {
			return 0;
		}
        //negative as drop
	}
};

#endif