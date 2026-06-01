import pandas as pd

# =========================
# 1. CARREGAR PLANILHA
# =========================

arquivo = "joao_fonseca_partidas_tratado.xlsx"

df = pd.read_excel(arquivo)

# =========================
# 2. RESUMO GERAL
# =========================

total_partidas = len(df)
total_vitorias = (df["resultado"] == "VITÓRIA").sum()
total_derrotas = (df["resultado"] == "DERROTA").sum()

aproveitamento = (total_vitorias / total_partidas) * 100

print("=" * 40)
print("RESUMO JOÃO FONSECA")
print("=" * 40)
print(f"Total de partidas: {total_partidas}")
print(f"Vitórias: {total_vitorias}")
print(f"Derrotas: {total_derrotas}")
print(f"Aproveitamento: {aproveitamento:.2f}%")

# =========================
# 3. ANÁLISE POR PISO
# =========================

print("\n" + "=" * 40)
print("DESEMPENHO POR PISO")
print("=" * 40)

analise_piso = (
    df.groupby(["piso", "resultado"])
    .size()
    .unstack(fill_value=0)
)

analise_piso["Total"] = analise_piso.sum(axis=1)
analise_piso["Aproveitamento_%"] = (
    analise_piso.get("VITÓRIA", 0) / analise_piso["Total"] * 100
).round(2)

print(analise_piso)

# =========================
# 4. CRIAR FAIXA DE RANKING
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
# 5. ANÁLISE POR FAIXA DE RANKING
# =========================

print("\n" + "=" * 40)
print("DESEMPENHO POR FAIXA DE RANKING DO ADVERSÁRIO")
print("=" * 40)

analise_ranking = (
    df.groupby(["faixa_ranking_adversario", "resultado"])
    .size()
    .unstack(fill_value=0)
)

analise_ranking["Total"] = analise_ranking.sum(axis=1)
analise_ranking["Aproveitamento_%"] = (
    analise_ranking.get("VITÓRIA", 0) / analise_ranking["Total"] * 100
).round(2)

ordem_faixas = ["Top 10", "Top 20", "Top 50", "Top 100", "Acima de 100", "Sem ranking"]
analise_ranking = analise_ranking.reindex(ordem_faixas).dropna(how="all")

print(analise_ranking)

# =========================
# 6. ADVERSÁRIOS MAIS FORTES VENCIDOS
# =========================

print("\n" + "=" * 40)
print("MELHORES ADVERSÁRIOS VENCIDOS")
print("=" * 40)

vitorias = df[df["resultado"] == "VITÓRIA"].copy()

melhores_vitorias = (
    vitorias.sort_values("ranking_adversario")
    [
        [
            "data_torneio",
            "torneio",
            "piso",
            "adversario",
            "ranking_adversario",
            "placar"
        ]
    ]
    .head(10)
)

print(melhores_vitorias)

# =========================
# 7. DERROTAS CONTRA ADVERSÁRIOS MAIS FORTES
# =========================

print("\n" + "=" * 40)
print("DERROTAS CONTRA ADVERSÁRIOS MAIS FORTES")
print("=" * 40)

derrotas = df[df["resultado"] == "DERROTA"].copy()

derrotas_fortes = (
    derrotas.sort_values("ranking_adversario")
    [
        [
            "data_torneio",
            "torneio",
            "piso",
            "adversario",
            "ranking_adversario",
            "placar"
        ]
    ]
    .head(10)
)

print(derrotas_fortes)

# =========================
# 8. EXPORTAR BASE ENRIQUECIDA
# =========================

nome_saida = "joao_fonseca_partidas_analisada.xlsx"

df.to_excel(nome_saida, index=False)

print("\n" + "=" * 40)
print("ARQUIVO FINAL GERADO")
print("=" * 40)
print(f"Arquivo criado: {nome_saida}")