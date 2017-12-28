from __builtin__ import any as is_any
import os
import logging

logging.basicConfig(filename='alfa_conf.log',level=logging.DEBUG,format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

start_up_dir = "/etc/rc.local"

# function to discover wlan interface dynamically, if only 1 wireless iface exists, use that - otherwise default to the very last wireless iface.
def find_wlan():
	net_ifaces = os.listdir("/sys/class/net")
	wireless_iface = "wlan"
	test_wlan = is_any(wireless_iface in i for i in net_ifaces)
	if test_wlan is True:
		wlan_ifaces = [j for j in net_ifaces if wireless_iface in j]
		logging.info('WLAN Interface(s) found as: ')
		for x in wlan_ifaces:
			logging.info('\t %s' % x)
		num_ifaces = len(wlan_ifaces)
		if num_ifaces is 1:
			wlan_result = str(wlan_ifaces[0])
			logging.info('Utilizing: %s' % wlan_result)
			return wlan_result
		elif num_ifaces != 0 and num_ifaces != 1:
			wlan_result = str(wlan_ifaces[num_ifaces - 1])
			logging.info('Utilizing last wlan interface: %s' % wlan_result)
			return wlan_result
		else:
			logging.warning('No interfaces listed.')
			return None

	else:
		logging.error('No wireless interface could be found...Exiting.')
		return None
		exit(1)

wlan = find_wlan()

if wlan is None:
	logging.error('No wireless interface was listed after being identified...Exiting.')
	exit(1)
else:
	logging.info('Bringing %s interface down...' % wlan)
	os.system('ifconfig %s down' % wlan)
	logging.info('Setting random MAC Address...')
	os.system('macchanger -r %s' % wlan)
	logging.info('Changing country region...')
	os.system('iw reg set GY')
	logging.info('Increasing interface txpower to 30...')
	os.system('iwconfig %s txpower 30' % wlan)
	logging.info('Bringing %s interface up...' % wlan)
	os.system('ifconfig %s up' % wlan)
	exit(0)