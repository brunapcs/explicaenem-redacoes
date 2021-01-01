import gspread 
import logging

logger = logging.getLogger(__name__)

class CorretoresConf(object): 
    last_tag = "LAST"
    email_col_name = "Email"

    def __init__(self):
        super().__init__()


    def config(self, sheet):
        self.wks = sheet
        self.all_records = sheet.get_all_records()
        self.total = len(self.all_records)
        self.start_index = self.get_start_index()
        self.last_index = 0

    def get_start_index(self): 
        """Gets row index on sheet of last corrector to reveice text.

        Returns:
            start_index: Row index of next corretor to receive a text.
        """ 
        try: 
            cell_corr = self.wks.find(self.last_tag)

        except gspread.exceptions.CellNotFound as ex: 
            logger.error(f'Nao encontrou em Corretores celula marcada como {self.last_tag}: {ex}')

        return cell_corr.row 
        
    
    def update_last_corrector(self):
        """Updates worksheet tagging with {last_tag} the corrector on index
        last_index."""  
           
        self.wks.update_cell(self.start_index, 2, 'X')
        self.wks.update_cell(self.last_index, 2, self.last_tag)    

corretores = CorretoresConf()