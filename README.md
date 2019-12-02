---

# Sequans Monarch-GO Python Demonstration Code
## Overview

Monarch is a single-chip LTE solution designed specifically for narrowband IoT applications, details of the solution are located at https://www.sequans.com/products-solutions/monarch-lte-platform/. The Monarch-GO comes (<<add product purchase link>>) with an interface board that provides a USB/UART VCP interface so it can easily be connected to a PC with an avaialble USB port.  To demonstrate some of the solutions functionality, this python script demonstrates implementation of the HTTP and MQTT connection methods. When run, the script presents the user a menu of actions:

```
     ****      
    **  **     Python HTTP/MQTT/HTTPS example using the Sequans Monarch Go Starter Kit
   **    **    Not using TLS.
  ** ==== **   

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
        
Run which test? 
```
The tests can be run with or without TLS by toggleing the TLS flag (selction #9)

## Running the Script
When you start the script, the following flags are possible:
```
usage: http_demo.py [-h] [-d] [-s SERVER] [-p PORT]

Script demonstrating HTTP/HTTPS/MQTT usage

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           enable output of debug messages
  -s SERVER, --server SERVER
                        server ip addr or domain name
  -p PORT, --port PORT  server port

!! Verify UART (uart0_at) and speed (uart0_at_speed) settings in script !!
```

 - Enabling debug message will cause the script to print the AT commands and responses to/from the Sequans Monarch-go
 - Allows you to set the SERVER if you want to use something other than 'broker.hivemq.com' (default)
 - Sets the PORT to a value other than 1883 (default)

The message at the bottom is  a reminder to check the settings of the variable **uart0_at**.  The value of **uart0_at** may change depending on how the VCP is enumerated by the computer when connected.


## HTTP Interactions
All HTTP functions interact with httpbin.org.  This site is a simple HTTP Request & Response service that provides a handy way to exercise HTTP requests.  Typically, it simply replies with the original request.  The test provides examples for common HTTP methods and when run, the reponse is generally:


```
{
  "args": {},
  "data": "PUT TEST",
  "files": {},
  "form": {},
  "headers": {
    "Content-Length": "8",
    "Host": "httpbin.org"
  },
  "json": null,
  "origin": "174.245.65.89, 174.245.65.89",
  "url": "https://httpbin.org/put"
}

=================================
Press <ENTER> to continue. 
```

When TLS is enabled, the script uses the certificate from httpbin.org to perform the exchange (the certificate is defined at the top of the http_demo.py script).

## MQTT Interactions

The MQTT examples are setup to use HiveMQ (www.hivemq.com) which is a MQTT broker service that allows users to publish and subscribe to topics for free using the URL **broker.hivemq.com**.  If you are using chrome, an easy way to use the Hive broker is to install MQTTBox application (it is also available for Linux, Mac, and Windows). The demo script uses: 

    topic = "sqn/test" 
    clientID = "client-test1"

So the MQTTBox server setup is:

    MQTT Client Name: SQN-Test
    Protocol: mqtt/tcp
    MQTT Client id: client-test1
    Host: broker.hivemq.com

The default for other setting are fine to get the demo working.

Once MQTTBox is setup it will connect to the Hive MQTT broker and you can subscribe to **sqn/test** to see when topics are posted.  Similarly, you can post to **sqn/test**.  When you post from the Post dialog, the message contents will show up in the Subscribe dialog (if subscribed) which is a good way to that the settings are all correct.

When you select 7 (MQTT Subscribe), any messages posted to sqn/test will be received.  This can be demonstrated by using the POST dialog to post a message.  Once posted, the message will be displayed on in the SUBSCRIBE dialog and the same message will be displayed by the script, for example:

               
         ****      
        **  **     Python HTTP/MQTT/HTTPS example using the Sequans Monarch Go Starter Kit
       **    **    Not using TLS.
      ** ==== **   
    
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
            
    Run which test? 7
    
    Setup for MQTT Subscribe
    Subscription now active...
    Received a message: +SQNSMQTTCLIENTONMESSAGE:0,"sqn/test",27,1,51
    
    
    
    {'it':'works still 543210'}
    
    OK
    
    Press <X> to monitor/receive another. 

Similarly, when you select 8 (MQTT Post) you will be prompted to enter a message.  The message you enter will be posted to the Hive MQTT broker and will be displayed in the SUBSCRIBE dialog:
               
         ****      
        **  **     Python HTTP/MQTT/HTTPS example using the Sequans Monarch Go Starter Kit
       **    **    Not using TLS.
      ** ==== **   
    
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
            
    Run which test? 8
    
    Setup for MQTT Post
    Subscription now active. [+SQNSMQTTCLIENTONSUBSCRIBE:0,"sqn/test",0
    ]
    Enter message to post or 'x' to exit: How now brown cow, 0123456789
    Enter message to post or 'x' to exit: x





