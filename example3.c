#include <stdio.h>
#include <stdlib.h>
#include <math.h>

void foo(int z, int w) {
}

void baz(int x, int y, int z) {
}

void quz(int x, int y, int z) {
}

void bar(int x, int y, int z) {
}

int main(int argc, char *argv[]) {
  int x = strtol(argv[0], NULL, 10);
  int y = strtol(argv[1], NULL, 10);

  int z = x + y;
  int w = y * y;
  if(z <= 1) {
    if(((z + w) % 7 == 0) && (x % 7 != 0)) {
      foo(z, w);
    }
  }
  else {
    if((int)(pow(2, z) - 1) % z != 0) {
      bar(x, y, z);
    }
    else {
      z = z + w;
      baz(z, y, x);
    }
  }
  z = z * z;
  quz(x, y, z);
}
