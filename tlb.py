from collections import deque

TLB_SIZE = 64  # Tamanho da TLB

class TLB:
    """ Implementação de um TLB (cache de páginas) """
    def __init__(self, size=TLB_SIZE):
        self.cache = {}  # Mapeamento página → frame
        self.order = deque()  # Controle de ordem (FIFO)
        self.size = size

    def get(self, page_number):
        """ Verifica se a página está na TLB """
        return self.cache.get(page_number, None)

    def update(self, page_number, frame_number):
        """ Atualiza a TLB com um novo mapeamento """
        if page_number in self.cache:
            self.order.remove(page_number)  # Remove a página se já existir
        elif len(self.cache) >= self.size:
            old_page = self.order.popleft()  # Remove a mais antiga (FIFO)
            del self.cache[old_page]

        self.cache[page_number] = frame_number
        self.order.append(page_number)
        
