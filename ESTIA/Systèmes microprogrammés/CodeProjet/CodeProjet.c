unsigned ReadADC (void);
unsigned retour (void);

short display_lamps = 0;             // 0 = lamp_OFF / 1 = lamp_ON
short BP_MOD  = 0;                      // 0= replie / 1= depli?
short BP_sens = 0;                       // 0= sens 1 / 1= sens 2
int clk;                           // clk valeur en Hz demandé
unsigned cnt;                    // variable de comptage
unsigned ret =0;                  // varible de retour à 0

// Définition port LCD
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
// Définition mot à afficher
char txt1[] = "Ralentir";
char txt2[] = "Accident";
char txt3[] = "Patrouille";

unsigned retour(){                 // retour à 0
     PORTA = 0;
     PORTB = 0;
     PORTC = 0;
     PORTD = 0;
     PORTE = 0;
}

void main () {

  unsigned PT_VIT  = 0;


  OPTION_REG = 0b10000111;         // Mise du timer 256 bits

  PORTA = 0;                        // State reset of Input-Output Ports
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

  ANSEL  = 0;                       // Input-Output are all digital
  ANSEL.ANS3 = 1;
  ANSELH = 0;
  IOCB.IOCB6 = 1;
  IOCB.IOCB7 = 1;
  INTCON = 0b10101000;

  ADCON0.ADCS1 = 1;
  ADCON0.ADCS0 = 0;

  ADCON1.VCFG1 = 0;
  ADCON1.VCFG0 = 0;

  ADCON0.CHS3 = 0;                 // Le potentionmètre est branché sur AN3
  ADCON0.CHS2 = 0;
  ADCON0.CHS1 = 1;
  ADCON0.CHS0 = 1;
  ADCON1.ADFM = 1;

  ADCON0.ADON = 1;

  C1ON_bit = 0;                    // Disable all comparators
  C2ON_bit = 0;

  TMR0  = 60;                    // Valeur de TMRO pour obtenir un temps d'incrémentation de 0.025s

  Lcd_Init();
  Lcd_Cmd(_LCD_CLEAR);
  Lcd_Cmd(_LCD_CURSOR_OFF);
  Lcd_Out(1,6,txt1);

  do {
    
      if (PORTC.RC0 == 1) {
         Lcd_Cmd(_LCD_CLEAR);
         Lcd_Cmd(_LCD_CURSOR_OFF);          // Cursor of
         Lcd_Out(1,6,txt1);
      }

      if (PORTD.RD0 == 1){
        Lcd_Cmd(_LCD_CLEAR);
        Lcd_Cmd(_LCD_CURSOR_OFF);                 // Write text in first row
        Lcd_Out(1,6,txt2);
      }

      if (PORTD.RD1 == 1) {
         Lcd_Cmd(_LCD_CLEAR);                    // Clear display
         Lcd_Cmd(_LCD_CURSOR_OFF);
         Lcd_Out(1,6,txt3);
      }
                                                             // mise en place de l'ADC de la carte
      PT_VIT = ReadADC();

      if (PT_VIT < 210) {                                        // définition des valeurs potentiomètre
          clk = 40;
      }

      else if ( PT_VIT < 619){
          clk = 20;
      }

      else {
          clk = 10;
      }

    if (BP_MOD == 0 ){


      if (BP_sens  == 0) {
          if (cnt>= clk ) {
            PORTD = PORTD << 1;
            cnt=0;
            if (PORTD==0b01000000 || PORTD == 0){
              PORTD = 0b00000100;
            }
          }
        }

        else {                                                     // idem mais inverser
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

      if (BP_sens  == 0) {
        ret= retour();

        PORTA.RA2 = display_lamps;
        PORTE.RE1 = display_lamps;
        PORTC.RC2 = display_lamps;
        PORTC.RC4 = display_lamps;
        PORTC.RC5 = display_lamps;
        PORTD.RD3 = display_lamps;
        PORTD.RD4 = display_lamps;
        PORTD.RD5 = display_lamps;


        if (cnt >= clk) {                                 // utilisation du timer

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
            BP_MOD = ~BP_MOD;

        }

        if(PORTB.RB7 == 1) {
            retour();
            BP_sens  = ~BP_sens;
        }

        INTCON.RBIF = 0;
    }

    if (TMR0IF_bit) {
      cnt++;
      TMR0IF_bit = 0;
      TMR0   = 60;
    }
}