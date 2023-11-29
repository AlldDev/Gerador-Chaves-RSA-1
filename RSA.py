import rsa
import os

_N_THREADS = os.cpu_count()

def gerar_key(tam):
    global _N_THREADS

    # GERANDO AS CHAVES | poolsize DEFINE O TANTO DE THREAD PARA GERAR MAIS RÁPIDO
    pubkey, privkey = rsa.newkeys(tam, poolsize=_N_THREADS)

    # TRANSFORMANDO-AS EM ALGO QUE SEJA GRAVAVEL (TYPE BYTES)
    pubkey = pubkey.save_pkcs1()
    privkey = privkey.save_pkcs1()
    ''' NOTA SOBRE PKCS1
    pkcs1 (Public Key Cryptography Standard #1) é um conjunto de padrões
    que descrevem algoritmos criptográficos para chave pública.
    esse padrão não oferece segurança ao arquivo gerado, por isso
    seria interessante adicionar uma criptografia no arquivo gerado...
    talvez uma chave simétrica onde ela fica dentro do código do servidor ?'''
    print(f'Chave Publica no Formato para salvar: {pubkey}\n'
          f'Chave Privada no Formato para salvar: {privkey}')

    with open('pubkey.pem', 'wb') as arq:
        arq.write(pubkey)
        arq.close()
    with open('privkey.pem', 'wb') as arq:
        arq.write(privkey)
        arq.close()

if __name__ == "__main__":
    #gerar_key(512)

    msg = 'Essa mensagem deverá ser criptografada! Ou não...'
    print(f'Mensagem Normal: {msg}')

    # LENDO OS ARQUIVOS DAS CHAVES E CARREGANDO-OS DE VOLTA PARA RSA
    with open('RSA-KEY-2/public_rsa.pem', 'rb') as arq:
        public_key = arq.read()
        public_key = rsa.PublicKey.load_pkcs1(public_key)
        arq.close()
    with open('RSA-KEY-2/private_rsa.pem', 'rb') as arq:
        private_key = arq.read()
        private_key = rsa.PrivateKey.load_pkcs1(private_key)
        arq.close()

    msg_crypt = rsa.encrypt((msg.encode()), public_key)
    print(f'Mensagem Criptografada: {msg_crypt}')

    msg_decrypt = rsa.decrypt(msg_crypt, private_key)
    print(f'Mensagem Descriptografada: {msg_decrypt.decode()}')
