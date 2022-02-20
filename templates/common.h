#ifndef COMMON_H
#define COMMON_H

#include <klee/klee.h>
#include <cstdint>
#include <cassert>

#define PORT_DROP (-1)

struct Header {
    uint32_t src_address;
    uint32_t dst_address;
    uint8_t protocol;
    uint16_t src_port;
    uint16_t dst_port;
};

struct PktState {
    Header header;
    int node;
    int port;

    PktState(Header h,  int n, int p) :
            header(h),
            node(n),
            port(p) {}
};

#endif