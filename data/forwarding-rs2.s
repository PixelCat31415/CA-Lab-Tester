add x1, zero, zero

add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops

; forwarding MEM -> EX
addi x1, x1, 42
add x2, zero, x1

add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops

; forwarding WB -> EX
addi x1, x1, 42
add x23, x23, x23  ; nops
add x3, zero, x1

add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops

; forwarding MEM, WB -> EX
addi x1, x1, 42
addi x1, x1, 42
add x4, zero, x1

add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops

; no forwarding
addi x1, x1, 42
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x5, zero, x1

add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops

; no forwarding from x0
addi x0, zero, 42
add x6, x1, x0

add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops

; no forwarding from x0
addi x0, zero, 42
add x23, x23, x23  ; nops
add x7, x1, x0

add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops

; no forwarding from x0
addi x0, zero, 42
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x8, x1, x0
