	.global uMin 			; Exporta o s�mbolo uMin
	.text					; Conte�do vai para a ROM

uMin:
	push	R4				; Faz um backup dos
	push	R5				; registradores que vamos usar
	mov.w	R12, R4			; Parametros de entrada em R4
	mov.b	#0xFF, R5		; e R5 (maior valor atual)

uMin_loop:
	cmp.b	@R4+, R5		; Compara o valor do vetor
	jlo		uMin_continue	; com o maior que j� encontramos

uMin_get:
	mov.b	-1(R4), R5		; Encontramos um elemento maior

uMin_continue:
	dec		R13				; Verifica se o vetor j� terminou
	jnz		uMin_loop		; caso n�o tenha terminado, volte
							; para o loop

	mov.b	R5, R12			; Retorno em R12 (conven��o)

	pop		R5				; Restaura os valores anteriores
	pop		R4				; de R4 e R5
	ret						; e retorna o resultado
	