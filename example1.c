#include <stdio.h>
#include <stdlib.h>

// void top(char input[]) {
//   int cnt = 0;
//   if (input[0] == 'b') cnt++;
//   if (input[1] == 'a') cnt++;
//   if (input[2] == 'd') cnt++;
//   if (input[3] == '!') cnt++;
//   if (cnt >= 3) abort(); // error
// }

int main(int argc, char *argv[]) {
  char *input = argv[1];
  int cnt = 0;
  if (input[0] == 'b') cnt++;
  if (input[1] == 'a') cnt++;
  if (input[2] == 'd') cnt++;
  if (input[3] == '!') cnt++;
  if (cnt >= 3) abort(); // error
  return 0;
}
