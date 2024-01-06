#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

#define INPUT_MAX (23)

void no(void) {
  printf("Nope.\n");
  exit(1);
}

void ok(void) {
  printf("Good job.\n");
}

int main(void) {
  unsigned inputIdx, outputIdx;
  char letter[4];
  char input[INPUT_MAX + 1];
  char output[9];
  size_t len;

  printf("Please enter key: ");
  if (
    scanf("%23s", input) != 1
    || input[1] != '0'
    || input[0] != '0'
  )
    no();
  fflush(stdin);
  memset(output, 0, 9);
  output[0] = 'd';
  letter[3] = 0;
  outputIdx = 1;
  inputIdx = 2;
  while (true) {
    len = strlen(output);
    if (len == 8 || len >= strlen(input))
      break ;
    letter[0] = input[inputIdx];
    letter[1] = input[inputIdx + 1];
    letter[2] = input[inputIdx + 2];
    output[outputIdx++] = atoi(letter);
    inputIdx += 3;
  }
  output[outputIdx] = 0;
  if (!strcmp(output, "delabere"))
    ok();
  else
    no();
  return 0;
}
