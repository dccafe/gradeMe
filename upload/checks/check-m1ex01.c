#include <msp430.h> 
#include <stdint.h>

uint8_t uMax(const uint8_t * vetor, const uint16_t size);

void main()
{    
    WDTCTL = WDTPW | WDTHOLD;
 
    volatile uint8_t grade = 0;

    const uint8_t testVector0[] = {0x10, 0x7F, 0x73, 0x5A};
    const uint8_t result0 = 0x7F, size0 = 4;

    const uint8_t testVector1[] = {0x80, 0xFF, 0x9B, 0xD2, 0xAB, 0xCD, 0x8F, 0xED};
    const uint8_t result1 = 0xFF, size1 = 8;

    const uint8_t testVector2[] = {0x10, 0x8F, 0x73, 0x5A, 0xE4, 0xAB, 0x7F, 0xCD};
    const uint8_t result2 = 0xE4, size2 = 8;

    const uint8_t testVector3[] = {0x01};
    const uint8_t result3 = 0x00, size3 = 0;

    const uint8_t * testVector[] = {testVector0, testVector1, testVector2, testVector3};
    const uint8_t result[]       = {result0,     result1,     result2,     result3};
    const uint8_t size[]         = {size0,       size1,       size2,       size3};

    uint8_t i = 4;
    while(i--)
    {
        if (result[i] == uMax(testVector[i], size[i]))
            grade |= 1 << i;
    }

    while(1);
}

