# Mini x86 Disassembler

This python3 script (`main.py`) attempts to parse arbitrary binary input
into x86 assembly code.

* Use linear sweep to disassemble an arbitrary binary file:
  `./main.py --linear-sweep -b <path-to-binary-file>`

* Use recursive descent to disassemble an arbitrary binary file:
  `./main.py --recursive-descent -b <path-to-binary-file>`

* Use linear sweep to disassemble the class examples plus a hand crafted example
  (example1, example2, ex2, jlex):
  `./main.py --linear-sweep --test-examples`

* Debug an issue, see all steps in the disassembly process:
  `./main.py ... -v` or `./main ... -vv`

## Assumptions / Features

* Only tested under linux (fedora) with python 3.4.3 .

* Both recursive descent and linear sweep algorithms are implemented.

* Code starts at offset 0 in the given file. Headers are not accounted for.

* Only the following mnemonics are implemented:
    add nop and not call or cmp pop dec push idiv repne cmpsd imul retf inc retn
    jmp sal jz/jnz sar lea sbb mov shr movsd test mul xor neg

* Upon encountering an unknown opcode, the disassembler notes the issue and attempts
  to continue. Upon an unrecoverable error the disassembler exits gracefully noting
  the current byte position of issue.

* Jumping/calling forwards and backwards is supported.

* All register references will be 32-bit references. The only exception is the
  `retn 16-bit` instruction.

* Labels are supported.

* If there is an unexpected error and you wish to see more output to debug the issue
  add `-v` to your command. Add another `-v` for more verbosity.

## CLI Help
```
usage: main.py [-h] [-b BINARY] [-v] [--recursive-descent] [--linear-sweep]
               [--test-examples] [--test-unit]

optional arguments:
  -h, --help            show this help message and exit
  -b BINARY, --binary BINARY
                        Disassemble the given binary file.
  -v, --verbosity       Show verbosity. Add more -v's to show more detail
  --recursive-descent   Use the recursive descent method.
  --linear-sweep        Use the linear sweep method.
  --test-examples       Disassemble the class examples (example1, example2,
                        ex2)
  --test-unit           Disassemble unit examples (one instruction at a time)
```
