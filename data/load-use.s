; load-use hazard (rs1)
add x1, x1, zero
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
lw x1, 0(zero)
add x2, x1, zero

add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops

; no hazard
add x1, x1, zero
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
lw x1, 0(zero)
add x23, x23, x23  ; nops
add x3, x1, zero

add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops

; load-use hazard (rs2)
add x1, x1, zero
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
lw x1, 0(zero)
add x4, zero, x1

add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops

; no hazard
add x1, x1, zero
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
add x23, x23, x23  ; nops
lw x1, 0(zero)
add x23, x23, x23  ; nops
add x5, zero, x1
