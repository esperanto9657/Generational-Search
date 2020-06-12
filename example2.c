#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
  char *s = argv[1];
  int x = s[0] - '0';
  int y = s[1] - '0';

  int z = x + y;
  if(x >= 5) {
    y = y + z;
    if(y < x) {
      abort();
    }
  }
  else {
    abort();
  }
}
