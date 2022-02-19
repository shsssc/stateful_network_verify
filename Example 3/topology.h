#ifndef TOPOLOGY_H
#define TOPOLOGY_H

#include "router1.h"
#include "router2.h"
#include "router3.h"
#include "router4.h"

class Topology {
public:
    PktState node_execute(PktState pktState) {
        int node = pktState.node;
        Header &header = pktState.header;
        int port = pktState.port;
        if (node == 0) {
            return node0.forward(pktState);
        }
        if (node == 1) {
            return node1.forward(pktState);
        }
        if (node == 2) {
            return node2.forward(pktState);
        }
        if (node == 3) {
            return node3.forward(pktState);
        }
        //error
        assert(0);
    }

    //negative as un-linked port
    static PktState link_function(PktState in) {
        int node = in.node;
        int port = in.port;
        Header &header = in.header;
        if (node == 0 && port == 1)
            return {header, 1, 1};
        if (node == 1 && port == 1)
            return {header, 0, 1};
        if (node == 0 && port == 2)
            return {header, 2, 1};
        if (node == 2 && port == 1)
            return {header, 0, 2};
        if (node == 1 && port == 3)
            return {header, 3, 1};
        if (node == 3 && port == 1)
            return {header, 1, 3};
        if (node == 2 && port == 2)
            return {header, 3, 2};
        if (node == 3 && port == 2)
            return {header, 2, 2};
        return {header, -1, -1};
    }

    int forward(PktState pktState) {
        for (int hop = 0; hop < 11; hop++) {
            pktState = node_execute(pktState);
            if (pktState.port == PORT_DROP) return pktState.port;
            pktState = link_function(pktState);
            if (pktState.port == PORT_DROP) return pktState.port;
        }
        return -1; //error
    }

public:
    Router1 node0;
    Router2 node1;
    Router3 node2;
    Router4 node3;
};

#endif