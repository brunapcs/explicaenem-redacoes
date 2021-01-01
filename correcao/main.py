import os
from datetime import datetime, timedelta
import gspread 
import logging
import argparse
import json
from datetime import datetime

import yagmail

logger = logging.getLogger(__name__)


def envia_email(correcoes, redacoes_wks, correcoes_wks): 

    """Recebe lista de dicts de correçoes.

    Envia emails para alunos Atualiza planilha de redações com o Status
    "Correção recebida". Atualiza planilha de correções com o Status
    "Enviado".
    """

    enviadas = []
    yag = yagmail.SMTP(os.environ["EMAIL"], os.environ["SENHA"])
    
    for correcao in correcoes:   
        
        print(correcao)

        now = datetime.now()
        data_envio = now.strftime('%d/%m/%y %H:%M:%S') 
        email_aluno = correcao.get('Email do aluno')
        nome_corretor = correcao.get('Nome')
        url_correcao = correcao.get('Anexe o arquivo com a correção')
        tema = correcao.get('Tema da Redação') 
        id_redacao = correcao.get("id da redação")

        mensagem = f'Olá Aluno! Aqui está a correção de sua redação! \
                    \n Corretor: {nome_corretor} \
                    \n Link para arquivos com correção: {url_correcao} \
                    \n Tema da redação: {tema} '
                 
        try:
            yag.send(email_aluno, 'explicaENEM- Correção de redação', mensagem)
            enviadas.append(email_aluno)

        except Exception as ex:
            logger.error(f'Problemas ao mandar email para:{email_aluno}. EX:{ex}')

        if atualiza_status_redacoes(redacoes_wks, data_envio, id_redacao): 
            status_corr = 'Enviado'
        else: 
            status_corr = 'Problema no ID'
        
        atualiza_status_correcoes(correcoes_wks, id_redacao, status_corr)

    return enviadas


def atualiza_status_redacoes(redacoes_wks, data_envio, id_redacao):
         
    try:  
        cell_red = redacoes_wks.find(id_redacao)
        redacoes_wks.update_cell(cell_red.row, cell_red.col+1, 'Correção recebida')
        redacoes_wks.update_cell(cell_red.row, cell_red.col+3, data_envio)
        
        return True 
    
    except gspread.exceptions.CellNotFound as ex: 
        logger.error(f'Nao encontrou em Redacoes celula com id: {ex}')
        
    except Exception as ex: 
        logger.error(f'Problemas ao atualizar Status em "Redações". Ex:{ex}')

    return False
 
def atualiza_status_correcoes(correcoes_wks, id_redacao, status): 

    try:    
        cell_cor = correcoes_wks.find(id_redacao)
        correcoes_wks.update_cell(cell_cor.row, cell_cor.col+1, status)

    except gspread.exceptions.CellNotFound as ex: 
        logger.error(f'Nao encontrou em Correcoes celula com id: {ex}')
        
    except Exception as ex: 
        logger.error(f'Problemas ao atualizar Status em "Correcoes". Ex:{ex}')
        correcoes_wks.update_cell(cell_cor.row, cell_cor.col +1, 'Problema atualizando status')
        

def main(request):

    gc = gspread.service_account(filename="key.json")
    sh = gc.open_by_key(os.environ["CORRECOES_SHEET_PROD"]) 
    red_sh = gc.open_by_key(os.environ["REDACOES_SHEET_PROD"])

    correcoes_wks = sh.worksheet("Correcoes")
    redacoes_wks = red_sh.worksheet("Redacoes")
   
    data_correcoes = correcoes_wks.get_all_records()
    correcoes_novas = check_correcoes(data_correcoes)    

    correcoes_enviadas = envia_email(correcoes_novas, redacoes_wks, correcoes_wks)

    resp = json.dumps(correcoes_enviadas)
    return resp

def check_correcoes(data): 

    novas = []
    
    for correcao in data: 
        status = correcao.get('Status')
        if status == 'Pendente' or status == '': 
            novas.append(correcao)

    return novas


if __name__ == '__main__': 
    main('test')