from collections import deque

NUM_FRAMES = 64  # Quantidade de frames físicos
git
class Memory:
    """ 
    Memória RAM (Frames físicos)
    Simula a memória física com substituição de páginas usando LRU ou Segunda Chance 
    """
    def __init__(self, algorithm="LRU"):
        self.frames = {}  # Mapeia frame → página
        self.free_frames = set(range(NUM_FRAMES))  # Frames livres
        self.algorithm = algorithm

        if self.algorithm == "LRU":
            self.usage_order = deque()  # Usado para LRU
            self.reference_bits = None  # Não precisa de referência
        elif self.algorithm == "SC":
            self.reference_bits = {}  # Mapeia frame → bit de referência
            self.usage_order = deque()  # Mantém a ordem das páginas

    def allocate(self, page_number):
        """ Aloca uma página na memória física """
        if self.free_frames:  # Se houver frames livres na memória
            frame = self.free_frames.pop()
        else:  # Memória estiver cheia
            frame = self.replace_memory_page()  # Substituir uma página

        self.frames[frame] = page_number
        if self.algorithm == "LRU":
            self.usage_order.append(frame)  # Atualiza a ordem de uso
        elif self.algorithm == "SC":
            self.reference_bits[frame] = 1  # Marca como referenciada
            self.usage_order.append(frame)  # Mantém a fila de ordem de chegada
        return frame

    def replace_memory_page(self):
        """ 
        Substitui uma página antiga por uma nova, dependendo do caso:
        1. LRU 
        2. SC
        """
        if self.algorithm == "LRU":
            frame = self.usage_order.popleft()  # Remove o mais antigo
        elif self.algorithm == "SC":
            frame = self.alg_memory_sc()  # Executa a lógica de Segunda Chance

        return self.del_frame(frame)  # Remove o frame da memória

    def alg_memory_sc(self):
        """ Algoritmo Segunda Chance para substituição de páginas """
        while True:
            frame = self.usage_order[0]  # Primeiro da fila
            if self.reference_bits.get(frame, 0) == 0:
                break  # Se o bit for 0, pode remover a página
            self.reference_bits[frame] = 0  # Dá uma segunda chance
            self.usage_order.rotate(-1)  # Move para o final da fila
        return frame

    def del_frame(self, frame):
        """ Remove um frame da memória """
        if frame in self.usage_order:
            self.usage_order.remove(frame)  # Remove da ordem de uso
        del self.frames[frame]
        self.free_frames.add(frame)
        return frame
