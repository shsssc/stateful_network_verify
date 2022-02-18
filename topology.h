#ifndef TOPOLOGY_H
#define TOPOLOGY_H
#include "router.h"

class Topology {
  public:
	Egress node_execute (int node, Header header) {
        if (node == 0) {
            return node0.forward(header);
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

    int forward(int node, Header header) {
        for (int hop = 0; hop < 16; hop ++) {
            Egress egress = node_execute(node, header);
            header = egress.header;
            if (egress.port < 0) return egress.port;
            node = port_to_device(egress.port);
            if (node < 0) return egress.port;
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