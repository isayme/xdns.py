Dns Encrypt
===========

Encrypt dns query data before translation to avoid dns poisoning.

What does the script do ?
=========================

To avoid dns poisoning, I create a rep named [isayme/DnsByTcp](https://github.com/isayme/DnsByTcp "isayme/DnsByTcp"). It make a TCP connection to avoid dns poisoning.  

But for this project, I prefer to make a UDP socket, and for the some purpose there must be some other method.  

The method I use is encrypting the DNS query. But, as normally known DNS servers donot realize my methon(in fact, I just return the complement of DNS query data), so to use the project, you have to run the script at local and a remote machine.

How to use
==========

For remote server(normally a vps server):
------------------

+ Open the python script for edit;
+ Change The MACRO LOCAL_DNS_IP to your remote machine's IP;
+ Change The MACRO REMOTE_DNS_IP to any famous dns server's IP;

For local machine(normally your PC):
------------------

+ Open the python script for edit;
+ Change The MACRO LOCAL_DNS_IP to '127.0.0.1';
+ Change The MACRO REMOTE_DNS_IP to your remote server's IP(the above remote server);

Question ?
==========

Any question ? Just mail to me !  
Mail : isaymeorg [dot] gmail [dot] com