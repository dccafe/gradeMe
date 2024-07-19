from subprocess import run
from os.path    import join
from os         import listdir as ls, \
                       remove  as rm

def compile(SRCFILE):
    # Compile
    root    = 'upload' 
    OBJDIR  = join(root,'obj')
    SRCDIR  = join(root,'src')
    BINDIR  = join(root,'bin')
    GCCDIR  = 'C:\\sdcard\\mspgcc\\'
    GCCBIN  = GCCDIR + 'bin\\'
    GCCINC  = GCCDIR + 'include\\'

    for directory in [OBJDIR, BINDIR]:
    	for file in ls(directory):
    		rm(file)

    cc = join(GCCBIN,'msp430-elf-gcc.exe')
    ld = join(GCCBIN,'msp430-elf-ld.exe' )
    db = join(GCCBIN,'msp430-elf-gdb.exe')

    ccOpt = f'-I {GCCINC} -mmcu=msp430f5529 -c -g -O0 -msmall'.split()
    ldOpt = f'-L {GCCINC} -T {GCCINC}\\msp430f5529.ld'.split()

    CHKFILE = 'check-' + SRCFILE.split('.')[0] + '.c'

    cFiles     = [SRCDIR + CHKFILE]
    asmFiles   = [SRCDIR + SRCFILE, SRCDIR + 'reset.S']
    objFiles   = [f.replace('.c','.o').replace('src','obj') for f in cFiles] + \
                 [f.replace('.S','.s').replace('src','obj') for f in asmFiles]

    print('Compiling')
    for (obj,src) in zip(objFiles, cFiles+asmFiles):
        cmd = [cc] + ccOpt + ['-o', obj, src]
        p = run()

    print('Linking')
    p = run([msp430ld] + ['-o', BINDIR + 'msp430f5529.elf'] + ldOptions + objFiles)

    return p.returncode

def check(testcases):

    # Start gdb process
    gdbmi = GdbController(command=[msp430gdb, BINDIR + 'msp430f5529.elf', '--interpreter=mi3'])
    gdbmi.write('-target-select remote :55000', timeout_sec=10)
    gdbmi.write('-target-download ', timeout_sec=10)

    for t in testcases:

        gdbmi.write(f'-break-insert {t[line]}', timeout_sec=10)
        gdbmi.write('-exec-continue', timeout_sec=10)
        sleep(1)

        result = gdbmi.write('-data-list-register-values x 28', timeout_sec=10)
        r12 = result[-1]['payload']['register-values'][0]['value']
        
        if r12 == t['result']:
            grade += t['grade']

