# WireCrack
Pentest tool com foco em teste de intrusão em redes wireless para Windows

# Como funciona?
A ferramenta ultiza o modulo <b>netsh.exe</b> do nosso querido rWindows, para se conectar a rede com as senhas de uma wordlist
e também usa a powershell para validar a conexão (uma sugestão seria mudar a validação para algo como ver se você possui um gateway, pois dessa forma se a rede não tiver conexão no momento do bruteforce, a ferramenta não vai funcionar)

# Como usar?
<code>python <b>C:\Users\usuario\WireCrack\WireCrack.py</b> --ssid "Rede a ser atacada" --wordlist rockyou.txt --auth wpa</code>