#ifndef TOPOLOGY_H
#define TOPOLOGY_H
#include "router1.h"
#include "router2.h"
#include "router3.h"
#include "router4.h"

class Topology {
  public:
	Egress node_execute (int node, Header header) {
        if (node == 0) {
            return node0.forward(header);
        }
        if (node == 1) {
            return node1.forward(header);
        }
        if (node == 2) {
            return node2.forward(header);
        }
        if (node == 3) {
            return node3.forward(header);
        }
        //error
        assert(0);
	}

    //negative as un-linked port
    int port_to_device(int node, int port) {
        if (node == 0) {
            if (port == 1) 
                return 1;
            if (port == 3) 
                return 2;
        }
        if (node == 1) {
            if (port == 2) 
                return 0;
            if (port == 6) 
                return 3;
        }
        if (node == 2) {
            if (port == 4) 
                return 0;
            if (port == 8) 
                return 3;
        }
        if (node == 3) {
            if (port == 7) 
                return 1;
            if (port == 9) 
                return 2;
        }
        return -1;
    }

    Location forward(int node, Header header) {
        for (int hop = 0; hop < 16; hop ++) {
            std::cout << hop << node << std::endl;
            Egress egress = node_execute(node, header);
            header = egress.header;
            if (egress.port < 0) return Location(node, egress.port);
            int new_node = port_to_device(node, egress.port);
            if (new_node < 0) return Location(node, egress.port);
            node = new_node;
        }
        return Location(-1, -1); //error
    }

    int get_node_max() {
        return 3;
    }

  public:
    Router1 node0;
    Router2 node1;
    Router3 node2;
    Router4 node3;
};

#endif