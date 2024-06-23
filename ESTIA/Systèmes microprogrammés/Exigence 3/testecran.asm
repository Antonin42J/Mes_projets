
_Move_Delay:

;testecran.c,44 :: 		void Move_Delay() {                  // Function used for text moving
;testecran.c,45 :: 		Delay_ms(500);                     // You can change the moving speed here
	MOVLW      6
	MOVWF      R11+0
	MOVLW      19
	MOVWF      R12+0
	MOVLW      173
	MOVWF      R13+0
L_Move_Delay0:
	DECFSZ     R13+0, 1
	GOTO       L_Move_Delay0
	DECFSZ     R12+0, 1
	GOTO       L_Move_Delay0
	DECFSZ     R11+0, 1
	GOTO       L_Move_Delay0
	NOP
	NOP
;testecran.c,46 :: 		}
L_end_Move_Delay:
	RETURN
; end of _Move_Delay

_main:

;testecran.c,47 :: 		void main(){
;testecran.c,48 :: 		ANSEL  = 0;                        // Configure AN pins as digital I/O
	CLRF       ANSEL+0
;testecran.c,49 :: 		ANSELH = 0;
	CLRF       ANSELH+0
;testecran.c,50 :: 		C1ON_bit = 0;                      // Disable comparators
	BCF        C1ON_bit+0, BitPos(C1ON_bit+0)
;testecran.c,51 :: 		C2ON_bit = 0;
	BCF        C2ON_bit+0, BitPos(C2ON_bit+0)
;testecran.c,52 :: 		Lcd_Init();                        // Initialize Lcd
	CALL       _Lcd_Init+0
;testecran.c,53 :: 		Lcd_Cmd(_LCD_CLEAR);               // Clear display
	MOVLW      1
	MOVWF      FARG_Lcd_Cmd_out_char+0
	CALL       _Lcd_Cmd+0
;testecran.c,54 :: 		Lcd_Cmd(_LCD_CURSOR_OFF);          // Cursor off
	MOVLW      12
	MOVWF      FARG_Lcd_Cmd_out_char+0
	CALL       _Lcd_Cmd+0
;testecran.c,55 :: 		Lcd_Out(1,6,txt3);                 // Write text in first row
	MOVLW      1
	MOVWF      FARG_Lcd_Out_row+0
	MOVLW      6
	MOVWF      FARG_Lcd_Out_column+0
	MOVLW      _txt3+0
	MOVWF      FARG_Lcd_Out_text+0
	CALL       _Lcd_Out+0
;testecran.c,56 :: 		Lcd_Out(2,6,txt4);                 // Write text in second row
	MOVLW      2
	MOVWF      FARG_Lcd_Out_row+0
	MOVLW      6
	MOVWF      FARG_Lcd_Out_column+0
	MOVLW      _txt4+0
	MOVWF      FARG_Lcd_Out_text+0
	CALL       _Lcd_Out+0
;testecran.c,57 :: 		Delay_ms(2000);
	MOVLW      21
	MOVWF      R11+0
	MOVLW      75
	MOVWF      R12+0
	MOVLW      190
	MOVWF      R13+0
L_main1:
	DECFSZ     R13+0, 1
	GOTO       L_main1
	DECFSZ     R12+0, 1
	GOTO       L_main1
	DECFSZ     R11+0, 1
	GOTO       L_main1
	NOP
;testecran.c,58 :: 		Lcd_Cmd(_LCD_CLEAR);               // Clear display
	MOVLW      1
	MOVWF      FARG_Lcd_Cmd_out_char+0
	CALL       _Lcd_Cmd+0
;testecran.c,59 :: 		Lcd_Out(1,1,txt1);                 // Write text in first row
	MOVLW      1
	MOVWF      FARG_Lcd_Out_row+0
	MOVLW      1
	MOVWF      FARG_Lcd_Out_column+0
	MOVLW      _txt1+0
	MOVWF      FARG_Lcd_Out_text+0
	CALL       _Lcd_Out+0
;testecran.c,60 :: 		Lcd_Out(2,5,txt2);                 // Write text in second row
	MOVLW      2
	MOVWF      FARG_Lcd_Out_row+0
	MOVLW      5
	MOVWF      FARG_Lcd_Out_column+0
	MOVLW      _txt2+0
	MOVWF      FARG_Lcd_Out_text+0
	CALL       _Lcd_Out+0
;testecran.c,61 :: 		Delay_ms(2000);
	MOVLW      21
	MOVWF      R11+0
	MOVLW      75
	MOVWF      R12+0
	MOVLW      190
	MOVWF      R13+0
L_main2:
	DECFSZ     R13+0, 1
	GOTO       L_main2
	DECFSZ     R12+0, 1
	GOTO       L_main2
	DECFSZ     R11+0, 1
	GOTO       L_main2
	NOP
;testecran.c,63 :: 		for(i=0; i<4; i++) {               // Move text to the right 4 times
	CLRF       _i+0
L_main3:
	MOVLW      4
	SUBWF      _i+0, 0
	BTFSC      STATUS+0, 0
	GOTO       L_main4
;testecran.c,64 :: 		Lcd_Cmd(_LCD_SHIFT_RIGHT);
	MOVLW      28
	MOVWF      FARG_Lcd_Cmd_out_char+0
	CALL       _Lcd_Cmd+0
;testecran.c,65 :: 		Move_Delay();
	CALL       _Move_Delay+0
;testecran.c,63 :: 		for(i=0; i<4; i++) {               // Move text to the right 4 times
	INCF       _i+0, 1
;testecran.c,66 :: 		}
	GOTO       L_main3
L_main4:
;testecran.c,67 :: 		while(1) {                         // Endless loop
L_main6:
;testecran.c,68 :: 		for(i=0; i<8; i++) {             // Move text to the left 7 times
	CLRF       _i+0
L_main8:
	MOVLW      8
	SUBWF      _i+0, 0
	BTFSC      STATUS+0, 0
	GOTO       L_main9
;testecran.c,69 :: 		Lcd_Cmd(_LCD_SHIFT_LEFT);
	MOVLW      24
	MOVWF      FARG_Lcd_Cmd_out_char+0
	CALL       _Lcd_Cmd+0
;testecran.c,70 :: 		Move_Delay();
	CALL       _Move_Delay+0
;testecran.c,68 :: 		for(i=0; i<8; i++) {             // Move text to the left 7 times
	INCF       _i+0, 1
;testecran.c,71 :: 		}
	GOTO       L_main8
L_main9:
;testecran.c,72 :: 		for(i=0; i<8; i++) {             // Move text to the right 7 times
	CLRF       _i+0
L_main11:
	MOVLW      8
	SUBWF      _i+0, 0
	BTFSC      STATUS+0, 0
	GOTO       L_main12
;testecran.c,73 :: 		Lcd_Cmd(_LCD_SHIFT_RIGHT);
	MOVLW      28
	MOVWF      FARG_Lcd_Cmd_out_char+0
	CALL       _Lcd_Cmd+0
;testecran.c,74 :: 		Move_Delay();
	CALL       _Move_Delay+0
;testecran.c,72 :: 		for(i=0; i<8; i++) {             // Move text to the right 7 times
	INCF       _i+0, 1
;testecran.c,75 :: 		}
	GOTO       L_main11
L_main12:
;testecran.c,76 :: 		}
	GOTO       L_main6
;testecran.c,77 :: 		}
L_end_main:
	GOTO       $+0
; end of _main
