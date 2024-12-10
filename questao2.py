import concurrent.futures
import threading
import time


db_lock = threading.Lock()

# Simulação banco de dados
BancoNoSQL = {
    1: ("Anna Luyza", 7.5),
    2: ("Roberto Tambasco", 8.0),
    3: ("Juliane Gomes", 9.0),
    4: ("Carolina Costa", 6.5),
    5: ("Giullia Fettuccine", 8.5)
}


def get_record_by_id(matricula):
    """Simula consulta ao banco com latência de 3 segundos"""
    time.sleep(3)  # Simula latência de rede
    with db_lock:
        return matricula, BancoNoSQL.get(matricula)


class get_all_records(threading.Thread):
    """Thread dedicada para consulta completa do banco"""

    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()
        self.resultado = None

    def run(self):
        """Simula consulta de todos os registros com latência de 30 segundos
        Utilizei essa função dessa forma para permitir o cancelamento da thread sem precisar
        esperar os 30 segundos que seriam necessários caso usasse time.sleep(30)
        """
        for i in range(30):
            if self._stop_event.is_set():
                return
            time.sleep(1)

        with db_lock:
            self.resultado = BancoNoSQL.copy()

    def stop(self):
        """Permite cancelamento da thread"""
        self._stop_event.set()


def main():
    print("Iniciando consultas concorrentes...")
    inicio = time.time()

    # Realiza 5 consultas concorrentes usando ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        matriculas = [1, 2, 3, 4, 5]
        resultados = list(executor.map(get_record_by_id, matriculas))

    # Processa e mostra resultados
    notas = []
    for matricula, (nome, nota) in resultados:
        print(f"Matrícula: {matricula}, Nome: {nome}, Nota: {nota}")
        notas.append(nota)

    fim = time.time()
    print(f"\nTempo total das consultas: {fim - inicio:.2f} segundos")
    print(f"Nota média: {sum(notas) / len(notas):.2f}")

    # Inicia consulta completa em thread separada
    print("\nIniciando consulta completa...")
    consulta_todos = get_all_records()
    consulta_todos.start()

    # Enquanto a consulta completa roda, faz uma consulta individual
    print("Realizando consulta individual...")
    mat, (nome, nota) = get_record_by_id(1)
    print(f"Resultado consulta individual - Matrícula: {mat}, Nome: {nome}, Nota: {nota}")

    # Cancela a consulta completa
    consulta_todos.stop()
    consulta_todos.join()
    print("get_all_records() foi cancelada")


if __name__ == "__main__":
    main()