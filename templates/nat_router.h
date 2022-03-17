#ifndef {{name_snake.upper()}}_H
#define {{name_snake.upper()}}_H

#include "common.h"
#include <string>

class {{name}} {
  public:
    {{name}}() {
        natTable[0].valid = 0;
        natTable[1].valid = 0;
        natTable[2].valid = 0;
    }

    PktState forward(PktState stateIn) { //generated-comment: [reached] {{name}}
        int node = stateIn.node;
        int portIn = stateIn.port;
        Header &header = stateIn.header;
        if (portIn == 0) { // inside
            for (int i = 0; i < 3; i ++) {
                if (natTable[i].valid && natTable[i].local_ip == header.src_address && natTable[i].local_port == header.src_port) {
                    header.src_address = natTable[i].global_ip;
                    header.src_port = natTable[i].global_port;
                    return {header, node, 1};
                }
            }

            // insert
            for (int i = 0; i < 3; i ++) {
                if (!natTable[i].valid) {
                    natTable[i].global_ip = *(uint32_t*) getSymbolicState(4);
                    natTable[i].global_port = *(uint16_t*) getSymbolicState(2);
                    klee_assume((natTable[i].global_ip >> {{32 - pool.prefix_len}}) == ({{pool.hex_address}} >> {{32 - pool.prefix_len}})); // {{pool.str_address}}/{{pool.prefix_len}}
                    natTable[i].local_ip = header.src_address;
                    natTable[i].local_port = header.src_port;
                    header.src_address = natTable[i].global_ip;
                    header.src_port = natTable[i].global_port;
                    return {header, node, 1};
                }
            }
            klee_assert(0);
        }
        if (portIn == 1) { // outside
            for (int i = 0; i < 3; i ++) {
                if (natTable[i].valid && natTable[i].global_ip == header.dst_address && natTable[i].global_port == header.dst_port) {
                    header.dst_address = natTable[i].local_ip;
                    header.dst_port = natTable[i].local_port;
                    return {header, node, 0};
                }
            }
        }
        return {header, node, -1};
    }

  private:
    struct tableEntry {
       bool valid;
       uint32_t local_ip;
       uint32_t local_port;
       uint32_t global_ip;
       uint32_t global_port;
    };

    tableEntry natTable[3];
};

#endif
