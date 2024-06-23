unsigned ReadADC (void);
unsigned retour (void);

short display_lamps = 0;             // 0 = lamp_OFF / 1 = lamp_ON
short mode = 0;                      // 0= replie / 1= depli?
short sens= 0;                       // 0= sens 1 / 1= sens 2
int clk;                           // clk valeur en Hz demandé
int time;                          // temps converti pour le timer                              // variable de comptage
unsigned cnt;
unsigned ret =0;                  // varible de retour à 0

unsigned retour(){                 // retour à 0
     PORTA = 0;
     PORTB = 0;
     PORTC = 0;
     PORTD = 0;
}

void main () {

  unsigned res = 0;


  OPTION_REG = 0b10000111;         // Mise du timer 256 bits

  PORTA = 0;                        // State reset of Input-Output Ports
  PORTB = 0;
  PORTC = 0;
  PORTD = 0;
  TRISA.TRISA5 = 0;                 // Configuration in output of RA1, RA2, RA3
  TRISA.TRISA2 = 0;                 // RB2, RB3, RC1, RC3 and RD0 pins
  TRISB.TRISB2 = 0;                 // --> to control lamps L0 to L7
  TRISB.TRISB3 = 0;
  TRISB.TRISB4 = 0;
  TRISB.TRISB5 = 0;
  TRISC.TRISC2 = 0;
  TRISC.TRISC3 = 0;
  TRISC.TRISC4 = 0;
  TRISC.TRISC5 = 0;
  TRISD.TRISD2 = 0;
  TRISD.TRISD3 = 0;
  TRISD.TRISD4 = 0;
  TRISD.TRISD5 = 0;

  TRISB.TRISB0 = 1;
  TRISB.TRISB1 = 1;

  TRISA.TRISA3 = 1;

  ANSEL  = 0;                       // Input-Output are all digital
  ANSEL.ANS3 = 1;
  ANSELH = 0;
  IOCB.IOCB0 = 1;
  IOCB.IOCB1 = 1;
  INTCON = 0b10101000;

  ADCON0.ADCS1 = 1;                // ? commenter
  ADCON0.ADCS0 = 0;

  ADCON1.VCFG1 = 0;                // ? commenter
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


    do {
                                                             // mise en place de l'ADC de la carte
      res = ReadADC();

      if (res < 210) {                                        // définition des valeurs potentiomètre
          clk = 40;
      }

      else if (res < 619){
          clk = 20;
      }

      else {
          clk = 10;
      }

      if (mode == 0 ){


         if (sens ==0){
         
            ret= retour();

            PORTA.RA2 = ~ display_lamps;          // RA1, RA2, RA3, RB2, RB3, RC1, RC3 and RD0
            PORTB.RB3 = ~ display_lamps;          // are set ON if display_lamps = 1
            PORTB.RB5 = ~ display_lamps;          // are set OFF if display_lamps = 0
            PORTC.RC4 = ~ display_lamps;
            PORTC.RC5 = ~ display_lamps;
            PORTD.RD3 = ~ display_lamps;
            PORTD.RD4 = ~ display_lamps;
            PORTD.RD5 = ~ display_lamps;


            if (cnt >= clk) {                                 // utilisation du timer

               display_lamps = ~display_lamps;

               cnt =0;
            }
         }

        else {
          ret = retour();
          PORTA.RA5 = display_lamps;          // RA1, RA2, RA3, RB2, RB3, RC1, RC3 and RD0
          PORTB.RB2 = display_lamps;          // are set ON if display_lamps = 1
          PORTB.RB4 = display_lamps;          // are set OFF if display_lamps = 0
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
      else {

        if (sens == 0) {
          PORTD = 0b00000100;
          if (cnt>= clk ) {
            PORTD = PORTD << 1;
            cnt=0;
          }
          if (PORTD==0b00100000 || PORTD ==0){
            PORTD = 0b00000100;
          }
        }
          
        else {                                                     // idem mais inverser
          PORTD = 0b00100000;
          if (cnt>= clk) {
            PORTD = PORTD >> 1;
            cnt=0;
          }
          if (PORTD==0b00000100 || PORTD==0){
            PORTD = 0b00100000;
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
        if(PORTB.RB0 == 1) {
            retour();
            mode = ~mode;

        }

        if(PORTB.RB1 == 1) {
            retour();
            sens = ~sens;
        }

        INTCON.RBIF = 0;
    }

    if (TMR0IF_bit) {
      cnt++;
      TMR0IF_bit = 0;
      TMR0   = 60;
    }
}