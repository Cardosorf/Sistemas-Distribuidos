# Aluno: Rafael Pais Cardoso
# DRE: 116140788
# Atividade: Lab 2
# Lado Servidor

import socket
import json
import os
import auxiliarBase
import select
import sys
import threading

HOST        = ''    # '' possibilita acessar qualquer endereco alcancavel da maquina local
PORTA       = 5000  # porta onde chegarao as mensagens para essa aplicacao
SEPARADORES = [" ",",",".","!","?",":","/","\\",";","(",")","[","]","{","}"] 

#define a lista de I/O de interesse (jah inclui a entrada padrao)
entradas = [sys.stdin]
#armazena historico de conexoes 
conexoes = {}

def NormalizaTexto(texto):
	return texto.lower()

def NormalizaJson(mensagem_json):
	'''Transforma as letras da palavra e do arquivo buscados em minuscula
	Entrada: mensagem no formato json
	Saida: '''

	mensagem_json["arquivo"] = NormalizaTexto(mensagem_json["arquivo"])
	mensagem_json["palavra"] = NormalizaTexto(mensagem_json["palavra"])

def NomeDaPalavraValido(mensagem_json):
	'''Verifica se a palavra esta correta
	Entrada: mensagem no formato json
	Saida: falso quando a palavra for invalida e verdadeiro quando valida'''

	if not mensagem_json["palavra"] or mensagem_json["palavra"].isspace():
		mensagem_json["sucesso"]        = False
		mensagem_json["mensagemErro"]   = "Palavra inválida"
		return False
	else:
		return True

def normalizacaoTokenizacao(dados):
	'''Remove os separadores e transforma as letras das palavras em minuscula
	Entrada: o arquivo de texto
	Saida: o arquivo de texto com as letras das palavras em minuscula e sem os separadores'''

	for delimitador in SEPARADORES:
		dados = dados.lower().replace(delimitador, " ")
	return dados

def ContaPalavrasDoArquivo(mensagem_json):
	'''Conta o numero de ocorrencia da palavra no arquivo e atualiza a mensagem
	Entrada: mensagem no formato json
	Saida: '''

	mensagem = 'Lendo o arquivo {nomeArquivo} e contando o número de ocorrências da palavra {nomePalavra}.'
	print(mensagem.format(nomeArquivo = mensagem_json["arquivo"], nomePalavra = mensagem_json["palavra"]))

	contador        = 0
	dados           = auxiliarBase.LeArquivo(mensagem_json)
	dados           = normalizacaoTokenizacao(dados)
	listaPalavras   = dados.split()

	for i in range(len(listaPalavras)):
		if (listaPalavras[i] == mensagem_json["palavra"]):
			contador+= 1

	mensagem_json["contagem"]   = contador
	mensagem_json["sucesso"]    = True

def IniciaServidor():
	'''Cria um socket de servidor e o coloca em modo de espera por conexoes
	Saida: o socket criado'''

	# cria o socket 
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Internet( IPv4 + TCP) 
	print('Servidor estabelecido.')
	# vincula a localizacao do servidor
	sock.bind((HOST, PORTA))
	# coloca-se em modo de espera por conexoes
	sock.listen(5) 
	# configura o socket para o modo nao-bloqueante
	sock.setblocking(False)
	# inclui o socket principal na lista de entradas de interesse
	entradas.append(sock)

	return sock

def AceitaConexao(sock):
	'''Aceita o pedido de conexao de um cliente
	Entrada: o socket do servidor
	Saida: o novo socket da conexao e o endereco do cliente'''

	# estabelece conexao com o proximo cliente
	clisock, endr = sock.accept()
	# registra a nova conexao
	conexoes[clisock] = endr 

	return clisock, endr

def AtendeRequisicoes(clisock, endr):
	'''Recebe mensagens e as envia de volta para o cliente (ate o cliente finalizar)
	Entrada: socket da conexao e endereco do cliente
	Saida: '''

	while True:
		# recebe dados do cliente
		mensagemRecebida = clisock.recv(1024) # argumento indica a qtde maxima de dados
			
		if not mensagemRecebida: # dados vazios: cliente encerrou
			print(str(endr) + '-> encerrou')
			clisock.close() # encerra a conexao com o cliente
			return 
	
		json_obj_recv = json.loads(str(mensagemRecebida, encoding='utf-8')) # carrega o json

		# normaliza o nome do arquivo e a palavra a ser buscada no texto
		NormalizaJson(json_obj_recv)

		# verifica se o nome do arquivo é válido. Caso não seja válido, retorna uma mensagem de erro para o cliente
		if(not auxiliarBase.NomeDoArquivoValido(json_obj_recv)):
			clisock.send(bytes(json.dumps(json_obj_recv), encoding='utf-8')) 
			continue

		# verifica se o caminho do arquivo é válido. Caso não seja válido, retorna uma mensagem de erro para o cliente
		if(not auxiliarBase.CaminhoDoArquivoValido(json_obj_recv)):
			clisock.send(bytes(json.dumps(json_obj_recv), encoding='utf-8')) 
			continue

		# verifica se o nome da palavra é válido. Caso não seja válido, retorna uma mensagem de erro para o cliente
		if(not NomeDaPalavraValido(json_obj_recv)):
			clisock.send(bytes(json.dumps(json_obj_recv), encoding='utf-8')) 
			continue

		ContaPalavrasDoArquivo(json_obj_recv)

		# envia mensagem para o cliente
		print('Processamento concluído. Enviado mensagem para o cliente.')
		clisock.send(bytes(json.dumps(json_obj_recv), encoding='utf-8')) 

def Main():
	'''Inicializa e implementa o loop principal (infinito) do servidor'''

	clientes = [] #armazena as threads criadas para fazer join
	
	sock     = IniciaServidor()

	print("Pronto para receber conexoes...")

	print("Comandos basicos do servidor: \n'fim' para finalizar o servidor quando nao existir clientes ativos; \n'historico' para listar o historico de conexoes; \n'ativos' para listar os clientes ainda ativos")

	while(True):
		#espera por qualquer entrada de interesse
		leitura, escrita, excecao = select.select(entradas, [], [])
		#tratar todas as entradas prontas
		for pronto in leitura:
			if pronto == sock:  #pedido novo de conexao
				clisock, endr = AceitaConexao(sock)
				print ('Conectado com: ', endr)
				#cria nova thread para atender o cliente
				cliente = threading.Thread(target=AtendeRequisicoes, args=(clisock,endr))
				cliente.start()
				clientes.append(cliente) #armazena a referencia da thread para usar com join()
			elif pronto == sys.stdin: #entrada padrao
				cmd = input()
				if cmd == 'fim': #solicitacao de finalizacao do servidor
					for c in clientes: #aguarda todas as threads terminarem
						c.join()
					sock.close()
					sys.exit()
				elif cmd == 'historico': #mostra o historico de conexoes
					mensagem = 'Historico de conexoes: {historicoConexoes}.'
					print(mensagem.format(historicoConexoes = str(conexoes.values())))
				elif cmd == 'ativos': #mostra a qtde de threads que estao ativas
					mensagem = 'Clientes ativos: {clientesAtivos}.'
					print(mensagem.format(clientesAtivos = str(threading.active_count() - 1)))

Main()
