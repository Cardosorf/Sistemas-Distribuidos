import os

CAMINHO_DIRETORIO = os.path.join(os.path.dirname(__file__), "Arquivos") # caminho do diretório com os arquivos de texto

def NomeDoArquivoValido(mensagem_json):
	if not mensagem_json["arquivo"] or mensagem_json["arquivo"].isspace():
		mensagem_json["sucesso"]        = False
		mensagem_json["mensagemErro"]   = "Nome do arquivo inválido"
		return False
	else:
		return True

def PegaCaminhoDoArquivo(mensagem_json):
	return os.path.join(CAMINHO_DIRETORIO, mensagem_json["arquivo"])

def CaminhoDoArquivoValido(mensagem_json):
	caminhoArquivo = os.path.join(CAMINHO_DIRETORIO, mensagem_json["arquivo"])
	
	if os.path.isfile(caminhoArquivo):
		return True
	else:
		mensagem_json["sucesso"]        = False
		mensagem_json["mensagemErro"]   = "Arquivo não encontrado."
		return False

def LeArquivo(mensagem_json):
    caminhoArquivo = PegaCaminhoDoArquivo(mensagem_json)
    file           = open(caminhoArquivo, 'r', encoding="utf8")
    
    dados          = file.read()

    file.close()

    return dados