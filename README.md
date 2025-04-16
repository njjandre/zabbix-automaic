# zabbix-automaic
Cadastro de hosts automatioc
 Ferramenta de Cadastro Automático de Hosts no Zabbix
Este projeto é uma aplicação desenvolvida em Python com o objetivo de automatizar o processo de cadastro de hosts no Zabbix — algo que, por padrão, a plataforma não oferece de forma nativa.

🔧 Funcionalidades
Interface gráfica amigável (GUI) para facilitar o uso.

Varredura por faixa de IP (range), definindo IP inicial e final.

Identificação automática do nome dos hosts via DNS reverso.

Associação automática dos hosts aos seus respectivos grupos.

Aplicação dos templates adequados no momento do cadastro.

Geração de logs completos para rastreabilidade.

Aplicação empacotada em .exe (Windows), com ícone personalizado, pronta para uso sem necessidade de instalar dependências.

💡 Sobre a Solução
Para uma solução simples, a aplicação entrega bastante valor, especialmente em cenários com grande volume de dispositivos a serem cadastrados, como antenas, impressoras e outros equipamentos de rede. Claro que ainda há pontos a melhorar, mas o foco foi resolver de forma prática e eficiente uma dor real do dia a dia.

✅ Requisitos
Python 3.10+

Acesso à API do Zabbix

(Opcional) Ambiente Windows para usar a versão empacotada .exe

🚀 Próximos passos
Melhorias na UI

Validação de campos

Opção para agendamento de varredura

Exportação de logs em formatos alternativos (CSV, JSON)

