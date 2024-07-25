import os

from subprocess             import run
from pygdbmi.gdbcontroller  import GdbController
from time                   import sleep
from testcases              import testcases

GCCDIR = 'C:\\sdcard\\mspgcc\\'
CCSDIR = 'C:\\sdcard\\ccs'
CCXDIR = 'ccs\\tools\\compiler\\ti-cgt-msp430_21.6.1.LTS'

cl430 = [f'{CCSDIR}\\{CCXDIR}\\bin\\cl430']
cl430opt = f'-g -D__MSP430F5529__ -i{CCSDIR}\\ccs\\ccs_base\\msp430\\include -i{CCSDIR}\\{CCXDIR}\\include -i{CCSDIR}\\{CCXDIR}\\lib'.split()
cl430lnk = '--run_linker lnk_msp430f5529.cmd'.split()

msp430gdb  = GCCDIR + '\\bin\\msp430-elf-gdb.exe'

def compile(sources, executable):

    print('Compiling files ', sources, 'into', executable)
    cl430out = ['-o', executable]
    cmd = cl430 + sources + cl430opt + cl430lnk + cl430out
    run(cmd, cwd='upload')

def flash(binary):

    print('Flashing', binary)

    # Start gdb process
    gdbmi = GdbController(command=[msp430gdb, 'upload\\' + binary, '--interpreter=mi3'])
    gdbmi.write('-gdb-set mi-async on')
    gdbmi.write('-target-select remote :55000', timeout_sec=5)
    gdbmi.write('-target-download', timeout_sec=5)
    
    return gdbmi

def runTests(gdbmi, mod, num):

    gdbmi.write('-exec-continue', timeout_sec=2)
    sleep(0.5)
    gdbmi.write('-exec-interrupt')
    output = gdbmi.write('-data-evaluate-expression grade', timeout_sec=10)

    result = int(output[-1]['payload']['value'].split()[0])

    mask    = 1
    grade   = 0
    details = ''
    for test in testcases[mod][num]:
        print(test['description'], end=' ')
        if result & mask:
            grade += test['grade']
            details += str(test['grade']) 
        else: 
            details += '0'

        mask <<= 1

        print('Grade: ', grade)
        details += '/' + str(test['grade']) + ': ' + test['description'] + '\n'

    details += 'Total: ' + str(grade)
    print(details)

    gdbmi.write('-target-detach')
    gdbmi.exit()

    return grade, details