# Aluno: Rafael Pais Cardoso
# DRE: 116140788
# Atividade: Lab 2
# Lado Servidor

import socket
import json
import os
import auxiliarBase

HOST        = ''    # '' possibilita acessar qualquer endereco alcancavel da maquina local
PORTA       = 5000  # porta onde chegarao as mensagens para essa aplicacao
SEPARADORES = [" ",",",".","!","?",":","/","\\",";","(",")","[","]","{","}"] 

def NormalizaTexto(texto):
	return texto.lower()

def NormalizaJson(mensagem_json):
	mensagem_json["arquivo"] = NormalizaTexto(mensagem_json["arquivo"])
	mensagem_json["palavra"] = NormalizaTexto(mensagem_json["palavra"])

def NomeDaPalavraValido(mensagem_json):
	if not mensagem_json["palavra"] or mensagem_json["palavra"].isspace():
		mensagem_json["sucesso"]        = False
		mensagem_json["mensagemErro"]   = "Palavra inválida"
		return False
	else:
		return True

def normalizacaoTokenizacao(dados):
	for delimitador in SEPARADORES:
		dados = dados.lower().replace(delimitador, " ")
	return dados

def ContaPalavrasDoArquivo(mensagem_json):
	mensagem = 'Lendo o arquivo {nomeArquivo} e contando o número de ocorrências da palavra {nomePalavra}.'
	print(mensagem.format(nomeArquivo = mensagem_json["arquivo"], nomePalavra = mensagem_json["palavra"]))

	contador        = 0
	dados           = auxiliarBase.LeArquivo(mensagem_json)
	dados 			= normalizacaoTokenizacao(dados)
	listaPalavras   = dados.split()

	for i in range(len(listaPalavras)):
		if (listaPalavras[i] == mensagem_json["palavra"]):
			contador+= 1

	mensagem_json["contagem"]   = contador
	mensagem_json["sucesso"]    = True

def IniciaServidor():
	# cria um socket para comunicacao
	sock = socket.socket() # valores default: socket.AF_INET, socket.SOCK_STREAM  
	
	# vincula a interface e porta para comunicacao
	sock.bind((HOST, PORTA))
	
	print('Servidor estabelecido.')
	
	# define o limite maximo de conexoes pendentes e coloca-se em modo de espera por conexao
	sock.listen(5) 
	
	while(True):
		# aceita a primeira conexao da fila (chamada pode ser BLOQUEANTE)
		novoSock, endereco = sock.accept() # retorna um novo socket e o endereco do par conectado
	
		print ('Conectado com:', endereco)
	
		while(True):
			# depois de conectar-se, espera uma mensagem (chamada pode ser BLOQUEANTE))
			mensagemRecebida = novoSock.recv(1024) # argumento indica a qtde maxima de dados
			
			if not mensagemRecebida: break
	
			json_obj_recv = json.loads(str(mensagemRecebida, encoding='utf-8')) # carrega o json

			# normaliza o nome do arquivo e a palavra a ser buscada no texto
			NormalizaJson(json_obj_recv)

			# verifica se o nome do arquivo é válido. Caso não seja válido, retorna uma mensagem de erro para o cliente
			if(not auxiliarBase.NomeDoArquivoValido(json_obj_recv)):
				novoSock.send(bytes(json.dumps(json_obj_recv), encoding='utf-8')) 
				continue

			# verifica se o caminho do arquivo é válido. Caso não seja válido, retorna uma mensagem de erro para o cliente
			if(not auxiliarBase.CaminhoDoArquivoValido(json_obj_recv)):
				novoSock.send(bytes(json.dumps(json_obj_recv), encoding='utf-8')) 
				continue

            # verifica se o nome da palavra é válido. Caso não seja válido, retorna uma mensagem de erro para o cliente
			if(not NomeDaPalavraValido(json_obj_recv)):
				novoSock.send(bytes(json.dumps(json_obj_recv), encoding='utf-8')) 
				continue

			ContaPalavrasDoArquivo(json_obj_recv)

			# envia mensagem para o cliente
			print('Processamento concluído. Enviado mensagem para o cliente.')
			novoSock.send(bytes(json.dumps(json_obj_recv), encoding='utf-8')) 

		# fecha o socket da conexao
		novoSock.close() 

	# fecha o socket principal
	sock.close() 

IniciaServidor()
