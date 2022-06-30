# Python
questo è il primo progetto che carico su github, si tratta di uno script di python che permette di fare un attacco di tipo DHCP Starvation
questo progetto l'ho fatto durante il corso dedicato appunto a python, durante il mio percorso di studio presso ICT Piemonte 

#Documentazione DHCP Starvation:
Programma pensato per sistemi di tipo Linux, Debian-Like.
personalmente l’ho testato su Ubuntu, nello specifico la versione 20.04LTS.

versione di python usata: 3.8.10

ed è stato testato “attaccando”, un pfsense con questa specifica iso:
pfSense-CE-2.5.2-RELEASE-amd64.iso, scaricabile qui:
https://repo.ialab.dsu.edu/pfsense/pfSense-CE-2.5.2-RELEASE-amd64.iso.gz 
Librerie utilizzate e comandi per l’installazione:
time, os: già presente di default in python
scapy: comando da usare, sudo pip install --pre scapy[basic], teoricamente dovrebbe bastare questo secondo la documentazione, nel caso di problemi provare: sudo pip install --pre scapy[complete]
netifaces: comando da usare, pip install netifaces
ipaddress: comando da usare, pip install ipaddress
getmac: sudo pip install getmac

per usare questo script bisogna utilizzare per forza il comando “sudo” prima dell’esecuzione.

per eseguire dunque fare:
eseguire il comando “chmod 770”, assicurarsi che il path di python sia corretto nella prima riga del codice, dopo di che usare il comando: “sudo ./dhcpstarvation.py” 
usare il comando: “sudo python3 dhcpstarvation.py” 

