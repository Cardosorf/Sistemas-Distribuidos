# Aluno: Rafael Pais Cardoso
# DRE: 116140788
# Atividade: Lab 1 - Servidor de echo
# Lado Ativo

import socket

HOST                    = 'localhost' # maquina onde esta o par passivo
PORTA                   = 5000        # porta que o par passivo esta escutando
CLOSE_CONNECTION_CODE   = 'END'

# cria socket
sock                    = socket.socket() # default: socket.AF_INET, socket.SOCK_STREAM 

# conecta-se com o par passivo
sock.connect((HOST, PORTA)) 

print('Conectado ao servidor de echo com sucesso.')
print('Envie mensagens ao servidor de echo e o mesmo as reenviará de volta.')
print('Caso não queira mais mandar mensagens para o servidor de echo, digite \'END\' (sem aspas).')

while(True):

    inputMessage = str(input("Digite uma mensagem: "))
    
    if (inputMessage == CLOSE_CONNECTION_CODE):
        break

    # envia uma mensagem para o par conectado
    sock.send(bytes(inputMessage, encoding='utf-8'))

    # espera a resposta do par conectado (chamada pode ser BLOQUEANTE)
    receivedMessage = sock.recv(1024) # argumento indica a qtde maxima de bytes da mensagem

    # imprime a mensagem recebida
    print('Echo:', str(receivedMessage, encoding='utf-8'))

# encerra a conexao
sock.close() 
