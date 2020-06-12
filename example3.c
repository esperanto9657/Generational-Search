#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char *argv[]) {
  int x = strtol(argv[1], NULL, 10);
  int y = strtol(argv[2], NULL, 10);

  int z = x + y;
  int w = y * y;
  if(z <= 1) {
    if(((z + w) % 7 == 0) && (x % 7 != 0)) {
      abort();
    }
  }
  else {
    if((int)(pow(2.0, z) - 1) % z != 0) {
      abort();
    }
    else {
      z = z + w;
      abort();
    }
  }
  z = z * z;
}
