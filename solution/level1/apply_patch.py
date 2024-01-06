if __name__ != "__main__":
  raise Exception("This file is not a module")


import sys
from pathlib import Path

if (libPath := str((Path(__file__).parent / "../../lib").absolute())) not in sys.path:
  sys.path.append(libPath)

import patcher

def printUsage():
  print("Usage: apply_patch.py <binary_folder>", file=sys.stderr)

def failure(reason: object):
  print(f"Error: {reason}.", file=sys.stderr)
  printUsage()
  exit(1)

if len(sys.argv) != 2:
  failure("invalid number of arguments")

binaryFolder = Path(sys.argv[1])

if not binaryFolder.is_dir():
  failure("binary_folder must be a directory")

try:
  patcher.patch(binaryFolder / "level1", {
    # replace:
    #   123c: e8 ff fd ff ff          call   1040 <strcmp@plt>
    # by:
    #   123c: 90                      nop
    #   123d: 90                      nop
    #   123e: 90                      nop
    #   123f: 31 c0                   xor    %eax,%eax
    # (need to fill with nop to keep the same code size,
    # otherwise the output file would be corrupted)
    0x123c: b"\x90\x90\x90\x31\xc0",
  })
except Exception as e:
  failure(e)
