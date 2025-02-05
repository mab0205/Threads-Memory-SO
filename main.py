from memory import Memory
from page_table import  PageTable
from tlb import TLB

# Configurações básicas
PAGE_SIZE = 2**12  # 4 KB

class MMU_handler:
    """ Gerenciador de Memória (MMU) que coordena TLB, tabela de páginas e memória """
    def __init__(self, policy="LRU"):
        self.tlb = TLB()
        self.page_table = PageTable()
        self.memory = Memory(policy)
        self.tlb_hits = 0
        self.tlb_misses = 0
        self.page_faults = 0
        self.disk_accesses = 0  # Contabiliza acessos ao disco

    def translate_address(self, logical_address):
        """ Traduz um endereço lógico para físico """
        page_number = logical_address >> 12  # Obtém os 20 bits da página
        offset = logical_address & 0xFFF  # Obtém os 12 bits de deslocamento

        # 1. Verifica se a página está na TLB
        frame_number = self.tlb.get(page_number)
        if frame_number is not None:
            self.tlb_hits += 1
        else:
            self.tlb_misses += 1
            frame_number = self.page_table.get_frame(page_number)

            if frame_number is None:
                # 2. Page Fault: carregar página na memória
                self.page_faults += 1
                self.disk_accesses += 1  # Contabiliza acesso ao disco
                frame_number = self.memory.allocate(page_number)
                self.page_table.update(page_number, frame_number)

            # Atualiza a TLB
            self.tlb.update(page_number, frame_number)

        # Se for Segunda Chance, atualiza bit de referência
        if self.memory.policy == "SC":
            self.memory.reference_bits[frame_number] = 1
        # Se for LRU, atualiza ordem de uso
        elif self.memory.policy == "LRU":
            if frame_number in self.memory.usage_order:
                self.memory.usage_order.remove(frame_number)
            self.memory.usage_order.append(frame_number)

        # Endereço físico = (frame * tamanho da página) + offset
        return (frame_number * PAGE_SIZE) + offset
    
def run_simulation(trace_file, policy="LRU"):
    """ Executa o simulador lendo um arquivo de trace """
    mmu = MMU_handler(policy)

    with open(trace_file, "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) != 2:
                continue
            address, operation = parts
            logical_address = int(address, 16)  # Converte de hexadecimal para inteiro
            mmu.translate_address(logical_address)

    # Exibir estatísticas
    print(f"Política: {policy}")
    print(f"TLB Hits: {mmu.tlb_hits}")
    print(f"TLB Misses: {mmu.tlb_misses}")
    print(f"Page Faults: {mmu.page_faults}")
    print(f"Acessos ao disco: {mmu.disk_accesses}")

# Teste com um arquivo de trace
print("sixpack")
run_simulation("sixpack.trace", policy="LRU")
run_simulation("sixpack.trace", policy="SC")

print("bzip")
run_simulation("bzip.trace", policy="LRU")
run_simulation("bzip.trace", policy="SC")

print("gcc")
run_simulation("gcc.trace", policy="LRU")
run_simulation("gcc.trace", policy="SC")

print("swim")
run_simulation("swim.trace", policy="LRU")
run_simulation("swim.trace", policy="SC")
