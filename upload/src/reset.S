; Header: 
;   Include msp430 header file
;   Defines global label main
#include <msp430.h>

			.global main
; -----------------------------------------------------------------------------
; Flash section 
; -----------------------------------------------------------------------------
			.section .text

; This is the reset ISR
RESET:	 	BR		#main

; -----------------------------------------------------------------------------
; ISR Address Table (also in flash)
; -----------------------------------------------------------------------------
			.section ".resetvec","ax"
			.word 	RESET