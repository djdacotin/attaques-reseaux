

import sys
import os
import time
from scapy.all import *



try:
	
	#interface = raw_input("nom interface eth0 , eth1 ... ? ")
	#ipServeur = raw_input("IP du serveur actif ? ")
	#portServeur = int(raw_input("Port du serveur actif ? "))
	#fausseIp = raw_input("Vous souhaitez vous faire passer pour quelle fausse IP ? ")
	#portClientFausseIp = int(raw_input("Vous souhaitez vous faire passer pour quelle port TCP ? "))


	interface ="eth0"
	ipServeur = "10.0.0.2"
	portServeur = 21
	fausseIp = "10.0.0.5"
	portClientFausseIp = 9876


	print ("portServeur:"+ str(portServeur))
	print ("portClientFausseIp:"+ str(portClientFausseIp))

	#On cree une entete TCP de demande connexion avec drapeau SYN
	enteteTcp = TCP(dport=portServeur, sport=portClientFausseIp , flags="S")

	#On cree une entete IP avec une fausse IP source
	enteteIp = IP(dst=ipServeur, src=fausseIp)

	#sr1 permet d'envoyer un paquet (le 1er du TCP threehand shake) 
	# et de recupererla premiere reponse (le 2eme paquet du TCP threehand shake)
	reponse = sr1(enteteIp/enteteTcp)

	#probleme : on ne recoit jamais la reponse puisqu'on a falsifie l adresse ip source.
	# donc le reste du programme ne fonctionne pas. 

	#On doit se comporter comme un client donc creation du paquet ACK (le 3eme paquet du TCP threehand shake)
	ackNumber = reponse.seq + 1

	print ("ackNumber:"+ackNumber)
	enteteTcp2 = TCP(dport=portServeur, sport=portClientFausseIp , flags="A", ack=ackNumber,seq=1)
	reponse2 = sr1(enteteIp/enteteTcp2)
	
	
	

except Exception, e:
   	print ("Erreur...")
   	print (e)
   	sys.exit(1)



		


