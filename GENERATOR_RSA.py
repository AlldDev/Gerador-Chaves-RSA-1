import rsa
import os
import shutil
import threading

def menu():
    os.system('cls' or 'clear')
    print('''
╔═══════════════════════════════════════════════════════════════════════════╗
║  ██████╗ ███████╗██████╗  █████╗ ██████╗  ██████╗ ██████╗                 ║
║ ██╔════╝ ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██╔══██╗                ║
║ ██║  ███╗█████╗  ██████╔╝███████║██║  ██║██║   ██║██████╔╝                ║
║ ██║   ██║██╔══╝  ██╔══██╗██╔══██║██║  ██║██║   ██║██╔══██╗                ║
║ ╚██████╔╝███████╗██║  ██║██║  ██║██████╔╝╚██████╔╝██║  ██║                ║
║  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝                ║                 
║             ██████╗ ███████╗ █████╗        ██╗                            ║
║             ██╔══██╗██╔════╝██╔══██╗      ███║                            ║
║             ██████╔╝███████╗███████║█████╗╚██║                            ║
║             ██╔══██╗╚════██║██╔══██║╚════╝ ██║                            ║
║             ██║  ██║███████║██║  ██║       ██║                            ║
║             ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝       ╚═╝                            ║
║ command: /gerar [qtd_keys] [tam_keys] [sob-escrever existentes -s ou -n)] ║
║ example: /gerar 10 512 -s                                                 ║
╚═══════════════════════════════════════════════════════════════════════════╝''')
    return input('Digite: ')

def gerar_key(t_key, p_dir):
    public_key_dir = os.path.join(p_dir, 'public_rsa.pem')
    private_key_dir = os.path.join(p_dir, 'private_rsa.pem')

    try:
        public_rsa, private_rsa = rsa.newkeys(t_key, poolsize=2)
        public_rsa = public_rsa.save_pkcs1()
        private_rsa = private_rsa.save_pkcs1()
    except:
        print(f'Erro ao Gerar Chave.\n {error}')

    try:
        with open(public_key_dir, 'wb') as arq:
            arq.write(public_rsa)
            arq.close()
        with open(private_key_dir, 'wb') as arq:
            arq.write(private_rsa)
            arq.close()
    except:
        print(f'Erro ao criar arquivos no diretório: {public_key_dir}')

if __name__ == "__main__":
    th = []
    protocol = None
    n_keys = None
    t_keys = None
    s_thread = None
    name_dir = 'RSA-KEY-'
    path_dir = None

    entry = menu()
    _, n_keys, t_key, sobescrever = entry.split(' ', maxsplit=3)
    n_keys = int(n_keys)
    t_key = int(t_key)

    match sobescrever:
        case '-s':
            sobescrever = True
        case '-n':
            sobescrever = False

    for i in range(0, n_keys):
        name_dir_key = name_dir + str(i)

        try:
            os.mkdir(name_dir_key)
            th.append(threading.Thread(target=gerar_key, args=(t_key, name_dir_key)))
            print(f'Criando {name_dir_key}')
        except OSError as error:
            if sobescrever == True:
                shutil.rmtree(name_dir_key)
                os.mkdir(name_dir_key)
                th.append(threading.Thread(target=gerar_key, args=(t_key, name_dir_key)))
                print(f'Sobescrevendo {name_dir_key}')
                pass
            elif sobescrever == False:
                print(f'Ignorando {name_dir_key}')
                pass

        # th.append(threading.Thread(target=gerar_key, args=(t_key, name_dir_key)))
        # th[i].start()

    for i in range(0, len(th)):
        th[i].start()

    for i in range(0, len(th)):
        th[i].join()
        print(f'Aguardando {i}')

    # sub_menu(len(th))