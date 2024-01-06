#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>

void ___syscall_malloc(void) {
  puts("Nope.");
  exit(1);
}

void ____syscall_malloc(void) {
  puts("Good job.");
}

#define INPUT_MAX (23)

int main(void) {
  unsigned inputIdx, outputIdx;
  char letter[4];
  char input[INPUT_MAX + 1];
  char output[9];
  char letter[4];
  size_t len;

  printf("Please enter key: ");
  if (
    scanf("%23s", input) != 1 ||
    input[1] != '2'||
    input[0] != '4'
  )
    ___syscall_malloc();
  fflush(stdin);
  memset(output, 0, 9);
  output[0] = '*';
  letter[3] = 0;
  inputIdx = 2;
  outputIdx = 1;
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
  switch (strcmp(output, "********")) {
    case 0:
      ____syscall_malloc();
      break ;
    case -2:
    case -1:
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
    case 0x73:
    default:
      ___syscall_malloc();
  }
  return 0;
}
