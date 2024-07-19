#include <msp430.h> 
#include <stdint.h>

uint8_t uMax(uint8_t * vetor, uint16_t size);
uint8_t result; 

void main()
{    
    WDTCTL = WDTPW | WDTHOLD;
    P1DIR |=  BIT0;
    P4DIR |=  BIT7;
    P4OUT &= ~BIT7;
    P1OUT |=  BIT0;  
 
    uint8_t testVector1[] = {0x10, 0x7F, 0x73, 0x5A};
    result = uMax(testVector1, 4);

    P4OUT |=  BIT7;

    uint8_t testVector2[] = {0x80, 0xFF, 0x9B, 0xD2, 0xAB, 0xCD, 0x8F, 0xED};
    result = uMax(testVector2, 8);

    P4OUT &= ~BIT7;  

    uint8_t testVector3[] = {0x10, 0x8F, 0x73, 0x5A, 0xE4, 0xAB, 0x7F, 0xCD};
    result = uMax(testVector3, 8);

    P4OUT |=  BIT7;

    uint8_t testVector4[] = {0x01};
    result = uMax(testVector4, 0);

    P4OUT &= ~BIT7;  

    while(1)
    {
        P1OUT ^= BIT0;
        __delay_cycles(1000000);
    }

}

