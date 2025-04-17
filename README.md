🔧 Zabbix Auto Register – Cadastro automático de hosts via GUI (Tkinter + PyZabbix)
Você já precisou adicionar vários hosts no Zabbix manualmente? Essa ferramenta resolve isso com uma interface simples e amigável! Aqui está um passo a passo de como desenvolvi o script que faz tudo isso acontecer usando Python.

🧠 Ideia
Automatizar o processo de:

Verificar se hosts respondem na rede.

Obter seus nomes (hostname).

Verificar se já existem no Zabbix.

Se não, cadastrar com o grupo e template informados.

Tudo isso via interface gráfica!

⚙️ Tecnologias Utilizadas
Python 3

Tkinter para a interface gráfica

pyzabbix para interação com a API do Zabbix

subprocess, ipaddress, socket e outros módulos nativos

📦 Instalação
bash
Copiar
Editar
pip install pyzabbix
🖼️ Interface Gráfica
A interface foi feita com tkinter e permite:

Conectar no servidor Zabbix

Informar IP inicial/final para escanear

Selecionar Grupo e Template com autocomplete

Acompanhar logs da execução

Pausar a varredura a qualquer momento

💡 Principais Funções
1. Conexão com o Zabbix

python
Copiar
Editar
zapi = ZabbixAPI(ZABBIX_SERVER)
zapi.login(ZABBIX_USER, ZABBIX_PASSWORD)
2. Verificação de disponibilidade via ping

python
Copiar
Editar
subprocess.run(["ping", "-n", "1", "-w", "1000", ip])
3. Obter hostname

python
Copiar
Editar
hostname = socket.gethostbyaddr(ip)[0]
4. Cadastro automático via API

python
Copiar
Editar
zapi.host.create(...)
📑 Resultado
Hosts online são cadastrados automaticamente

Evita duplicidade

Gera log da execução (log_zabbix_*.txt)

Interface leve e direta

🧪 Próximos passos
Adicionar suporte a múltiplas interfaces (ex: SNMP, JMX)

Compatibilidade multiplataforma (Linux/Mac)

Empacotar como .exe via PyInstaller

🧑‍💻 Autor
Nilson Jandre
🛠️ DevOps & Automação
🔗 [Seu LinkedIn ou GitHub]
