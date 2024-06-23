#line 1 "C:/Users/antonin.jonot/OneDrive - ESTIA/Bureau/ESTIA/2A-Semestre3/Système microprogrammé/Projet/Projet ROBESTIA/Codes/CodeProjet/CodeProjet.c"
unsigned ReadADC (void);
unsigned retour (void);

short display_lamps = 0;
short mode = 0;
short sens= 0;
int clk;
int time;
unsigned cnt;
unsigned ret =0;
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

unsigned retour(){
 PORTA = 0;
 PORTB = 0;
 PORTC = 0;
 PORTD = 0;
 PORTE = 0;
}

void main () {

 unsigned res = 0;


 OPTION_REG = 0b10000111;

 PORTA = 0;
 PORTB = 0;
 PORTC = 0;
 PORTD = 0;
 PORTE = 0;
 TRISA.TRISA5 = 0;
 TRISA.TRISA2 = 0;
 TRISE.TRISE0 = 0;
 TRISE.TRISE1 = 0;
 TRISE.TRISE2 = 0;
 TRISE.TRISE3 = 0;
 TRISC.TRISC2 = 0;
 TRISC.TRISC3 = 0;
 TRISC.TRISC4 = 0;
 TRISC.TRISC5 = 0;
 TRISD.TRISD2 = 0;
 TRISD.TRISD3 = 0;
 TRISD.TRISD4 = 0;
 TRISD.TRISD5 = 0;

 TRISB.TRISB6 = 1;
 TRISB.TRISB7 = 1;

 TRISD.TRISD0 = 1;
 TRISD.TRISD1 = 1;
 TRISC.TRISC0 = 1;

 TRISA.TRISA3 = 1;

 ANSEL = 0;
 ANSEL.ANS3 = 1;
 ANSELH = 0;
 IOCB.IOCB6 = 1;
 IOCB.IOCB7 = 1;
 INTCON = 0b10101000;

 ADCON0.ADCS1 = 1;
 ADCON0.ADCS0 = 0;

 ADCON1.VCFG1 = 0;
 ADCON1.VCFG0 = 0;

 ADCON0.CHS3 = 0;
 ADCON0.CHS2 = 0;
 ADCON0.CHS1 = 1;
 ADCON0.CHS0 = 1;
 ADCON1.ADFM = 1;

 ADCON0.ADON = 1;

 C1ON_bit = 0;
 C2ON_bit = 0;

 TMR0 = 60;

 Lcd_Init();
 Lcd_Cmd(_LCD_CLEAR);
 Lcd_Cmd(_LCD_CURSOR_OFF);
 Lcd_Out(1,6,txt1);

 do {

 if (PORTC.RC0 == 1) {
 Lcd_Cmd(_LCD_CLEAR);
 Lcd_Cmd(_LCD_CURSOR_OFF);
 Lcd_Out(1,6,txt1);
 }

 if (PORTD.RD0 == 1){
 Lcd_Cmd(_LCD_CLEAR);
 Lcd_Cmd(_LCD_CURSOR_OFF);
 Lcd_Out(1,6,txt2);
 }

 if (PORTD.RD1 == 1) {
 Lcd_Cmd(_LCD_CLEAR);
 Lcd_Cmd(_LCD_CURSOR_OFF);
 Lcd_Out(1,6,txt3);
 }

 res = ReadADC();

 if (res < 210) {
 clk = 40;
 }

 else if ( res < 619){
 clk = 20;
 }

 else {
 clk = 10;
 }

 if (mode == 0 ){


 if (sens == 0) {
 if (cnt>= clk ) {
 PORTD = PORTD << 1;
 cnt=0;
 if (PORTD==0b01000000 || PORTD == 0){
 PORTD = 0b00000100;
 }
 }
 }

 else {
 if (cnt>= clk) {
 PORTD = PORTD >> 1;
 cnt=0;
 if (PORTD == 0b00000010 || PORTD == 0){
 PORTD = 0b00100000;
 }
 }
 }
 }
 else {

 if (sens == 0) {
 ret= retour();

 PORTA.RA2 = display_lamps;
 PORTE.RE1 = display_lamps;
 PORTC.RC2 = display_lamps;
 PORTC.RC4 = display_lamps;
 PORTC.RC5 = display_lamps;
 PORTD.RD3 = display_lamps;
 PORTD.RD4 = display_lamps;
 PORTD.RD5 = display_lamps;


 if (cnt >= clk) {

 display_lamps = ~ display_lamps;

 cnt =0;
 }
 }

 else {
 ret = retour();
 PORTA.RA5 = display_lamps;
 PORTE.RE0 = display_lamps;
 PORTE.RE2 = display_lamps;
 PORTC.RC2 = display_lamps;
 PORTC.RC3 = display_lamps;
 PORTD.RD2 = display_lamps;
 PORTD.RD3 = display_lamps;
 PORTD.RD4 = display_lamps;

 if (cnt >= clk ) {

 display_lamps = ~display_lamps;

 cnt =0;
 }

 }

 }
 } while (1);
}

unsigned ReadADC() {
 unsigned result;

 Delay_us(4);

 ADCON0.GO = 1;
 while(ADCON0.GO);

 result = ADRESH*256 + ADRESL;

 return result;
}

void interrupt() {
 if(INTCON.RBIF == 1) {
 if(PORTB.RB6 == 1) {
 retour();
 mode = ~mode;

 }

 if(PORTB.RB7 == 1) {
 retour();
 sens = ~sens;
 }

 INTCON.RBIF = 0;
 }

 if (TMR0IF_bit) {
 cnt++;
 TMR0IF_bit = 0;
 TMR0 = 60;
 }
}
