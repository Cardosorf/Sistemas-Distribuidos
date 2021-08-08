# Aluno: Rafael Pais Cardoso
# DRE: 116140788
# Atividado: Lab 2
# Lado Cliente

import socket   
import json

HOST                    = 'localhost' # maquina onde esta o par passivo
PORTA                   = 5000        # porta que o par passivo esta escutando
CLOSE_CONNECTION_CODE   = '||END||'

def MontaMensagem(nomeArquivo, palavraBuscada):
	# tipo de mensagem trocada entre o cliente e o servidor
	json_obj_send   = { "arquivo": None, "palavra": None,"contagem": None, "sucesso": None, "mensagemErro": None }
	json_obj_send["arquivo"] = nomeArquivo
	json_obj_send["palavra"] = palavraBuscada
	return json_obj_send

def IniciaCliente():
	# cria socket
	sock = socket.socket() # default: socket.AF_INET, socket.SOCK_STREAM 
	
	# conecta-se com o par passivo
	sock.connect((HOST, PORTA)) 
	
	print('Conectado ao servidor com sucesso.')
	print('Envie o nome do arquivo com a extensão (i.e., \'receitas.txt\' sem aspas) e a palavra a ser buscada (i.e., \'abacate\' sem aspas).')
	print('OBS: O nome do arquivo e a palavra a ser buscada serão normalizados.')
	print('Caso queira encerrar, digite \'||END||\' (sem aspas) em qualquer momento.')

	while(True):
		nomeArquivo = str(input("Digite o nome do arquivo: "))
	
		if (nomeArquivo == CLOSE_CONNECTION_CODE):
			break
	
		if not nomeArquivo or nomeArquivo.isspace():
			print('Nome de arquivo nulo ou vazio. Por favor, digite algo válido')
			continue
	
		palavraBuscada = str(input("Digite o nome da palavra: "))

		if (palavraBuscada == CLOSE_CONNECTION_CODE):
			break

		while(not palavraBuscada or palavraBuscada.isspace()):
			print('Palavra buscada nula ou vazia. Por favor, digite algo válido')
			palavraBuscada = str(input("Digite o nome da palavra: "))
		
		mensagem = MontaMensagem(nomeArquivo, palavraBuscada)
	
		# envia uma mensagem para o par conectado
		sock.send(bytes(json.dumps(mensagem), encoding='utf-8'))
	
		# espera a resposta do par conectado (chamada pode ser BLOQUEANTE)
		mensagemRecebida = sock.recv(1024) # argumento indica a qtde maxima de bytes da mensagem
	
		mensagemRecebida = json.loads(str(mensagemRecebida, encoding='utf-8'))
	
		if(mensagemRecebida["sucesso"] == False):
			print(mensagemRecebida["mensagemErro"])
		else:
			mensagem = 'No arquivo {nomeArquivo} foi possível encontrar {numeroContagem} ocorrências da palavra {nomePalavra}.'
			print(mensagem.format(nomeArquivo = mensagemRecebida["arquivo"], numeroContagem = mensagemRecebida["contagem"], nomePalavra = mensagemRecebida["palavra"]))
	
	# encerra a conexao
	sock.close() 

IniciaCliente()