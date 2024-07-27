	.global uMax 			; Exporta o s�mbolo uMax
	.text					; Conte�do vai para a ROM

uMax:
	tst		R13
	jz		uMax_empty

	push	R4				; Faz um backup dos
	push	R5				; registradores que vamos usar
	mov.w	R12, R4			; Parametros de entrada em R4
	mov.b	#0x00, R5		; e R5 (maior valor atual)

uMax_loop:
	cmp.b	@R4+, R5		; Compara o valor do vetor
	jhs		uMax_continue	; com o maior que j� encontramos

uMax_get:
	mov.b	-1(R4), R5		; Encontramos um elemento maior

uMax_continue:
	dec		R13				; Verifica se o vetor j� terminou
	jnz		uMax_loop		; caso n�o tenha terminado, volte
							; para o loop

	mov.b	R5, R12			; Retorno em R12 (conven��o)

uMax_ret:
	pop		R5				; Restaura os valores anteriores
	pop		R4				; de R4 e R5
	ret						; e retorna o resultado
	
uMax_empty:					; Se o vetor estiver vazio 
	clr		R12				; retorna 0x00
	ret
