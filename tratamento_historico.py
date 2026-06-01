import pandas as pd

# =========================
# 1. CONFIGURAÇÃO
# =========================

JOGADOR = "Joao Fonseca"
arquivo_entrada = "joao_fonseca_historico_bruto.xlsx"
arquivo_saida = "joao_fonseca_historico_tratado.xlsx"

# =========================
# 2. CARREGAR BASE BRUTA
# =========================

df = pd.read_excel(arquivo_entrada)

# =========================
# 3. CRIAR COLUNA RESULTADO
# =========================

df["resultado"] = df.apply(
    lambda linha: "VITÓRIA" if linha["winner_name"] == JOGADOR else "DERROTA",
    axis=1
)

# =========================
# 4. CRIAR ADVERSÁRIO
# =========================

df["adversario"] = df.apply(
    lambda linha: linha["loser_name"] if linha["winner_name"] == JOGADOR else linha["winner_name"],
    axis=1
)

# =========================
# 5. CRIAR RANKING DO JOÃO
# =========================

df["ranking_joao"] = df.apply(
    lambda linha: linha["winner_rank"] if linha["winner_name"] == JOGADOR else linha["loser_rank"],
    axis=1
)

# =========================
# 6. CRIAR RANKING DO ADVERSÁRIO
# =========================

df["ranking_adversario"] = df.apply(
    lambda linha: linha["loser_rank"] if linha["winner_name"] == JOGADOR else linha["winner_rank"],
    axis=1
)

# =========================
# 7. CRIAR ANO
# =========================

df["data_torneio"] = pd.to_datetime(
    df["tourney_date"].astype(str),
    format="%Y%m%d",
    errors="coerce"
)

df["ano"] = df["data_torneio"].dt.year

# =========================
# 8. CLASSIFICAR FAIXA DE RANKING
# =========================

def classificar_ranking(ranking):
    if pd.isna(ranking):
        return "Sem ranking"
    elif ranking <= 10:
        return "Top 10"
    elif ranking <= 20:
        return "Top 20"
    elif ranking <= 50:
        return "Top 50"
    elif ranking <= 100:
        return "Top 100"
    else:
        return "Acima de 100"

df["faixa_ranking_adversario"] = df["ranking_adversario"].apply(classificar_ranking)

# =========================
# 9. CLASSIFICAR TIPO DE TORNEIO
# =========================

def classificar_torneio(nivel):
    if nivel == "G":
        return "Grand Slam"
    elif nivel == "M":
        return "Masters 1000"
    elif nivel == "A":
        return "ATP 250/500"
    elif nivel == "D":
        return "Davis Cup"
    elif nivel == "F":
        return "ATP Finals"
    else:
        return "Outro"

df["tipo_torneio"] = df["tourney_level"].apply(classificar_torneio)

# =========================
# 10. ORGANIZAR BASE FINAL
# =========================

base_final = df[
    [
        "data_torneio",
        "ano",
        "tourney_name",
        "tipo_torneio",
        "surface",
        "resultado",
        "adversario",
        "ranking_joao",
        "ranking_adversario",
        "faixa_ranking_adversario",
        "score",
        "round",
        "minutes",
        "winner_name",
        "loser_name"
    ]
].copy()

# =========================
# 11. RENOMEAR COLUNAS
# =========================

base_final = base_final.rename(
    columns={
        "tourney_name": "torneio",
        "surface": "piso",
        "score": "placar",
        "round": "fase",
        "minutes": "duracao_minutos",
        "winner_name": "vencedor",
        "loser_name": "perdedor"
    }
)

# =========================
# 12. ORDENAR POR DATA
# =========================

base_final = base_final.sort_values(
    by="data_torneio",
    ascending=True
)

# =========================
# 13. EXPORTAR
# =========================

base_final.to_excel(arquivo_saida, index=False)

# =========================
# 14. RESUMO NO TERMINAL
# =========================

print("=" * 50)
print("BASE HISTÓRICA TRATADA GERADA")
print("=" * 50)
print(f"Arquivo criado: {arquivo_saida}")
print(f"Total de partidas: {len(base_final)}")
print(f"Primeira data: {base_final['data_torneio'].min().date()}")
print(f"Última data: {base_final['data_torneio'].max().date()}")

print("\nVitórias e derrotas:")
print(base_final["resultado"].value_counts())

print("\nPartidas por ano:")
print(base_final["ano"].value_counts().sort_index())

print("\nPrévia:")
print(base_final.head(10))