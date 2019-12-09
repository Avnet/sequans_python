import serial
import argparse, os
import time
import sys

#====================================================================================================================
#	Configurable parameters
#====================================================================================================================
uart0_at = "/dev/ttyUSB0"				# section for AT0 channel configuration
uart0_at_speed = 115200
channel0_at = serial.Serial(uart0_at, uart0_at_speed, timeout=0.5, parity=serial.PARITY_NONE, rtscts=True)  # open serial port

topic = "sqn/test"
clientID = "client-test1"

stream_count = 9
use_tls = False
dbg_msgs = False
r = '\r'
ssl_ca_pem_certificat = '''
-----BEGIN CERTIFICATE-----
MIIEkjCCA3qgAwIBAgIQCgFBQgAAAVOFc2oLheynCDANBgkqhkiG9w0BAQsFADA/
MSQwIgYDVQQKExtEaWdpdGFsIFNpZ25hdHVyZSBUcnVzdCBDby4xFzAVBgNVBAMT
DkRTVCBSb290IENBIFgzMB4XDTE2MDMxNzE2NDA0NloXDTIxMDMxNzE2NDA0Nlow
SjELMAkGA1UEBhMCVVMxFjAUBgNVBAoTDUxldCdzIEVuY3J5cHQxIzAhBgNVBAMT
GkxldCdzIEVuY3J5cHQgQXV0aG9yaXR5IFgzMIIBIjANBgkqhkiG9w0BAQEFAAOC
AQ8AMIIBCgKCAQEAnNMM8FrlLke3cl03g7NoYzDq1zUmGSXhvb418XCSL7e4S0EF
q6meNQhY7LEqxGiHC6PjdeTm86dicbp5gWAf15Gan/PQeGdxyGkOlZHP/uaZ6WA8
SMx+yk13EiSdRxta67nsHjcAHJyse6cF6s5K671B5TaYucv9bTyWaN8jKkKQDIZ0
Z8h/pZq4UmEUEz9l6YKHy9v6Dlb2honzhT+Xhq+w3Brvaw2VFn3EK6BlspkENnWA
a6xK8xuQSXgvopZPKiAlKQTGdMDQMc2PMTiVFrqoM7hD8bEfwzB/onkxEz0tNvjj
/PIzark5McWvxI0NHWQWM6r6hCm21AvA2H3DkwIDAQABo4IBfTCCAXkwEgYDVR0T
AQH/BAgwBgEB/wIBADAOBgNVHQ8BAf8EBAMCAYYwfwYIKwYBBQUHAQEEczBxMDIG
CCsGAQUFBzABhiZodHRwOi8vaXNyZy50cnVzdGlkLm9jc3AuaWRlbnRydXN0LmNv
bTA7BggrBgEFBQcwAoYvaHR0cDovL2FwcHMuaWRlbnRydXN0LmNvbS9yb290cy9k
c3Ryb290Y2F4My5wN2MwHwYDVR0jBBgwFoAUxKexpHsscfrb4UuQdf/EFWCFiRAw
VAYDVR0gBE0wSzAIBgZngQwBAgEwPwYLKwYBBAGC3xMBAQEwMDAuBggrBgEFBQcC
ARYiaHR0cDovL2Nwcy5yb290LXgxLmxldHNlbmNyeXB0Lm9yZzA8BgNVHR8ENTAz
MDGgL6AthitodHRwOi8vY3JsLmlkZW50cnVzdC5jb20vRFNUUk9PVENBWDNDUkwu
Y3JsMB0GA1UdDgQWBBSoSmpjBH3duubRObemRWXv86jsoTANBgkqhkiG9w0BAQsF
AAOCAQEA3TPXEfNjWDjdGBX7CVW+dla5cEilaUcne8IkCJLxWh9KEik3JHRRHGJo
uM2VcGfl96S8TihRzZvoroed6ti6WqEBmtzw3Wodatg+VyOeph4EYpr/1wXKtx8/
wApIvJSwtmVi4MFU5aMqrSDE6ea73Mj2tcMyo5jMd6jmeWUHK8so/joWUoHOUgwu
X4Po1QYz+3dszkDqMp4fklxBwXRsW10KXzPMTZ+sOPAveyxindmjkW8lGy+QsRlG
PfZ+G6Z6h7mjem0Y+iWlkYcV4PIWL1iwBi8saCbGS5jN2p8M+X+Q7UNKEkROb3N6
KOqkqm57TH2H3eDJAkSnh6/DNFu0Qg==
-----END CERTIFICATE-----
'''

#====================================================================================================================

parser = argparse.ArgumentParser(
	description='Script demonstrating HTTP/HTTPS/MQTT usage', 
	epilog='!! Verify UART (uart0_at) and speed (uart0_at_speed) settings in script !!\n\n'
	)
parser.add_argument('-d', '--debug', action='store_true',
	help='enable output of debug messages',
	default=False
        )
parser.add_argument('-s', '--server',
        help='server ip addr or domain name',
        default='broker.hivemq.com'
        )
parser.add_argument('-p', '--port',
        help='server port',
        default='1883'
        )

#====================================================================================================================

def do_debug(doit, msg):
	if doit:
		print(msg)

def pause(msg):
	agn=raw_input(msg) 
	if agn == 'x' or agn == 'X':
		return False
	else:
		return True

def reading_raw_resp():
	maxtimeout = 20
	for timeout in range(0, maxtimeout):
		tmp_line = channel0_at.readlines()
		for line in tmp_line:
                	if line.rstrip() == 'OK':
				return
			else:
				if line[0:3] == '<<<':
					line = line.replace('<<<','')
				print(line.rstrip())
	return 

def reading_resp():
	time.sleep(2)
	tmp_line = channel0_at.readlines()
	for line in tmp_line:
		print(line)
	#return tmp_line
	return 

def waiting_response(resp):
	found = 0
	maxtimeout = 20
	for timeout in range(0, maxtimeout):
		tmp_line = channel0_at.readlines()
		for line in tmp_line:
			line = line.replace('\r', '').replace('\n', '')
			if line == resp:
				found = 1
				return True
		time.sleep(1)
	if found == 0:
		print('... not found. Exit.')
		sys.exit()
		
def waiting_response_noexit(resp):
	found = 0
	maxtimeout = 5
	for timeout in range(0, maxtimeout):
		tmp_line = channel0_at.readlines()
		for line in tmp_line:
			line = line.replace('\r', '').replace('\n', '')
			if line == resp:
				found = 1
				return True
		time.sleep(1)
	return False

def get_line_include(word):
	maxtimeout = 20
	for timeout in range(0, maxtimeout):
		tmp_line = channel0_at.readlines()
		for line in tmp_line:
			if line.find(word) != -1:
				return line
		time.sleep(1)
	return ''

def checking_at():
	channel0_at.readlines()
	channel0_at.write('AT'+r)
	waiting_response('OK')

def load_cert():
	cert_size = len(ssl_ca_pem_certificat)
	print("...loading certificate ({} bytes)".format(cert_size))
        cmd = "at+sqnsnvw=\"certificate\",0," + str(cert_size) + r
	channel0_at.write(cmd)
	waiting_response('> ')
	channel0_at.write(ssl_ca_pem_certificat)
	waiting_response('OK')
        cmd = "at+sqnspcfg=1,2,\"\",7,1" + r
	channel0_at.write(cmd)
	waiting_response('OK')
        print('...Certificate Loaded')

def remove_cert():
	cmd = "AT+SQNSNVW=\"certificate\",0,0" + r
	channel0_at.write(cmd)
	waiting_response('OK')
	print('\n...certificate removed')

def stream_test():
        print('=================================')
        print('Perform a STREAM test, streaming {} chunks from httpbin.org'.format(stream_count))
	if use_tls:
          print(r'using TLS.')
          load_cert()
        cmd = "at+sqnhttpcfg=1,\"httpbin.org\"" + r
	channel0_at.write(cmd)
	waiting_response('OK')
        cmd = "AT+SQNHTTPQRY=1,0,\"/stream/" +str(stream_count)+"\"" + r
	channel0_at.write(cmd)
	waiting_response('OK')
        resp = get_line_include('+SQNHTTPRING:')
	print('->received a response: '+resp)
	cmd = "AT+SQNHTTPRCV=1" + r
	print('cmd sent: '+cmd)
	channel0_at.write(cmd)
        print('Response:')
        reading_raw_resp()
	if use_tls:
          remove_cert()
        print('=================================')
        pause("Press <ENTER> to continue. ")

        
def put_test():
        print('=================================')
        print('Perform PUT test with httpbin.org')
	if use_tls:
          print(r'using TLS.')
          load_cert()
        cmd = "at+sqnhttpcfg=1,\"httpbin.org\"" + r
	channel0_at.write(cmd)
	waiting_response('OK')
	cmd = "AT+SQNHTTPSND=1,1,\"/put\",8" + r
	channel0_at.write(cmd)
	waiting_response('> ')
        channel0_at.write("PUT TEST")
	waiting_response('OK')
        get_line_include('+SQNHTTPRING: ')
        cmd = "AT+SQNHTTPRCV=1" + r
	channel0_at.write(cmd)
        print('httpbin.org Response is:')
        reading_raw_resp()
	if use_tls:
          remove_cert()
        print('=================================')
        pause("Press <ENTER> to continue. ")

def post_test():
        print('=================================')
        print('Perform POST test with httpbin.org')
	if use_tls:
          print(r'using TLS.')
          load_cert()
        cmd = "at+sqnhttpcfg=1,\"httpbin.org\"" + r
	channel0_at.write(cmd)
	waiting_response('OK')
        cmd = "AT+SQNHTTPSND=1,0,\"/post\",9" + r
	channel0_at.write(cmd)
	waiting_response('> ')
        channel0_at.write("POST TEST")
	waiting_response('OK')
        get_line_include('+SQNHTTPRING: ')
        cmd = "AT+SQNHTTPRCV=1" + r
	channel0_at.write(cmd)
        print('httpbin.org Response is:')
        reading_raw_resp()
	if use_tls:
          remove_cert()
        print('=================================')
        pause("Press <ENTER> to continue. ")

def delete_test():
        print('=================================')
        print('Perform DELETE test with httpbin.org')
	if use_tls:
          print(r'using TLS.')
          load_cert()
        cmd = "at+sqnhttpcfg=1,\"httpbin.org\"" + r
	channel0_at.write(cmd)
	waiting_response('OK')
	cmd = "AT+SQNHTTPQRY=1,2,\"/delete\",\"accept: application/json\"" + r
	channel0_at.write(cmd)
	waiting_response('OK')
        get_line_include('+SQNHTTPRING: ')
        cmd = "AT+SQNHTTPRCV=1" + r
	channel0_at.write(cmd)
        print('httpbin.org Response is:')
        reading_raw_resp()
	if use_tls:
          remove_cert()
        print('=================================')
        pause("Press <ENTER> to continue. ")


def get_test():
        print('=================================')
        print('Perform GET test using httpbin.org')
	if use_tls:
          print(r'using TLS.')
          load_cert()
        cmd = "at+sqnhttpcfg=1,\"httpbin.org\"" + r
	channel0_at.write(cmd)
	waiting_response('OK')
        cmd = "AT+SQNHTTPQRY=1,0,\"/get\"" + r
	channel0_at.write(cmd)
	waiting_response('OK')
        get_line_include('+SQNHTTPRING: ')
        cmd = "AT+SQNHTTPRCV=1" + r
	channel0_at.write(cmd)
        print('Response is:')
        reading_raw_resp()
	if use_tls:
          remove_cert()
        print('=================================')
        pause("Press <ENTER> to continue. ")

def mqtt_recv(debug, server, port):
        mqtt_cfg = "AT+SQNSMQTTCLIENTCFG=0,\"" + clientID + "\""+ r
   	do_debug(debug, "Send Command: " + mqtt_cfg)
        channel0_at.write(mqtt_cfg)
        waiting_response_noexit('OK')
	try:
                mqtt_conn = 'AT+SQNSMQTTCLIENTCONNECT=0,"' + server + '",' + port + r
   		do_debug(debug,"Send Command: " + mqtt_conn)
                channel0_at.write(mqtt_conn)
                resp=get_line_include('+SQNSMQTTCLIENTONCONNECT:')
		if resp == '':
			print('TIME OUT:Unable to connect! ')
			return
   		do_debug(debug,"Connect Response: " + resp)

                mqtt_sub = "AT+SQNSMQTTCLIENTSUBSCRIBE=0,\"" + topic + "\",1" + r
   		do_debug(debug,"Send Command: " + mqtt_sub)
                channel0_at.write(mqtt_sub)
                get_line_include('+SQNSMQTTCLIENTONSUBSCRIBE:')
                print 'Subscription now active...'
          	while True:
	                resp = get_line_include('+SQNSMQTTCLIENTONMESSAGE:')
			print('Received a message: ' + resp)
			if resp != '':
			    cmd = 'AT+SQNSMQTTCLIENTRCVMESSAGE=0,"' + topic + '"' + r
   			    do_debug(debug,"Send Command: " + cmd)
			    channel0_at.write(cmd)
			    reading_resp()
        		    agn=pause("Press <X> to monitor/receive another. ")
                            if agn:
			        break
        finally:
		mqtt_disconn = 'AT+SQNSMQTTCLIENTDISCONNECT=0' + r
 		do_debug(debug,"Send Command: " + mqtt_disconn)
		channel0_at.write(mqtt_disconn)
		resp = get_line_include('OK')
		return

def mqtt_post(debug, server, port):
	try:
                mqtt_cfg = "AT+SQNSMQTTCLIENTCFG=0,\"" + clientID + "\""+ r
 		do_debug(debug,"Send Command: " + mqtt_cfg)
                channel0_at.write(mqtt_cfg)
                waiting_response('OK')

                mqtt_conn = 'AT+SQNSMQTTCLIENTCONNECT=0,"' + server + '",' + port + r
 		do_debug(debug,"Send Command: " + mqtt_conn)
                channel0_at.write(mqtt_conn)
                get_line_include('+SQNSMQTTCLIENTONCONNECT:')

                mqtt_sub = "AT+SQNSMQTTCLIENTSUBSCRIBE=0,\"" + topic + "\",1" + r
 		do_debug(debug,"Send Command: " + mqtt_sub)
                channel0_at.write(mqtt_sub)
                resp=get_line_include('+SQNSMQTTCLIENTONSUBSCRIBE:')
                print 'Subscription now active. ['+resp+']'
          	while True:
			msg = raw_input("Enter message to post or 'x' to exit: ")
                        if msg == 'x':
 				break
			cmd = 'AT+SQNSMQTTCLIENTPUBLISH=0,"' + topic + '",1' + r
			do_debug(debug,'Sending CMD: ' + cmd)
			channel0_at.write(cmd)
	                waiting_response('> ')
			channel0_at.write(msg + '')
	                get_line_include('+SQNSMQTTCLIENTPUBLISH:')
		
		mqtt_disconn = 'AT+SQNSMQTTCLIENTDISCONNECT=0' + r
 		do_debug(debug,"Send Command: " + mqtt_disconn)
		channel0_at.write(mqtt_disconn)
		resp = get_line_include('OK')
	finally:
		return

#====================================================================================================================

if __name__ == '__main__':
    args = parser.parse_args()
    checking_at()
    ans=True
    while ans:
        print("               ");
        print("     ****      ");
        print("    **  **     Python HTTP/MQTT/HTTPS example using the Sequans Monarch Go Starter Kit")
	if use_tls:
            print("   **    **    Using TLS.");
        else:
            print("   **    **    Not using TLS.");
        print("  ** ==== **   ");
        print ("""
        1.Display Modem FW version
        2.HTTP STREAM Test
        3.HTTP PUT Test
        4.HTTP POST Test
        5.HTTP DELETE Test
        6.HTTP GET Test
        7.MQTT Subscribe
        8.MQTT Post
        9.Toggle TLS 
        0.Exit
        """)
        ans=raw_input("Run which test? ") 
        if ans=="1": 
          print("\n Starter Kit Firmware:") 
          channel0_at.write('AT!="showversion"'+r)
          reading_raw_resp()
          print('=================================')
          pause("Press <ENTER> to continue. ")
        elif ans=="2":
          print("\n HTTP PUT Test") 
  	  stream_test()
        elif ans=="3":
          print("\n HTTP PUT Test") 
          put_test()
        elif ans=="4":
          print("\n HTTP POST Test") 
          post_test()
        elif ans=="5":
          print("\n HTTP DELETE Test") 
          delete_test()
        elif ans=="6":
          print("\n HTTP GET Test") 
          get_test()
        elif ans=="7":
          print("\nSetup for MQTT Subscribe") 
          mqtt_recv(args.debug, args.server, args.port)	
        elif ans=="8":
          print("\nSetup for MQTT Post") 
          mqtt_post(args.debug, args.server, args.port)	
        elif ans=="9":
          print("\nToggle TLS setting") 
	  use_tls = not use_tls
        elif ans=="0":
          print("\n Exit.") 
          sys.exit()
        else:
          print("\n Invalid entry!") 

    print('Exit programm.')
    channel0_at.close()

