[BITS 32]

jmp section_labels

section_add:
  add dword eax, 0x44434241
  add dword [ecx + 0xFF], 0x44434241
  add edx, ebx
  add [edx + 0xff], ebx
  add edx, [ebx]
  retn

section_and:
  and dword eax, 0x44434241
  and dword [ecx + 0xFF], 0x44434241
  and edx, ebx
  and [edx + 0xFF], ebx
  and edx, [ebx]
  retn

section_call:
  call section_cmp
  ;call [ebx + 0xc]
  call 0x000001A0   ; to xor section
  retn

section_cmp:
  cmp eax, dword 0x44434241
  cmp dword edx, 0x44434241
  cmp dword [eax+7], 0x44434241
  cmp dword edx, ecx
  cmp dword ebx, [ecx+9]
  retn

section_dec:
  dec dword [eax+0x44434241]
  dec ecx
  dec edx
  dec ebx
  dec esp
  dec ebp
  dec esi
  dec edi
  retn

section_inc:
  inc dword [eax+0x44434241]
  inc ecx
  inc edx
  inc ebx
  inc esp
  inc ebp
  inc esi
  inc edi
  retn

section_mulops:
  imul dword eax
  imul dword [ecx+0x44434241]
  mul dword eax
  mul dword [ecx+0x44434241]
  idiv dword eax
  idiv dword [ecx+0x44434241]
  div dword eax
  div dword [ecx+0x44434241]
  imul eax, [edx + 0x44434241]
  imul eax, [edx + 0x44434241], 0x44434241
  retn

section_jmp:
  jmp short section_jmp_internal1
section_jmp_internal1:
  ;jmp 0x44434241
  jmp 0xB1
  ;jmp eax
  jz section_jmp_internal2
section_jmp_internal2:
  ;jz 0x44434241
  jz 0xB3
section_jmp_internal3:
  jnz section_jmp
section_jmp_internal4:
  ;jnz 0x44434241
  jz 0xBB
section_jmp_internal5:
  jmp section_jmp_internal6
section_jmp_internal6:
  nop
  retn

unreachable_data_section1:
  db 0x09, 0x24, 0x2d, 0x2d, 0x2e, 0x41

unreachable_data_section2:
  db 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xE7, 0xE8, 0xE9

section_lea:
  lea eax, [0x44434241]
  lea eax, [ecx + 0x42]
  lea eax, [edi + 0x44434241]
  retn

section_mov:
  mov [eax], ecx
  mov ecx, [edx]
  mov eax, dword 0x44434241
  mov ebx, dword 0x44434241
  mov ecx, dword 0x44434241
  mov [eax], dword 0x44434241
  retn

section_movsd:
  movsd
  retn

section_neg:
  neg eax
  neg ecx
  retn

section_nop:
  nop
  nop
  nop eax  ; new
  nop ecx  ; new
  nop dword [ecx + 0xFF]  ; new
  nop dword [0x44434241]  ; new
  nop dword [ecx]  ; new
  retn

section_not:
  not eax
  not ecx
  not edx
  retn

section_or:
  or dword eax, 0x44434241
  or dword [ecx + 0xFF], 0x44434241
  or edx, ebx
  or [edx + 0xff], ebx
  or edx, [ebx]
  retn

section_pop:
  pop dword [eax]
  pop dword [0x44434241]
  pop ecx
  retn

section_push:
  push dword [eax]
  push dword [ecx]
  push ecx
  push 0x44434241
  retn

section_cmpsd:
  cmpsd
  retn

section_repne:
  repne CMPSD

  ; The below instructions don't seem valid:
  ;    "REPNE/REPNZ prefix is encoded using F2H. Repeat-Not-Zero prefix applies only to string and
  ;    input/output instructions. (F2H is also used as a mandatory prefix for some instructions.)"
  ; - Vol 2A-1
  ; Though... there are a few that look a bit like it: ADDSD, ADDSUBPS, BNDCU, BNDCN, CMPSD ("Compare Scalar Double-Precision
  ; Floating-Point Values"... not the string one), CRC32, DIVSD, MOVSD (again, for double precision, not strings)...
  ;repne movsd
  ;repne inc eax
  retn

section_ret_f:
  retn
  retn 0x8
  retf
  retf 0x8

section_sal_sar:
  sal eax, 1
  shl eax, 1
  sar eax, 1
  shr eax, 1
  sal ecx, 1 ; new
  shl edx, 1 ; new
  sar ebx, 1 ; new
  shr edi, 1 ; new
  retn

section_sbb:
  sbb eax, 0x44434241
  sbb ecx, 0x44434241
  sbb [ecx], eax
  sbb ecx, [eax]
  retn

section_sub:
  sub eax, 0x44434241
  sub ecx, 0x44434241
  sub [ecx], eax
  sub ecx, [eax]
  retn

section_test:
  test eax, 0x44434241
  test dword [ecx], 0x44434241
  test ecx, edx
  retn

section_xor:
  xor eax, eax
  xor ecx, ebx
  xor eax, 0x44434241
  xor dword [eax], 0x44434241
  retn

section_tricky:
  ADD EDI, ESI
  ADD EDI, [ESI]
  ADD EDI, [ESI + 0x10]
  ADD EDI, dword [ESI + 0x10000010]
  ADD EDI, [0x10000000]
  ADD [EBP + 0x00], EDI
  ADD EDI, 0x11223344
  MOV ESI, EBX
  MOV [ESI], EBX
  MOV [ESI*8 + EDI], EBX
  MOV [ESI*4 + EDI + 0xAABBCCDD], dword 0x11223344
  MOV [ESI*4 + 0x00000000], dword  0x11223344 ; translates to "MOV [ESI*4], dword  0x11223344"
  MOV [ESI*4], dword 0x11223344
  MOV [ESP], ECX    ; multiple encodings !... \x89\x0C\xE4, \x89\x0C\x24, \x89\x0C\x64, \x89\x0C\xA4
  retn

section_labels:
  call section_add
  call section_and
  call section_call
  call section_cmp
  call section_dec
  call section_inc
  call section_mulops
  call section_jmp
  call section_lea
  call section_mov
  call section_movsd
  call section_neg
  call section_nop
  call section_not
  call section_or
  call section_pop
  call section_push
  call section_cmpsd
  call section_repne
  call section_ret_f
  call section_sal_sar
  call section_sbb
  call section_sub
  call section_test
  call section_xor
  call section_tricky
