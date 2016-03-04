import shutil

import utils
from decoderState import DecoderState
from strategy.linearSweep import LinearSweepDecoder
from x86.decoder import X86Decoder

def test(StrategyClass, verbose, detail):
    testOps = []

    terminalSize = shutil.get_terminal_size((80, 20))
    
    testOps.append((b"\x01\xF7","ADD EDI, ESI"))
    testOps.append((b"\x03\x3E","ADD EDI, [ESI]"))
    testOps.append((b"\x03\x7E\x10","ADD EDI, [ESI + 0x10]"))
    testOps.append((b"\x03\xBE\x10\x00\x00\x00","ADD EDI, [ESI + 0x00000010]"))
    testOps.append((b"\x03\x3D\x00\x00\x00\x10","ADD EDI, [0x10000000]"))
    testOps.append((b"\x01\x7D\x00","ADD [EBP + 0x00], EDI"))
    testOps.append((b"\x81\xC7\x44\x33\x22\x11","ADD EDI, 0x11223344"))

    testOps.append((b"\x8B\xF3","MOV ESI, EBX"))
    testOps.append((b"\x89\x1E","MOV [ESI], EBX"))
    testOps.append((b"\x89\x1C\xF7","MOV [ESI*8 + EDI], EBX"))
    testOps.append((b"\xC7\x84\xB7\xDD\xCC\xBB\xAA\x44\x33\x22\x11","MOV [ESI*4 + EDI + 0xAABBCCDD], 0x11223344"))

    #testOps.append((b"\xC7\x04\xB5\x00\x00\x00\x00\x44\x33\x22\x11","MOV [ESI*4 + 0x00000000], 0x11223344")) # MOV [ ESI*4 ], 0x11223344
    testOps.append((b"\xC7\x04\xB5\x00\x00\x00\x00\x44\x33\x22\x11","MOV [ESI*4], 0x11223344"))

    testOps.append((b"\x89\x0C\xE4","MOV [ESP], ECX"))
    testOps.append((b"\x89\x0C\x24","MOV [ESP], ECX"))
    testOps.append((b"\x89\x0C\x64","MOV [ESP], ECX"))
    testOps.append((b"\x89\x0C\xA4","MOV [ESP], ECX"))


    failedTestIdxs = []
    for idx, testObj in enumerate(testOps):
        objectStr, expectedInstruction = testObj

        title = "TEST %d: %s"%((idx+1), repr(expectedInstruction))
        utils.logger.info((utils.colors.INVERT+title)+(" "*(terminalSize.columns-len(title))) +utils.colors.NORMAL )

        # Run...

        decoderState = DecoderState(objectStr=objectStr)

        decoderSpec = X86Decoder(decoderState)
        decoder = StrategyClass(decoderSpec)
        #decoderState.showDecodeProgress()

        decoder.decode(verbose=True, detail=True)

        decoderState.showDecodeProgress(detail=True)

        # Validate...

        foundInstructions = list(decoderState.instructions.values())
        if len(foundInstructions) != 1:
            raise RuntimeError("Too many instructions found!")

        inst = foundInstructions[0]
        if inst.upper() != expectedInstruction.upper():
            objStr = ' '.join('{:02x}'.format(x) for x in objectStr)
            utils.logger.info((utils.colors.RED+"Test %d Failed:"+utils.colors.NORMAL+"    %s\n\tExpected: %s\n\tFound   : %s\n") % (idx+1, objStr, expectedInstruction.upper(), inst.upper()))

            failedTestIdxs.append(idx)

    utils.logger.info((utils.colors.BOLD+"\nFailed Tests: %d\nTest Indexes: %s" + utils.colors.NORMAL) % (len(failedTestIdxs),", ".join([str(idx+1) for idx in failedTestIdxs])))
