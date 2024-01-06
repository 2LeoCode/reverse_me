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
  patcher.patch(binaryFolder / "level3", {
    # 1 - remove the first character check
    # replace:
    #   1376: e8 65 ff ff ff          call   12e0 <___syscall_malloc>
    # by:
    #   1376: 90                      nop
    #   1377: 90                      nop
    #   1378: 90                      nop
    #   1379: 90                      nop
    #   137a: 90                      nop
    0x1376: b"\x90\x90\x90\x90\x90",
    # 2 - remove the second character check
    # replace:
    #   138c: e8 4f ff ff ff          call   12e0 <___syscall_malloc>
    # by:
    #   138c: 90                      nop
    #   138d: 90                      nop
    #   138e: 90                      nop
    #   138f: 90                      nop
    #   1390: 90                      nop
    0x138c: b"\x90\x90\x90\x90\x90",
    # 3 - remove the continue condition to skip the loop (not mandatory)
    # replace:
    #   1408: 0f 85 05 00 00 00       jne    13fe <main+0x12e>
    # by:
    #   1408: 90                      nop
    #   1409: 90                      nop
    #   140a: 90                      nop
    #   130b: 90                      nop
    #   130c: 90                      nop
    #   130d: 90                      nop
    0x1408: b"\x90\x90\x90\x90\x90\x90",
    # 4 - replace the call to strcmp by xor eax, eax
    # replace:
    #   1475: e8 d6 fb ff ff          call   1040 <strcmp@plt>
    # by:
    #   1475: 90                      nop
    #   1476: 90                      nop
    #   1477: 90                      nop
    #   1478: 31 c0                   xor %eax,%eax
    0x1475: b"\x90\x90\x90\x31\xc0",
  })
except Exception as e:
  failure(e)
