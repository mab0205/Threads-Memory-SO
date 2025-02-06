from collections import deque

TLB_SIZE = 16  # Tamanho da TLB

class TLB: #(Translation Lookaside Buffer)
    """ 
    Cache de mapeamentos
    Implementação da TLB com suporte a LRU e Segunda Chance 
    """
    def __init__(self, size=TLB_SIZE, algorithm ="LRU"):
        self.size = size
        self.algorithm  = algorithm 
        self.cache = {}  # Mapeia página → frame
        self.order = deque()  # Para controlar LRU e FIFO
        self.flag_bits = {} if algorithm  == "SC" else None  # SC bit de referencia

    def search_tlb(self, page_number):
        """ Verifica se a página está na TLB """
        frame = self.cache.get(page_number, None)

        if frame is not None and self.algorithm  == "SC":
            self.flag_bits[page_number] = 1  # Marca como referencia

        elif frame is not None and self.algorithm  == "LRU":
            self.order.remove(page_number)
            self.order.append(page_number)  # Atualiza a ordem

        return frame

    def update(self, page_number, frame_number):
        """ Atualiza a TLB, substituindo páginas se necessário """

        if page_number in self.cache:
            self.order.remove(page_number)  # Remove se já existir
        elif len(self.cache) >= self.size:
            self.replace_tlb_entry()  # Substituir uma entrada

        self.cache[page_number] = frame_number
        self.order.append(page_number)

        if self.algorithm  == "SC":
            self.flag_bits[page_number] = 1  # Define bit de referência

    def replace_tlb_entry(self):
        """ Remove uma entrada da TLB """
        if self.algorithm  == "LRU":
            old_page = self.order.popleft()  # Remove a mais antiga
            
        elif self.algorithm  == "SC": 
            old_page = self.alg_sc()#ALGORITMO SEGUNDA CHANCE

        self.pag_exists(old_page) #página existe
    
    def alg_sc(self):
        """
        Se o bit for 0, a página é removida
        Se o bit for 1, o bit é zerado e a página é movida para o final da fila (segunda chance)
        O processo se repete até encontrar uma página com bit 0.
        """
        while True:
                old_page = self.order[0]  #Primeiro da fila
                if old_page not in self.cache:
                    self.order.popleft()  # Remover inconsistência
                    continue  #próxima iteração

                if self.flag_bits.get(old_page, 0) == 0:
                    break
                else: #Se bit =1  
                    self.flag_bits[old_page] = 0  # Dá uma segunda chance
                    self.order.rotate(-1)  # Move para o final
        return old_page

    def pag_exists(self, old_page):
        """ Garantir que a página existe antes de removê-la """

        if old_page in self.cache:
            del self.cache[old_page]
        if old_page in self.order:
            self.order.remove(old_page)
        if self.algorithm  == "SC" and old_page in self.flag_bits:
            del self.flag_bits[old_page]


        
