from memory import Memory
from page_table import PageTable
from tlb import TLB

# Configurações básicas
PAGE_SIZE = 2**12  # 4 KB

class MMU:
    """ Gerenciador de Memória (MMU) coordenando TLB, tabela de páginas e memória física """
    def __init__(self, algorithm="LRU"):
        self.tlb = TLB(algorithm=algorithm)
        self.page_table = PageTable()
        self.memory = Memory(algorithm=algorithm)
        self.tlb_hits = 0
        self.tlb_miss = 0
        self.page_faults = 0

    def translate_address(self, logical_address):
        """ Traduz um endereço lógico para um endereço físico """
        p = logical_address >> 12 # Obtém o número da página (20 bits mais significativos)
        d = logical_address & 0xFFF  # Obtém o deslocamento Offset dentro da página (12 bits menos significativos)
        
        # Verifica se a página está na TLB (cache de endereços)
        frame_number = self.tlb.search_tlb(page_number=p)  # Busca na TLB
        
        if frame_number is not None:  # Hit -> achou na TLB
            self.tlb_hits += 1
        
        else:  # Nao achou -> Precisa buscar na Tabela de Páginas
            self.tlb_miss += 1
            frame_number = self.page_table.search_table(page_number=p)# A página está carregada na RAM?

            if frame_number is None:  # Nao achou na tabela -> Página não está na RAM
                self.page_faults += 1  
                # Aloca um novo frame na memória (ou substitui uma página)
                frame_number = self.memory.allocate(page_number=p)  
                self.page_table.update(p, frame_number)# Atualiza a Tabela de Páginas
            
            # Atualiza a TLB para futuras referências rápidas
            self.tlb.update(p, frame_number)
    
def run_simulation(trace_file, algorithm="LRU"):
    """ Executa o simulador comparando as políticas LRU e Segunda Chance """
    mmu = MMU(algorithm)

    with open(trace_file, "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) != 2:
                continue
            address, operation = parts
            logical_address = int(address, 16)  # Converte de hexadecimal para inteiro
            mmu.translate_address(logical_address)  # metodo para VERIFICA SE HÁ UM NOVO ENDEREÇO

    # Exibir estatísticas
    print(f"Algoritmo usado: {algorithm}")
    print(f"TLB Hits: {mmu.tlb_hits}")
    print(f"TLB Misses: {mmu.tlb_miss}")
    print(f"Falhas de Paginas - Acesso Disco: {mmu.page_faults}")
    
# Teste com um arquivo de trace
print("sixpack")
run_simulation("sixpack.trace", algorithm="LRU")
run_simulation("sixpack.trace", algorithm="SC")
print("--------------------------------------")

print("bzip")
run_simulation("bzip.trace", algorithm="LRU")
run_simulation("bzip.trace", algorithm="SC")
print("--------------------------------------")

print("gcc")
run_simulation("gcc.trace", algorithm="LRU")
run_simulation("gcc.trace", algorithm="SC")
print("--------------------------------------")

print("swim")
run_simulation("swim.trace", algorithm="LRU")
run_simulation("swim.trace", algorithm="SC")
print("--------------------------------------")
