from pathlib import Path
import os, stat

def patch(
    binaryPath: str | Path,
    edits: dict[int, bytes],
  ):
  path = Path(binaryPath)
  with path.open("rb") as f:
    content = bytearray(f.read())

  for address, replaceBytes in edits.items():
    content[address:address+len(replaceBytes)] = replaceBytes
  
  with open(
      f"{path.name}.patch",
      "wb",
      opener=lambda path, flags: os.open(
          path, flags, stat.S_IWUSR | stat.S_IRUSR | stat.S_IEXEC
        )
    ) as f:
    f.write(content)
