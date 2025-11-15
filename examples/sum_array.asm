; Sum of array example
; Assumes array starts at address 0x0100
; R0 = base address (0x0100)
; R1 = current pointer
; R2 = sum accumulator
; R3 = counter
; R4 = current value

        ADDI R0, R0, 0x0100  ; Set base address (simplified - would need MOVI)
        ADDI R1, R0, 0       ; R1 = base address
        ADDI R2, R2, 0       ; sum = 0
        ADDI R3, R3, 10      ; count = 10

loop:   LOAD R4, R1, 0      ; load *R1
        ADD  R2, R2, R4     ; sum += value
        ADDI R1, R1, 2       ; R1 += 2 (next element, word-aligned)
        ADDI R3, R3, -1      ; count--
        BRZ  R3, done        ; if count == 0, done
        JMP  loop            ; continue loop

done:   HALT

