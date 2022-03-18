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

    void reverse() {
        uint32_t tmp = src_address;
        src_address = dst_address;
        dst_address = tmp;

        uint16_t tmp2 = src_port;
        src_port = dst_port;
        dst_port = tmp2;
    }
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

uint8_t shared_symbolic_state[256];
uint32_t used_state_len = 0;

uint8_t *getSymbolicState(uint32_t size) {
    uint8_t * a = shared_symbolic_state + used_state_len;
    used_state_len += size;
    return a;
}


#endif
