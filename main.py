import argparse
import pyfiglet
import socket
from datetime import datetime

parser = argparse.ArgumentParser(description="ScanniFy - Ein einfacher Portscanner")
parser.add_argument("-t", "--target", required=True, help="Ziel-IP-Adresse oder Hostname")
parser.add_argument("-sT", "--syn-scan", action="store_true", help="Führe einen SYN-Portscan durch")
parser.add_argument("-o", "--output-file", help="Datei, in die die Ergebnisse geschrieben werden sollen")
parser.add_argument("aktion", choices=["offen", "geschlossen", "alle"], help="Aktion zum Scannen (offen, geschlossen, alle)")

args = parser.parse_args()

ascii_banner = pyfiglet.figlet_format("ScanniFy")
print(ascii_banner)

target = args.target

print("_" * 50)
print("Scanning Target: " + target)
print("Scanning started at: " + str(datetime.now()))
print("_" * 50)

try:
    open_ports = []
    closed_ports = []

    for port in range(1, 65536):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.5)

        result = s.connect_ex((target, port))
        if result == 0:
            open_ports.append(port)
            if args.syn_scan:
                print("[*] Port {} is open (SYN scan)".format(port))
            else:
                print("[*] Port {} is open".format(port))
        else:
            closed_ports.append(port)
        s.close()

    if args.aktion == "offen":
        print("Offene Ports:", open_ports)
    elif args.aktion == "geschlossen":
        print("Geschlossene Ports:", closed_ports)
    elif args.aktion == "alle":
        print("Offene Ports:", open_ports)
        print("Geschlossene Ports:", closed_ports)

    if args.output_file:
        with open(args.output_file, "w") as file:
            file.write("Offene Ports auf {}: {}\n".format(target, open_ports))

except Exception as e:
    print("An error occurred:", str(e))
