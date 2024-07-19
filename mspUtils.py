import os

from subprocess import run
from flask import flash as alert

OBJDIR     = 'upload\\obj\\'
SRCDIR     = 'upload\\src\\'
BINDIR     = 'upload\\bin\\'

GCCPATH    = 'C:\\sdcard\\mspgcc\\'
GCCBIN     = GCCPATH + 'bin\\'
GCCINC     = GCCPATH + 'include\\'

msp430gcc  = GCCBIN + 'msp430-elf-gcc.exe'
msp430ld   = GCCBIN + 'msp430-elf-ld.exe'
msp430gdb  = GCCBIN + 'msp430-elf-gdb.exe'

gccOptions = f'-c -I inc -I {GCCINC} -mmcu=msp430f5529 -O0 -msmall -g'.split()
ldOptions  = f'          -L {GCCINC} -T {GCCINC}\\msp430f5529.ld'.split()

def compile(filename):

    basename = filename.split('.')[0].split('-')[1]
    print(basename)

    SRCFILE = filename
    CHKFILE = 'check-' + basename + '.c'

    dirs = [OBJDIR, BINDIR]
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)

    cFiles     = [SRCDIR + CHKFILE]
    asmFiles   = [SRCDIR + SRCFILE, SRCDIR + 'reset.S']
    objFiles   = [f.replace('.c','.o').replace('src','obj') for f in cFiles] + \
                 [f.replace('.S','.s').replace('src','obj') for f in asmFiles]

    print('Compiling')
    for (obj,src) in zip(objFiles, cFiles+asmFiles):
        print(src)
        p = run([msp430gcc] + gccOptions + ['-o', obj, src])

    print('Linking')
    p = run([msp430ld] + ldOptions + ['-o', BINDIR + 'msp430f5529.elf'] + objFiles)

def flash():
    from pygdbmi.gdbcontroller import GdbController

    print('Flashing')

    # Start gdb process
    gdbmi = GdbController(command=[msp430gdb, BINDIR + 'msp430f5529.elf', '--interpreter=mi3'])
    gdbmi.write('-target-select remote :55000', timeout_sec=10)
    gdbmi.write('-target-download ', timeout_sec=10)
    
    return gdbmi



def runTests(gdbmi, mod, num):

    def runUntil(line):
        from time import sleep

        regs = [0]*16

        gdbmi.write(f'-break-insert {line}', timeout_sec=10)
        gdbmi.write('-exec-continue', timeout_sec=10)
        sleep(1)
        result = gdbmi.write('-data-list-register-values x', timeout_sec=10)
        for reg in result[-1]['payload']['register-values']:
            regs[int(reg['number']) - 16] = int(reg['value'], 0)

        return regs

    print('testing')

    from testcases import testcases

    grade = 0
    details = ''
    for test in testcases[mod][num]:
        print(test['description'], end=' ')
        regs = runUntil(test['line'])
        check = []
        for regNum, value in test['result']:
            check.append(regs[regNum] == value)
        if all(check):
            grade += test['grade']
            details += str(test['grade']) 
        else:
            details += '0'
        print('Grade: ', grade)
        details += '/' + str(test['grade']) + ': ' + test['description'] + '\n'

    details += 'Total: ' + str(grade)
    print(details)

    gdbmi.write('-target-detach')
    gdbmi.exit()

    return grade, details