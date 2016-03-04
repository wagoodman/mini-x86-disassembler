import shutil

import utils
from decoderState import DecoderState
#from strategy.linearSweep import LinearSweepDecoder
from x86.decoder import X86Decoder

example1 = ("test/example1.o","test/example1.S")
example2 = ("test/example2.o","test/example2.S")
ex2 = ("test/ex2","test/ex2.S")
jlex = ("test/jlex.o","test/jlex.S")

examples = (example1, example2, ex2, jlex)

def test(StrategyClass, tests=None, verbose=False, detail=False):

    if not tests:
        tests = range(0,len(examples))

    for idx in tests:
        testEx(idx, StrategyClass, verbose, detail)
        utils.logger.info("\n\n")

def testEx(exIdx, StrategyClass, verbose, detail):

    terminalSize = shutil.get_terminal_size((80, 20))

    example = examples[exIdx]

    strategyName = StrategyClass.__name__
    utils.logger.info(utils.colors.BOLD + ("Running %s with a strategy of %s" %(repr(example[0]), repr(strategyName) )) + utils.colors.NORMAL )

    objectStr = open(example[0],'rb').read()

    # Run...

    decoderState = DecoderState(objectStr=objectStr)

    decoderSpec = X86Decoder(decoderState)
    decoder = StrategyClass(decoderSpec)
    #decoderState.showDecodeProgress()

    decoder.decode(verbose=verbose, detail=detail)

    decoderState.showDecodeProgress(detail=True)

    if decoderState.isComplete():

        utils.logger.info(utils.colors.GREEN+utils.colors.INVERT+(" "*(terminalSize.columns))+utils.colors.NORMAL)
        title = "Completed disassembly of %s"%repr(example[0])
        utils.logger.info(utils.colors.GREEN+utils.colors.INVERT+(title + " "*(terminalSize.columns-len(title)))+utils.colors.NORMAL)
        utils.logger.info(utils.colors.GREEN+utils.colors.INVERT+(" "*(terminalSize.columns))+utils.colors.NORMAL)

    elif not decoderState.isComplete() and decoderState.isSweepComplete():

        utils.logger.info(utils.colors.YELLOW+utils.colors.INVERT+(" "*(terminalSize.columns))+utils.colors.NORMAL)
        title = "Almost completed disassembly of %s. A few bytes remain encoded when using Linear Sweep method."%repr(example[0])
        utils.logger.info(utils.colors.YELLOW+utils.colors.INVERT+(title + " "*(terminalSize.columns-len(title)))+utils.colors.NORMAL)
        utils.logger.info(utils.colors.YELLOW+utils.colors.INVERT+(" "*(terminalSize.columns))+utils.colors.NORMAL)
    elif not decoderState.isComplete() and decoderState.isRecursiveDescentComplete():

        utils.logger.info(utils.colors.YELLOW+utils.colors.INVERT+(" "*(terminalSize.columns))+utils.colors.NORMAL)
        title = "Almost completed disassembly of %s. A few bytes remain encoded when using Recursive Descent method."%repr(example[0])
        utils.logger.info(utils.colors.YELLOW+utils.colors.INVERT+(title + " "*(terminalSize.columns-len(title)))+utils.colors.NORMAL)
        utils.logger.info(utils.colors.YELLOW+utils.colors.INVERT+(" "*(terminalSize.columns))+utils.colors.NORMAL)
    else:

        utils.logger.info(utils.colors.YELLOW+utils.colors.BOLD + ("Could not finish processing %s" %repr(example[0])) + utils.colors.NORMAL )
