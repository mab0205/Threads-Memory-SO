from collections import deque
import random

NUM_FRAMES = 64  # Quantidade de frames físicos

class Memory:
    """ Simula a memória física com substituição de páginas """
    def __init__(self, policy="LRU"):
        self.frames = {}  # Mapeia frame → página
        self.free_frames = set(range(NUM_FRAMES))  # Conjunto de frames livres
        self.policy = policy
        self.reference_bits = {} if policy == "SC" else None  # Usado na Segunda Chance
        self.usage_order = deque() if policy == "LRU" else None  # Usado na LRU

    def allocate(self, page_number):
        """ Aloca uma página na memória física """
        if self.free_frames:
            frame = self.free_frames.pop()
        else:
            frame = self.evict_page()  # Precisa substituir uma página

        self.frames[frame] = page_number
        if self.policy == "LRU":
            self.usage_order.append(frame)
        elif self.policy == "SC":
            self.reference_bits[frame] = 1  # Define bit de referência para Segunda Chance
        return frame

    def evict_page(self):
        """ Substitui uma página na memória conforme a política """
        if self.policy == "LRU":
            frame = self.usage_order.popleft()
        elif self.policy == "SC":
            while True:
                frame, page = random.choice(list(self.frames.items()))
                if self.reference_bits[frame] == 0:
                    break
                self.reference_bits[frame] = 0  # Dá uma segunda chance
            del self.reference_bits[frame]
        del self.frames[frame]
        self.free_frames.add(frame)
        return frame