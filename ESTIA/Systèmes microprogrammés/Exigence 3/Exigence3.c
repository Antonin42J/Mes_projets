/*
 * Project name:
     Lcd_Test (Demonstration of the LCD library routines)
 * Copyright:
     (c) Mikroelektronika, 2011.
 * Revision History:
     20110929:
       - initial release (FJ);
 * Description:
     This code demonstrates how to use LCD 4-bit library. LCD is first
     initialized, then some text is written, then the text is moved.
 * Test configuration:
     MCU:             PIC18F45K22
                      http://ww1.microchip.com/downloads/en/DeviceDoc/40001412G.pdf
     Dev.Board:       EasyPIC7 - ac:LCD
                      http://www.mikroe.com/easypic/
     Oscillator:      HS-PLL 32.0000 MHz, 8.0000 MHz Crystal
     Ext. Modules:    Character Lcd 2x16
                      https://www.mikroe.com/lcd-2x16-blue
     SW:              mikroC PRO for PIC
                      http://www.mikroe.com/mikroc/pic/
 * NOTES:
     - Turn on Lcd backlight switch SW4.6. (board specific)
*/
// Lcd module connections
sbit LCD_RS at RB4_bit;
sbit LCD_EN at RB5_bit;
sbit LCD_D4 at RB0_bit;
sbit LCD_D5 at RB1_bit;
sbit LCD_D6 at RB2_bit;
sbit LCD_D7 at RB3_bit;
sbit LCD_RS_Direction at TRISB4_bit;
sbit LCD_EN_Direction at TRISB5_bit;
sbit LCD_D4_Direction at TRISB0_bit;
sbit LCD_D5_Direction at TRISB1_bit;
sbit LCD_D6_Direction at TRISB2_bit;
sbit LCD_D7_Direction at TRISB3_bit;
// End Lcd module connections
char txt1[] = "Ralentir";
char txt2[] = "Accident";
char txt3[] = "Patrouille";


void main(){

  PORTA = 0;                        // State reset of Input-Output Ports
  PORTB = 0;
  PORTC = 0;
  PORTD = 0;
  TRISD.TRISD1 = 1;
  TRISD.TRISD2 = 1;
  TRISD.TRISD2 = 1;
  ANSEL  = 0;                        // Configure AN pins as digital I/O
  ANSELH = 0;
  Lcd_Init();                        // Initialize Lcd


  // Moving text
  
  Lcd_Out(1,6,txt1);

  do {

    if (PORTD.RD1 == 1) {
       Lcd_Cmd(_LCD_CLEAR);
       Lcd_Cmd(_LCD_CURSOR_OFF);          // Cursor of
       Lcd_Out(1,6,txt1);
    }

    if (PORTD.RD2 == 1){
      Lcd_Cmd(_LCD_CLEAR);
      Lcd_Cmd(_LCD_CURSOR_OFF);                 // Write text in first row
      Lcd_Out(1,6,txt2);
    }

    if (PORTD.RD3 == 1) {
       Lcd_Cmd(_LCD_CLEAR);
       Lcd_Cmd(_LCD_CURSOR_OFF);               // Clear display
       Lcd_Out(1,6,txt3);
       i=0;
    }
  } while (1);
}