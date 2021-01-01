import os
import gspread 
import logging
import json
import yagmail
from tools.CorretoresConf import corretores
from tools.redacoes import Redacoes

logger = logging.getLogger(__name__)

REDACOES_WORKSHEET_NAME = "Redacoes"
CORRETORES_WORKSHEET_NAME = "Corretores"
yag = yagmail.SMTP(os.environ["EMAIL"], os.environ["SENHA"])

def main(request):

    gc = gspread.service_account(filename="key.json")
    sheet = gc.open_by_key(os.environ["REDACOES_SHEET_PROD"])

    redacoes = Redacoes(sheet.worksheet(REDACOES_WORKSHEET_NAME)) 
    corretores.config(sheet.worksheet(CORRETORES_WORKSHEET_NAME)) 

    envia_email(redacoes, corretores)
    corretores.update_last_corrector() 

    return redacoes.redacoes_novas


def envia_email(red, corretores): 
    """Envia emails com links para redacoes 
    para corretores disponiveis iniciando por aquele que
    recebeu por ultimo.

    Atualiza last_index na lista de corretores.
    """
    index = corretores.start_index

    for redacao in red.redacoes_novas:   

        if index + 1 >= corretores.total: 
            index = 0 
        else:
            index = index + 1

        email_corretor = corretores.all_records[index-2].get(corretores.email_col_name, "Faltando email do corretor")
        red.set_params(redacao)
        mensagem = build_message(red)
        
        try:
            yag.send(email_corretor, 'explicaENEM-Redação para correção', mensagem)
            logger.info(f"Recadao enviada para: {email_corretor}. Id:{red.id}")
            status = 'Enviado para correção'

        except Exception as ex:
            logger.error(ex)
            status = 'Falha no envio'

        red.update_status(red.id, status, email_corretor)

    corretores.last_index = index

def build_message(red): 
    adicional = ''' Boa tarde corretores!
                        Na semana passada alguns emails foram enviados sem o link para os arquivos de redações. 
                        Por isso, reiniciamos o programa de envio/recebimento de redações e estamos reprocessando os casos de erro.
                        Não se preocupe caso a redação abaixo não corresponda a que havia recebido previamente.
                        Por fim, desejamos um feliz natal atrasado para todos! 

                        - Equipe de T.I explicaENEM '''
    mensagem =  adicional + f"\n\nRedação de aluno: {red.email_aluno}" \
                f"\nId: {red.id}" \
                f"\nEnviada na data: {red.data_envio}" \
                f"\nTema: {red.tema}" \
                f"\nArquivos no(s) link(s):{red.link_redacao}" \
                "\nPor favor envie a correção através do formulário: https://forms.gle/cHfFSYxgoY5HhBeDA"
    
    return mensagem


if __name__ == '__main__': 
    main('oi')