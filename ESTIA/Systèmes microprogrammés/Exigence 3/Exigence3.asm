
_main:

;Exigence3.c,44 :: 		void main(){
;Exigence3.c,46 :: 		PORTA = 0;                        // State reset of Input-Output Ports
	CLRF       PORTA+0
;Exigence3.c,47 :: 		PORTB = 0;
	CLRF       PORTB+0
;Exigence3.c,48 :: 		PORTC = 0;
	CLRF       PORTC+0
;Exigence3.c,49 :: 		PORTD = 0;
	CLRF       PORTD+0
;Exigence3.c,50 :: 		TRISD.TRISD1 = 1;
	BSF        TRISD+0, 1
;Exigence3.c,51 :: 		TRISD.TRISD2 = 1;
	BSF        TRISD+0, 2
;Exigence3.c,52 :: 		TRISD.TRISD2 = 1;
	BSF        TRISD+0, 2
;Exigence3.c,53 :: 		ANSEL  = 0;                        // Configure AN pins as digital I/O
	CLRF       ANSEL+0
;Exigence3.c,54 :: 		ANSELH = 0;
	CLRF       ANSELH+0
;Exigence3.c,55 :: 		INTCON = 0b10101000;
	MOVLW      168
	MOVWF      INTCON+0
;Exigence3.c,56 :: 		IOCB.IOCB7 = 1;
	BSF        IOCB+0, 7
;Exigence3.c,57 :: 		C1ON_bit = 0;                      // Disable comparators
	BCF        C1ON_bit+0, BitPos(C1ON_bit+0)
;Exigence3.c,58 :: 		C2ON_bit = 0;
	BCF        C2ON_bit+0, BitPos(C2ON_bit+0)
;Exigence3.c,59 :: 		i=0;
	CLRF       _i+0
	CLRF       _i+1
;Exigence3.c,60 :: 		Lcd_Init();                        // Initialize Lcd
	CALL       _Lcd_Init+0
;Exigence3.c,65 :: 		Lcd_Out(1,6,txt1);
	MOVLW      1
	MOVWF      FARG_Lcd_Out_row+0
	MOVLW      6
	MOVWF      FARG_Lcd_Out_column+0
	MOVLW      _txt1+0
	MOVWF      FARG_Lcd_Out_text+0
	CALL       _Lcd_Out+0
;Exigence3.c,67 :: 		do {
L_main0:
;Exigence3.c,69 :: 		if (PORTD.RD1 == 1) {
	BTFSS      PORTD+0, 1
	GOTO       L_main3
;Exigence3.c,70 :: 		Lcd_Cmd(_LCD_CLEAR);
	MOVLW      1
	MOVWF      FARG_Lcd_Cmd_out_char+0
	CALL       _Lcd_Cmd+0
;Exigence3.c,71 :: 		Lcd_Cmd(_LCD_CURSOR_OFF);          // Cursor of
	MOVLW      12
	MOVWF      FARG_Lcd_Cmd_out_char+0
	CALL       _Lcd_Cmd+0
;Exigence3.c,72 :: 		Lcd_Out(1,6,txt1);
	MOVLW      1
	MOVWF      FARG_Lcd_Out_row+0
	MOVLW      6
	MOVWF      FARG_Lcd_Out_column+0
	MOVLW      _txt1+0
	MOVWF      FARG_Lcd_Out_text+0
	CALL       _Lcd_Out+0
;Exigence3.c,73 :: 		}
L_main3:
;Exigence3.c,75 :: 		if (PORTD.RD2 == 1){
	BTFSS      PORTD+0, 2
	GOTO       L_main4
;Exigence3.c,76 :: 		Lcd_Cmd(_LCD_CLEAR);
	MOVLW      1
	MOVWF      FARG_Lcd_Cmd_out_char+0
	CALL       _Lcd_Cmd+0
;Exigence3.c,77 :: 		Lcd_Cmd(_LCD_CURSOR_OFF);                 // Write text in first row
	MOVLW      12
	MOVWF      FARG_Lcd_Cmd_out_char+0
	CALL       _Lcd_Cmd+0
;Exigence3.c,78 :: 		Lcd_Out(1,6,txt2);
	MOVLW      1
	MOVWF      FARG_Lcd_Out_row+0
	MOVLW      6
	MOVWF      FARG_Lcd_Out_column+0
	MOVLW      _txt2+0
	MOVWF      FARG_Lcd_Out_text+0
	CALL       _Lcd_Out+0
;Exigence3.c,79 :: 		}
L_main4:
;Exigence3.c,81 :: 		if (PORTD.RD3 == 1) {
	BTFSS      PORTD+0, 3
	GOTO       L_main5
;Exigence3.c,82 :: 		Lcd_Cmd(_LCD_CLEAR);
	MOVLW      1
	MOVWF      FARG_Lcd_Cmd_out_char+0
	CALL       _Lcd_Cmd+0
;Exigence3.c,83 :: 		Lcd_Cmd(_LCD_CURSOR_OFF);               // Clear display
	MOVLW      12
	MOVWF      FARG_Lcd_Cmd_out_char+0
	CALL       _Lcd_Cmd+0
;Exigence3.c,84 :: 		Lcd_Out(1,6,txt3);
	MOVLW      1
	MOVWF      FARG_Lcd_Out_row+0
	MOVLW      6
	MOVWF      FARG_Lcd_Out_column+0
	MOVLW      _txt3+0
	MOVWF      FARG_Lcd_Out_text+0
	CALL       _Lcd_Out+0
;Exigence3.c,85 :: 		i=0;
	CLRF       _i+0
	CLRF       _i+1
;Exigence3.c,86 :: 		}
L_main5:
;Exigence3.c,87 :: 		} while (1);
	GOTO       L_main0
;Exigence3.c,88 :: 		}
L_end_main:
	GOTO       $+0
; end of _main
