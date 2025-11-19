from typing import NamedTuple, Optional

# Classe "Medida" para armazenar os dados do arquivo txt


class Medida(NamedTuple):
    tempo: float
    carga: float
    deslocamento: float

# Converte uma linha do txt em um objeto "Medida" (retorna None se for inválida)


def parse_linha(linha: str) -> Optional[Medida]:
    partes = linha.strip().replace(",", ".").split(
        "\t")  # vírgula -> ponto, separa por tab
    if len(partes) == 3:
        try:
            return Medida(float(partes[0]), float(partes[1]), float(partes[2]))
        except ValueError:
            return None
    return None

# Filtro 1: filtra os dados apenas para o intervalo de deslocamento de -3,495 mm a -3,5 mm


def filtro_disp(m: Medida) -> bool:
    return -3.5 <= m.deslocamento <= -3.495

# Filtro 2: filtra os dados com diferença de tempo > 2.1 (considerando um ciclo),
# seleciona apenas a primeira medida de cada bloco onde o tempo difere > 2.1 s do anterior selecionado.


def filtro_tempo(medidas):
    resultado = []
    ultimo = None
    for m in medidas:
        if ultimo is None or m.tempo - ultimo.tempo > 2.1:
            resultado.append(m)
            ultimo = m
    return resultado

# Programa principal


def main():
    # --------------------------Entrada----------------------------------------------------------------------

    # recebe como entrada o arquivo txt de dados brutos gerado pelo software VectorPro após o ensaio cíclico
    with open("D:\códigosVScode\_analise_Dados_altprint\ensaios_Ciclicos\_20perc\_2gap\entrada\_2.txt", "r", encoding="utf-8") as f:
        linhas = f.read().strip().splitlines()

# --------------------------Processamento----------------------------------------------------------------------

    # descarta o cabeçalho do arquivo txt de dados do ensaio cíclico
    linhas_sem_cabecalho = linhas[1:]
    medidas = filter(None, map(parse_linha, linhas_sem_cabecalho))

    # aplica filtro 1
    medidas_filtradas = list(filter(filtro_disp, medidas))

    # aplica filtro 2
    medidas_final = filtro_tempo(medidas_filtradas)

# --------------------------Saída----------------------------------------------------------------------

    # gera como saída um novo arquivo txt com os dados já tratados, sendo a 1º coluna o nº do ciclo e
    # a 2ª coluna a carga no respectivo ciclo
    with open("D:\códigosVScode\_analise_Dados_altprint\ensaios_Ciclicos\_20perc\_2gap\saida\_2.txt", "w", encoding="utf-8") as f_out:

        for m in medidas_final:
            ciclos = m.tempo / 2.1
            tenComp = m.carga / 50
            linha = f"{ciclos:.3f}\t{abs(m.carga):.3f}\n"
           # linha = f"{ciclos:.3f}\t{abs(tenComp):.3f}\n"
            # troca pontos por vírgulas
            linha = linha.replace(".", ",")
            f_out.write(linha)


if __name__ == "__main__":
    main()
