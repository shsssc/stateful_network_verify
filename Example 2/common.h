#ifndef COMMON_H
#define COMMON_H

#include <klee/klee.h>
#include <cstdint>
#include <cassert>

struct Header {
    uint32_t src_address;
    uint32_t dst_address;
    uint8_t protocol;
    uint16_t src_port;
    uint16_t dst_port;
};

struct Egress {
    Header header;
    int port;

    Egress(Header h, int p) :
        header(h),
        port(p)
    {}
};

struct Location {
    int node;
    int port;

    Location(int n, int p) :
        node(n),
        port(p)
    {}
};

#endif