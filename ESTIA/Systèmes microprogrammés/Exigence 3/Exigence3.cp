#line 1 "C:/Users/antonin.jonot/OneDrive - ESTIA/Bureau/ESTIA/2A-Semestre3/Système microprogrammé/Projet/Projet ROBESTIA/Codes/Exigence 3/Exigence3.c"
#line 26 "C:/Users/antonin.jonot/OneDrive - ESTIA/Bureau/ESTIA/2A-Semestre3/Système microprogrammé/Projet/Projet ROBESTIA/Codes/Exigence 3/Exigence3.c"
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

char txt1[] = "Ralentir";
char txt2[] = "Accident";
char txt3[] = "Patrouille";
int i;

void main(){

 PORTA = 0;
 PORTB = 0;
 PORTC = 0;
 PORTD = 0;
 TRISD.TRISD1 = 1;
 TRISD.TRISD2 = 1;
 TRISD.TRISD2 = 1;
 ANSEL = 0;
 ANSELH = 0;
 INTCON = 0b10101000;
 IOCB.IOCB7 = 1;
 C1ON_bit = 0;
 C2ON_bit = 0;
 i=0;
 Lcd_Init();




 Lcd_Out(1,6,txt1);

 do {

 if (PORTD.RD1 == 1) {
 Lcd_Cmd(_LCD_CLEAR);
 Lcd_Cmd(_LCD_CURSOR_OFF);
 Lcd_Out(1,6,txt1);
 }

 if (PORTD.RD2 == 1){
 Lcd_Cmd(_LCD_CLEAR);
 Lcd_Cmd(_LCD_CURSOR_OFF);
 Lcd_Out(1,6,txt2);
 }

 if (PORTD.RD3 == 1) {
 Lcd_Cmd(_LCD_CLEAR);
 Lcd_Cmd(_LCD_CURSOR_OFF);
 Lcd_Out(1,6,txt3);
 i=0;
 }
 } while (1);
}
