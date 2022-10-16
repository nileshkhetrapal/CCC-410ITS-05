'''
The function of this script is to resolve DNS names of all the hosts in a range /24 with the IP and DNS server piped in from the command line.
'''
$scope = $args[0]
$serverIP = $args[1]

#Generate all the IP addreses
For ($i=0; $i-le 255; $i++) {
$ip = $scope + ("."+ $i)
Write-host $ip
#Resolve-DnsName -DnsOnly {$ip} -Server {$serverIP}
}


#for loop through all the IP addresses

#Resolve-DnsName -DnsOnly 192.168.3 -Server 192.168.4.4
#
