## Criar monitoração no zabbix:

host=<nome_do_driver>

doc="https://globo.service-now.com/kb_view.do?sysparm_article=<KB>",

notification_email="globomap@corp.globo.com",

notification_slack="#storm-alarmes",

hostgroups="1669"


## Criar KB no service now:
Base de Conhecimento: Suporte

Categoria: Globomap

Implementado por: Globo Map

Titulo: [Alarme GloboMap Driver Zabbix] - passive_<nome_do_driver>

Texto:<br>
O Alarme passive_<nome_do_driver>

Sintomas

Alarme no zabbix

Causa

- O serviço não está rodando.
- Falha de comunicação com o Zabbix.
- Janela de manutenção

Resolução

Em caso de janela, botar o alarm ACK. Se após o fim da janela o alarme não sumir ou não tenha janela, favor colocar o alarme em ACK e abrir um PRB para o time Storm.

Nos outros casos, abrir um PRB e enviá-lo para o Time Storm. Colocar Não há necessidade de acionamento fora do horário comercial.
