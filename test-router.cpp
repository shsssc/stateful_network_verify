#include <klee/klee.h>

class Router {
  public:
	int forward (uint32_t dst) {
		if ((dst & 0xFFFF0000) == ((192 << 24) | (168 << 16))) {
			return 1;
		} else if ((dst & 0xFF000000) == (10 << 24)) {
			return 2;
		} else {
			return 0;
		}
	}
};

int main() {
	uint32_t dst;
	klee_make_symbolic(&dst, sizeof(dst), "dst");
	int port = Router().forward(dst);
	return 0;
}
