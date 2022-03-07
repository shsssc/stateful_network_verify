#ifndef {{name_snake.upper()}}_H
#define {{name_snake.upper()}}_H

#include "common.h"

class {{name}} {
  public:
    PktState forward(PktState stateIn) { //generated-comment: [reached] {{name}}
        int node = stateIn.node;
        int portIn = stateIn.port;
        Header &header = stateIn.header;
{{code}}
        assert(0);
    }
};

#endif
