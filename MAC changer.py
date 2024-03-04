#!/usr/sbin/env python3

import subprocess #usada para executar comandos externos do sistema operacional pelo Python
import random # usado para gerar números aleatórios.
import re
import getpass #solicita uma senha ao usuário

def get_random_mac():
    """
    Gera um endereço MAC aleatório.
    """

    #3 primeiros digitos fixos e os outros 3 aleatórios
    mac = [ 0x00, 0x16, 0x3e,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff) ]

    #Pega a lista "mac" de numeros hexadecimais e transforma em uma string separada por ":" e retorna esses valores
    return ':'.join(map(lambda x: "%02x" % x, mac))
'''
lambda x: "%02x" % x: Esta é uma função lambda que recebe um argumento x e retorna 
"%02x" % x, ou seja, o valor de x formatado como uma string hexadecimal de dois dígitos.

map(lambda x: "%02x" % x, mac): A função map aplica a função lambda a cada elemento da lista mac. 
Ou seja, para cada elemento x em mac, a função lambda é chamada para formatá-lo como uma string 
hexadecimal de dois dígitos. Isso resulta em uma lista de strings formatadas contendo os 
valores hexadecimais de cada elemento de mac.

':'.join(...): Finalmente, ':'.join() é usado para juntar todas as 
strings formatadas separadas por ':', criando assim uma única string que representa 
o endereço MAC no formato comum (por exemplo, "00:16:3e:2a:5b:8c").
'''

def change_mac(interface, novo_mac, password):
    """
    Altera o endereço MAC da interface de rede especificada.
    """
    # Monta o comando para alterar o MAC
    comando = f"sudo ifconfig {interface} down && sudo ifconfig {interface} hw ether {novo_mac} && sudo ifconfig {interface} up"


    subprocess.call('echo {} | sudo -S {}'.format(password, comando), shell=True)
    # echo {} vai conter a senha que vai para a entrada padrão onde vai ser lida pelo sudo -S {} que vai ter dentro dele o comando que foi escrito
    '''
      ^^^^^^ Esta linha executa o comando usando subprocess.call(), que é usado para chamar processos externos. 
       Ele usa sudo para obter permissões de superusuário e executa o comando criado anteriormente.
    '''

def main():
    interface = input("Digite o nome da interface de rede (ex: eth0, wlan0): ")
    mac_option = input("Deseja um MAC aleatório? (S/N): ").upper()

    if mac_option == 'S':
        new_mac = get_random_mac()
    else:
        new_mac = input("Digite o novo MAC desejado (formato xx:xx:xx:xx:xx:xx): ")

    # Verifica se o formato do MAC é válido
    if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', new_mac):
        '''
        ^  indica o início da string.
        
        ([0-9A-Fa-f]{2}[:-]){5} significa que espera-se um grupo de 5 conjuntos de 2 caracteres. 
        Estes caracteres podem ser dígitos (0-9), letras maiúsculas (A-F) ou minúsculas (a-f).
        
        [0-9A-Fa-f] significa qualquer caractere que seja um dígito ou uma letra de A a F, seja maiúscula ou minúscula.
        
        {2} indica que esperamos exatamente dois desses caracteres consecutivos.
        
        [:-] significa que esperamos que entre cada par de dois caracteres possa haver um dos seguintes símbolos: 
        dois pontos : ou um hífen -.
        
        {5} significa que esperamos que esse padrão de dois caracteres seguido de um dos símbolos (: ou -) 
        se repita exatamente 5 vezes.
        
        
        ([0-9A-Fa-f]{2}) significa que esperamos outro grupo de dois caracteres, sem o hífen ou dois pontos dessa vez.
        
        $ indica o final da string.
        '''
        print("Formato de MAC inválido.")
        return

    password = getpass.getpass("Digite a senha do sudo: ")

    change_mac(interface, new_mac, password)
    print("Endereço MAC alterado com sucesso para", new_mac)

if __name__ == "__main__":
    main()
