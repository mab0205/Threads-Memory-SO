class PageTable:
    """ Implementação da Tabela de Páginas """
    def __init__(self):
        self.table = {}

    def get_frame(self, page_number):
        """ Retorna o frame associado à página ou None se não estiver na memória """
        return self.table.get(page_number, None)

    def update(self, page_number, frame_number):
        """ Atualiza a tabela de páginas """
        self.table[page_number] = frame_number

