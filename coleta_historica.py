import pandas as pd

# =========================
# CONFIGURAÇÃO
# =========================

JOGADOR = "Joao Fonseca"

anos = [
    2023,
    2024,
    2025
]

# =========================
# COLETA
# =========================

lista_dfs = []

for ano in anos:

    print(f"Baixando {ano}...")

    url = (
        f"https://raw.githubusercontent.com/"
        f"JeffSackmann/tennis_atp/master/"
        f"atp_matches_{ano}.csv"
    )

    df = pd.read_csv(url)

    lista_dfs.append(df)

# =========================
# UNIR TUDO
# =========================

base_completa = pd.concat(
    lista_dfs,
    ignore_index=True
)

print()
print(f"Total de partidas ATP: {len(base_completa):,}")

# =========================
# FILTRAR JOÃO
# =========================

joao = base_completa[
    (base_completa["winner_name"] == JOGADOR)
    |
    (base_completa["loser_name"] == JOGADOR)
].copy()

print(f"Partidas do João: {len(joao)}")

# =========================
# EXPORTAR
# =========================

joao.to_excel(
    "joao_fonseca_historico_bruto.xlsx",
    index=False
)

print()
print("Arquivo criado com sucesso!")