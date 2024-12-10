import asyncio
import random


# Gera números aleatórios até alguém vencer ou atingir o limite
async def gerador(fila_numeros, jogo_terminado):
    numeros_sorteados = set()
    for _ in range(1000):  # XLimit = 1000
        # Verifica se o jogo já terminou
        if jogo_terminado.is_set():
            break

        numero = random.randint(0, 100)
        if numero not in numeros_sorteados:
            numeros_sorteados.add(numero)
            await fila_numeros.put(numero)
            await asyncio.sleep(0.1)

    # Sinaliza fim para o narrador
    await fila_numeros.put(None)

#Anuncia números até alguém vencer ou acabarem os números
async def narrador(fila_numeros, jogadores, jogo_terminado):
    while True:
        numero = await fila_numeros.get()
        if numero is None or jogo_terminado.is_set():
            # Sinaliza fim para os jogadores
            for j in jogadores:
                await j.fila.put(None)
            break

        print(f"\nNumber is {numero}")
        for j in jogadores:
            await j.fila.put(numero)


class Jogador:
    def __init__(self, nome, cartela):
        self.nome = nome
        self.cartela = set(cartela)
        self.marcados = set()
        self.fila = asyncio.Queue()

    async def jogar(self, jogo_terminado):
        while True:
            numero = await self.fila.get()
            if numero is None:
                return False

            if numero in self.cartela:
                self.marcados.add(numero)

            print(f"{self.nome} {numero} {list(self.cartela)} {len(self.marcados)}")

            if self.cartela == self.marcados:
                print(f"{self.nome} is the WINNER {self.cartela} {self.marcados}")
                # Sinaliza que o jogo terminou
                jogo_terminado.set()
                return True

            # Verifica se alguém já ganhou
            if jogo_terminado.is_set():
                return False


async def main():
    # Configuração inicial
    jogadores = [
        Jogador("player-1", [5, 10, 48, 55]),
        Jogador("player-2", [8, 46, 80, 99]),
        Jogador("player-3", [17, 29, 78, 95])
    ]

    # Cria fila de números e evento de término
    fila_numeros = asyncio.Queue()
    jogo_terminado = asyncio.Event()

    # Inicia tarefas
    tarefas = [
        asyncio.create_task(gerador(fila_numeros, jogo_terminado)),
        asyncio.create_task(narrador(fila_numeros, jogadores, jogo_terminado)),
        *[asyncio.create_task(j.jogar(jogo_terminado)) for j in jogadores]
    ]

    # Aguarda até alguem ganhar
    await asyncio.gather(*tarefas)

    if jogo_terminado.is_set():
        print("Game is over")
    else:
        print("No winner after 1000 numbers")


if __name__ == "__main__":
    random.seed(42)  # Seed para reprodução
    asyncio.run(main())