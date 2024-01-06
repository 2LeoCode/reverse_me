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

patcher.patch(binaryFolder / "level2", {
  # 1 - remove the first character check
  # replace:
  #   1340: e8 db fe ff ff          call   1220 <no>
  # by:
  #   1340: 90                      nop
  #   1341: 90                      nop
  #   1342: 90                      nop
  #   1343: 90                      nop
  #   1344: 90                      nop
  0x1340: b"\x90\x90\x90\x90\x90",
  # 2 - remove the second character check
  # replace:
  #   1359: e8 c2 fe ff ff          call   1220 <no>
  # by:
  #   1359: 90                      nop
  #   135a: 90                      nop
  #   135b: 90                      nop
  #   135c: 90                      nop
  #   135d: 90                      nop
  0x1359: b"\x90\x90\x90\x90\x90",
  # 3 - remove the continue condition to skip the loop (not mandatory)
  # replace:
  #   13f3: 0f 85 05 00 00 00       jne    13fe <main+0x12e>
  # by:
  #   13f3: 90                      nop
  #   13f4: 90                      nop
  #   13f5: 90                      nop
  #   13f6: 90                      nop
  #   13f7: 90                      nop
  #   13f8: 90                      nop
  0x13f3: b"\x90\x90\x90\x90\x90\x90",
  # 4 - replace the call to strcmp by xor eax, eax
  # replace:
  #   1465: e8 d6 fb ff ff          call   1040 <strcmp@plt>
  # by:
  #   1465: 90                      nop
  #   1466: 90                      nop
  #   1467: 90                      nop
  #   1468: 31 c0                   xor %eax,%eax
  0x1465: b"\x90\x90\x90\x31\xc0",
})
