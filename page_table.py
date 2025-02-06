class PageTable:
    """ Implementação da Tabela de Páginas """
    def __init__(self):
        self.table = {}

    def search_table(self, page_number):
        """ 1. Sim, retorna o frame e atualiza TLB
            2. Caso contrario None se não estiver na memória """
        return self.table.get(page_number, None)

    def update(self, page_number, frame_number):
        """ Atualiza a tabela de páginas """
        self.table[page_number] = frame_number

