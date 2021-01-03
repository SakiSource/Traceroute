import ipinfo
import requests
import json
import time


def main():
    file = open("routes.txt")
    line = file.readline()
    startDividing = 0
    # Retrive address from text file
    while line != '':
        line = file.readline()
        currentLineSplit = line.split()
        if len(currentLineSplit) == 0 or len(currentLineSplit) == 1:
                print("")
        elif currentLineSplit != [] and currentLineSplit[0] == "traceroute": # traceroute line
            if startDividing == 0:
                startDividing = startDividing + 1
            else:
                print(averageTime)
                print("Number of hops [" + str(counter) + "]")
            print("")
            counter = 0
            print("************************************************")
            print("Host Info ")
            print("Host Address: ")
            print(currentLineSplit[2])
            print("Host IP: ")
            hostIp = currentLineSplit[3]
            hostIp = hostIp[:-1]
            print(bracketRemove(hostIp))
            print("************************************************")
            averageTime = 0
        elif currentLineSplit != [] and currentLineSplit[1] == "*":
            counter = counter + 1
            print("Hop: [" + str(counter) + "]")
            print("Timed out")
            print("")
        else:
            counter = counter + 1
            print("Hop: [" + str(counter) + "]")

            print("Web Address: ")
            print(currentLineSplit[1])

            print("IP Address: ")
            ip = bracketRemove(currentLineSplit[2])
            print(ip)

            response = requests.get("http://ip-api.com/json/" + ip + "?fields=status,message,country,city,lat,lon,isp,asname,query")
            data = response.json()
            retryTime = response.headers['X-Rl']
            if retryTime == "1":
                time.sleep(65)

            print("Physical Location: ")
            print(findLocation(data))

            print("Network: ")
            print(findNetwork(data))

            print("Provider: ")
            print(findISP(data))

            print("")

            averageTime = currentLineSplit[3]
    print(averageTime)

def bracketRemove(ipAddress): # Remove the brackets
    noBrackets = ipAddress[1:-1]
    return noBrackets

def findISP(data): ## Find the Organisation
    if data["status"] == "success":
        if len(data["isp"]) != 0:
            return data["isp"]
        else:
            return "0"
    else:
        return "0"

def findNetwork(data): # Find the network
    if data["status"] == "success":
        if len(data["asname"]) != 0:
            return data["asname"]
    else:
        return "0"

def findLocation(data): ## Find the physical address
    if data["status"] == "success":
        return data["country"] + ", " + data["city"] + "\n" + "Lat: " + str(data["lat"]) + "\n" + "Lon: " + str(data["lon"])
    else:
        return "0"


main()
