#include <msp430.h> 
#include <stdint.h>

uint8_t uMin(uint8_t * vetor, uint16_t size);

void main()
{    
    WDTCTL = WDTPW | WDTHOLD;
    P1DIR |=  BIT0;
    P4DIR |=  BIT7;
    P4OUT &= ~BIT7;
    P1OUT |=  BIT0;  
 
    uint8_t testVector[] = {0x10, 0xAB, 0x73, 0x01};
    uint8_t result = uMin(testVector, 4);

    P4OUT |=  BIT7;

    while(1)
    {
        P1OUT ^= BIT0;
        __delay_cycles(1000000);
    }

}

