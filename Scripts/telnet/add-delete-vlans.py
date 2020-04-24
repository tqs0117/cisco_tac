#!/usr/bin/env python3

import getpass
import sys
import telnetlib
import time

# host ip
HOST = "10.122.163.64"

# auth method if needed
user = raw_input("Enter your remote account: ")
password = getpass.getpass(prompt='Password: ')
enable = getpass.getpass(prompt='Enable: ')

# test vlans should be added in following list
vlan = [11, 22, 33, 44, 55, 66, 77, 88, 99, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 220, 221, 222, 223, 224,
		225, 226, 227, 228, 229, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 440, 441, 442, 443, 444, 445, 446,
		447, 448]

# for iteration count
it = 0



session = telnetlib.Telnet(HOST)

session.read_until("Username: ")

session.write(user + "\n")

if password:
    session.read_until("Password: ")
    session.write(password + "\n")

session.write("enable\n")

session.read_until("Password: ")
session.write(enable + "\n")

session.read_until("F340.08.03-2900L-1#")
session.write("ter len 0\n")


while(1):

	# 2960L-DUT should be replaced by actual host name

	print time.ctime(int(time.time()))
	f = open("Result.txt", "a+")
	f.write(str(time.ctime(int(time.time()))))
	f.write("\n")
	f.close()

	# session.read_until("F340.08.03-2900L-2#")
	session.write("conf t\n")

	session.read_until("(config)#")
	session.write("no vlan %s\n" % ",".join(map(str, vlan)))
	print "deleted vlan %s\n" % ",".join(map(str, vlan))

	session.read_until("(config)#")
	session.write("vlan %s\n" % ",".join(map(str, vlan)))

	print "added vlan %s\n" % ",".join(map(str, vlan))

	session.read_until("(config-vlan)#")
	session.write("end\n")

	for i in vlan:

		print "\nchecking vlan %s" % i

		session.read_until("F340.08.03-2900L-1#")

		session.write("show platform port-asic vlan asic-num 1 vlan %d\n" % i)

		# 2960L-DUT should be replaced by actual host name
		output = session.read_until("F340.08.03-2900L-1#")
		#print output
		#print len(output)

		if len(output) > 0:
			lines = output.split("\n")
			for line in lines:
				#print line
				if line.find("isValid:0") != -1:
					print ("Issue was observed at Vlan %d" % i)
					f = open("Result.txt", "a+")
					f.write("Issue was observed at Vlan %d" % i)
					f.write(output)
					f.close()
					exit()
				elif line.find("isValid:1") != -1:
					print ("vlan %d is good" % i)
			session.write("\n")


	print ("No issue was observed for iteration %d\n" % it)
	f = open("Result.txt", "a+")
	f.write("No issue was observed for iteration %d\n" % it)
	f.close()
	it = it + 1
	time.sleep(5)


#print session.read_eager()

#session.write("exit\n")

#print session.read_all()

#print "end"
