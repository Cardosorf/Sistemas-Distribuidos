# Aplicação cliente/servidor concorrente

 Este laboratório é uma continuação do Laboratório 2.
 Desse modo, estendemos a aplicação distribuída desenvolvida no Laboratório 2 para aplicar os conceitos estudados sobre servidores concorrentes (ou multitarefa) e multiplexados
 
## Lado Servidor

 É constituído pelos arquivos ladoServidor.py e auxiliarBase.py.
 
 O arquivo ladoServidor.py é o script que inicia o servidor e se coloca em modo de espera por conexões dos clientes. Além disso, solicita o acesso ao arquivo, realiza a busca pela palavra informada e prepara a resposta para ser devolvida para a camada de interface no formato json. Além disso, o servidor é capaz de receber comandos básicos da entrada padrão, como "fim" para para finalizar o servidor quando não existir clientes ativos, "historico" para listar o histórico de conexões e "ativos" para listar os clientes ainda ativos. 

 O arquivo auxiliarBase.py é responsável por verificar se o arquivo existe na base e por devolver o seu conteúdo, caso exista.
 
 
## Lado Cliente

 É constituído pelo arquivo ladoCliente.py.
 
 Este arquivo é o script que atua como o cliente e se conecta com o servidor. Além disso, recebe comandos básicos da entrada padrão para permitir a escrita do nome do arquivo, a palavra a ser buscada e encerrar a conexão com o servidor através do comando "||END||".
 Também recebe o resultado do processamento do servidor através de uma mensagem no formato json contento o número de palavras que foram encontradas no arquivo ou, então, alguma mensagem de erro.

## Observações

 A aplicação foi desenvolvida no sistema Linux e a linguagem utilizada foi Python 3.5.2.
