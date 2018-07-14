import spidev
import time

from libsoc import gpio
from dweet import Dweet
from gpio_96boards import GPIO



GPIO_CS = GPIO.gpio_id('GPIO_CS')
BUTTON = GPIO.gpio_id('GPIO_A')
RELE = GPIO.gpio_id('GPIO_C')
LED = GPIO.gpio_id('GPIO_E')


pins = ((GPIO_CS, 'out'), (RELE, 'out'), (LED, 'out'), (BUTTON, 'in'),)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10000
spi.mode = 0b00
spi.bits_per_word = 8



dweet = Dweet()

def readTemp(gpio):

	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	time.sleep(0.0002)
	gpio.digital_write(GPIO_CS, GPIO.LOW)
	r = spi.xfer2([0x01, 0xA0, 0x00])
	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	adcout = (r[1] << 8) & 0b1100000000
	adcout = adcout | (r[2] & 0xff)		
	adc_temp = (((adcout * 5.0)/1023)-0.5)*100
	return adc_temp


def readLumi(gpio):
		
	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	time.sleep(0.002)
	gpio.digital_write(GPIO_CS, GPIO.LOW)
	r = spi.xfer2([0x01, 0x80, 0x00])
	gpio.digital_write(GPIO_CS, GPIO.HIGH)

	adcout = (r[1] << 8) & 0b1100000000
	adcout = adcout | (r[2] & 0xff)
	if (adcout < 200):
	    gpio.digital_write(LED, GPIO.HIGH)	
            print("Luz Ambiente Acesa")
	else:
	     gpio.digital_write(LED, GPIO.LOW)
	     print("Luz Ambiente Apagada")
	return adcout

def liga():

    gpio.digital_write(RELE, GPIO.HIGH)
    print "Sistema Ligado"
    
 
def desliga():

    gpio.digital_write(RELE, GPIO.LOW)
    print "Sistema Desligado" 
    	


def envia_dweet():
	dweet.dweet_by_name(name="neves_smart", data={"Temperatura":temp, "Luminosidade":lumi, "led":lamp, "rele": sistem})
	resposta = dweet.latest_dweet(name="neves_smart")



if __name__=='__main__':

	with GPIO(pins) as gpio:
	        status = 0
		while True:
			temp = readTemp(gpio)
			lumi = readLumi(gpio)		
			lamp = gpio.digital_read(LED)
			sistem = gpio.digital_read(RELE)
			button_value = gpio.digital_read(BUTTON)
                        #print "Botao:%d" %button_value
                        #print "Status:%d" %status
                        time.sleep(0.25)
                        if button_value == 1:
                        
                           if status == 0:
                              status = 1
                              liga()
                              
                           else:
                                status = 0
                                desliga()
                        		

			print "Temp: %2.1f\nlumi: %d\nLed: %d\nrele: %d\n" %(temp, lumi, lamp, sistem)
			envia_dweet()
			time.sleep(10)
			
			




	



