import pandas as pd

# =========================
# 1. CONFIGURAÇÃO
# =========================

JOGADOR = "Joao Fonseca"

url = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2025.csv"

# =========================
# 2. CARREGAR BASE
# =========================

df = pd.read_csv(url)

# =========================
# 3. FILTRAR PARTIDAS DO JOÃO
# =========================

joao = df[
    (df["winner_name"] == JOGADOR) |
    (df["loser_name"] == JOGADOR)
].copy()

# =========================
# 4. CRIAR COLUNA RESULTADO
# =========================

joao["resultado_joao"] = joao.apply(
    lambda linha: "VITÓRIA" if linha["winner_name"] == JOGADOR else "DERROTA",
    axis=1
)

# =========================
# 5. CRIAR COLUNA ADVERSÁRIO
# =========================

joao["adversario"] = joao.apply(
    lambda linha: linha["loser_name"] if linha["winner_name"] == JOGADOR else linha["winner_name"],
    axis=1
)

# =========================
# 6. CRIAR RANKING DO JOÃO
# =========================

joao["ranking_joao"] = joao.apply(
    lambda linha: linha["winner_rank"] if linha["winner_name"] == JOGADOR else linha["loser_rank"],
    axis=1
)

# =========================
# 7. CRIAR RANKING DO ADVERSÁRIO
# =========================

joao["ranking_adversario"] = joao.apply(
    lambda linha: linha["loser_rank"] if linha["winner_name"] == JOGADOR else linha["winner_rank"],
    axis=1
)

# =========================
# 8. ORGANIZAR BASE FINAL
# =========================

resultado = joao[
    [
        "tourney_date",
        "tourney_name",
        "surface",
        "resultado_joao",
        "adversario",
        "ranking_joao",
        "ranking_adversario",
        "score",
        "round",
        "minutes"
    ]
].copy()

# =========================
# 9. RENOMEAR COLUNAS
# =========================

resultado = resultado.rename(
    columns={
        "tourney_date": "data_torneio",
        "tourney_name": "torneio",
        "surface": "piso",
        "resultado_joao": "resultado",
        "adversario": "adversario",
        "ranking_joao": "ranking_joao",
        "ranking_adversario": "ranking_adversario",
        "score": "placar",
        "round": "fase",
        "minutes": "duracao_minutos"
    }
)

# =========================
# 10. AJUSTAR DATA
# =========================

resultado["data_torneio"] = pd.to_datetime(
    resultado["data_torneio"].astype(str),
    format="%Y%m%d"
)

# =========================
# 11. EXPORTAR PARA EXCEL
# =========================

nome_arquivo = "joao_fonseca_partidas_tratado.xlsx"

resultado.to_excel(nome_arquivo, index=False)

# =========================
# 12. RESUMO NO TERMINAL
# =========================

print("Arquivo criado com sucesso!")
print(f"Nome do arquivo: {nome_arquivo}")
print(f"Total de partidas encontradas: {len(resultado)}")
print()
print(resultado.head(10))