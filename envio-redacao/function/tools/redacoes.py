import gspread
import logging

logger = logging.getLogger(__name__)

class Redacoes(object): 
    header_email = 'Endereço de e-mail'
    header_link_redacao = 'Envie o(s) arquivo(s) com sua redação'
    header_data_envio = 'Carimbo de data/hora'
    header_tema = 'Sua redação é sobre qual tema?' 
    header_id = 'id'
    header_status = 'Status'
    NEW_TEXT_STATUS = 'Pendente'

    def __init__(self, wks):
       self.email_aluno = ""
       self.link_redacao = "" 
       self.data_envio  = "" 
       self.tema = "" 
       self.id = "" 
       self.wks = wks
       self.data_redacoes = wks.get_all_records()
       self.redacoes_novas = self.check_redacoes_status() 
    
    def check_redacoes_status(self): 
        """Retrieves from worksheet the information of all texts not sent to
        correction.

        Returns:
            novas_redacoes: array of dicts containing the information of texts that were
            not yet sent to correction
        """ 
        novas_redacoes = []
        
        for redacao in self.data_redacoes: 
            status = redacao.get(self.header_status)
            if status == self.NEW_TEXT_STATUS or '': 
                novas_redacoes.append(redacao)

        return novas_redacoes
    
    def update_status(self, id, status, email_corretor):
        """Updates a text status and adds the email info of designated
        corrector.""" 
        try: 
            cell = self.wks.find(id)
            self.wks.update_cell(cell.row, cell.col +1, status)
            self.wks.update_cell(cell.row, cell.col +2 , email_corretor)

        except gspread.exceptions.CellNotFound as ex: 
            logger.error(f'Nao encontrou em Redacoes celula com id {id}. Ex: {ex}')

    
    def set_params(self, redacao):
        """Receives a dict containing information about the text and populates
        parameters according with the matching headers.""" 
        self.email_aluno = redacao.get(self.header_email)
        self.link_redacao = redacao.get(self.header_link_redacao)
        self.data_envio = redacao.get(self.header_data_envio)
        self.tema = redacao.get(self.header_tema) 
        self.id = redacao.get(self.header_id)
        