# GradeMe - MSP430 Edition
#### Video Demo:  https://youtu.be/pFw0jGdNF2c
#### Description:
This is a web application to grade automatically exercises for an embedded systems course on MSP430 microcontrollers. Exercises are loaded into the microcontroller and verified for correctness. A grade is then given back to the student according to his work. 

Background: I'm a professor at University of Brasília, Brazil, where I teach a course on microcontrollers. We are using Texas Instruments MSP430 for our course. Our course is organized into 3 parts that we call "modules".

The first module focuses on the microcontroller architecture and all programs are written in Assembly. The second part focuses on GPIOs and Timers and the third part is all about communication and A/D conversion. For the second and third modules, we use C programming language.

Inspired by "check50", this project is supposed to help students verify their work automatically and get insights on what they are doing wrong. 

The project is composed of a web application that comunicates to the microcontroller via GDB bridge in order to load code into the microcontroller, run testcases and collect the results from internal registers and memory. The GDB bridge is composed of two softwares. A "GDB agent" server creates a USB connection to the programmer interface and listens to gdb commands. With the server active and the microcontroller connected, we can use GDB to send and receive data to the microcontroller. 

I'm using GDB's machine interface as it is easier for a computer to parse GDB's output. This is done by python's pygdbmi module. When GDB agent server is running, we can connect to it using a remote target on port 55000. Then we proceed to load the compiled binary and run the different testcases. 

There are quite a few strategies to verify the correctness of a given code for a microcontroller. The strategy will depend on the module. 

In the first module, where we explore the microcontroller's architecture, all exercises are written in assembly language. To verify that a given program has executed correctly, we only need one microcontroller to run the testcases. For each testcase, we stop the execution of the program and read back the expected result of the internal registers. For example, if the exercise demands the student to write a software to search for the biggest element of an array, it should be provided with different arrays and also exceptional cenarios. Examples:

1) Test vector [0x01, 0x80, 0x23, 0x45] should be able to test if the student is using the correct instruction for signed or unsigned numbers. The biggest element is 0x45 if numbers are interpreted as signed or 0x80 if numbers are interpreted as unsigned. 

2) An empty vector could be used to verify if the user is checking for a bad usage cenario. 

3) Using test vector 1 with size = 2, should test if the student is using byte or word instructions. The MSP430 uses little endian memory organization, so that test vector 1 is the same as [0x8001, 0x4523] if elements are interpreted as words. This should also work for the sign test (testcase 1).

4) Very long arrays can be used to check for the algorithm performance, although this is not the focus of our course.

From the second module onwards, the tests get a little bit more complicated, as we focus on more complex functionalities. We can always use GDB to read memory and peripheral's configuration but there are so many ways to solve these class of problems that this approach would limit the student's creativity. 

Another aproach would be to use two microcontrolers. One for the student's code and a second to run an embedded tester. The tester would treat the student's solution as a black box, only checking for what we can observe from the outside. For example, if the student is requested to make the LED blink at a certain frequency, we should measure it and match it with a given margin of error as digital oscillators are not 100% accurate. 

If the student is supposed to work with mechanical switches, they might present switching noise. It is expected that the student program some sort of debounce strategy. With the two microcontrollers approach, we can emulate switching noise and also test situations where we expect a pull-up or pull-down resistor.

Serial communication will follow the same approach. We should evaluate if the baudrate is correct, check if the messages are beeing delivered and if the correct functionality is present. 

When it comes to A/D conversion, aditional peripherals are needed. In order to test the internal A/D converter, we need a D/A converter. Unfortunatelly, the MSP430F5529, used in our course does not offers such peripheral. We should use an external D/A converter pluged-in over SPI or I2C interface. 

These are all milestones that we want to achieve in the near future. Considering the scope of this course, this final project will focus only on verifying simple testcases as a proof-of-concept. 

How to use the software: The user must register in order to use the check functionality. In the register view, the user must enter his enrolment ID and a password of choice (twice). Once registered, it can procede with the login and then the "check" view will be available. 

In the "check" view there is only a form to submit a file. The name of the file is used to select the correct exercise. The name of the file should be as follows: 

- m\<mod\>ex\<num\>.\<ext\>

Where \<mod\> and \<num\> are the values of the module and the exercise number, respectivelly. The \<num\> value should be entered using two digits with left zero padding if necessary. The file extension in \<ext\> will be either "S" for assembly files or "c" for C files. Examples:

- m1ex01.S
- m3ex13.c

When the user submit one file, it will trigger the compile/link process. The app will select the corresponding test case by the name of the file. Then it will compile the exercise, the validation test case and a file called "reset.S" that is used to start the program when the microcontroller is reseted, turned on, or in the debug session. 

Finally, the debuger gets connected to the "GDB agent" server and will flash the microcontroller with the freshly cooked binary. The debugger will execute test by test placing breakpoints automatically and waiting for the software to execute. Once finished, the debugger will load register values and compare it to the expected results. At the end, the exercise should be graded and the user is redirected to the index, where all the grades are listed.


