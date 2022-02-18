#ifndef TOPOLOGY_H
#define TOPOLOGY_H
#include "router.h"

class Topology {
  public:
	int node_execute (int node, uint32_t dst) {
        if (node == 0) {
            return node0.forward(dst);
        }
        //error
        assert(0);
	}

    //negative as un-linked port
    int port_to_device(int port) {
        if (port == 3) {
            return 0;
        } else {
            return -1;
        }
    }

    int forward(int node, uint32_t dst) {
        for (int hop = 0; hop < 16; hop ++) {
            int port = node_execute(node, dst);
            if (port < 0) return port;
            node = port_to_device(port);
            if (node < 0) return port;
        }
        return -1; //error
    }

    int get_node_max() {
        return 0;
    }

  public:
    Router node0;
};

#endif