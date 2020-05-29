#include <stdio.h>
#include <stdlib.h>

void foo(int x, int y, int z) {
}

void baz(int x, int y, int z) {
}

void qux(int x, int y, int z) {
}

void bar(int x, int y, int z) {
}

int main(int argc, char *argv[]) {
  int x = strtol(argv[0], NULL, 10);
  int y = strtol(argv[1], NULL, 10);

  int z = x + y;
  if(x >= 5) {
    foo(x, y, z);
    y = y + z;
    if(y < x) {
      baz(x, y, z);
    }
    else {
      qux(x, y, z);
    }
  }
  else {
    bar(x, y, z);
  }
}
