import pandas as pd

# =========================
# 1. CONFIGURAÇÃO
# =========================

arquivo_entrada = "joao_fonseca_historico_tratado.xlsx"
arquivo_saida = "joao_fonseca_relatorio_historico.xlsx"

# =========================
# 2. CARREGAR BASE
# =========================

df = pd.read_excel(arquivo_entrada)

# =========================
# 3. FUNÇÃO DE ANÁLISE
# =========================

def criar_resumo(df, coluna):
    resumo = (
        df.groupby([coluna, "resultado"])
        .size()
        .unstack(fill_value=0)
    )

    if "VITÓRIA" not in resumo.columns:
        resumo["VITÓRIA"] = 0

    if "DERROTA" not in resumo.columns:
        resumo["DERROTA"] = 0

    resumo["Total"] = resumo["VITÓRIA"] + resumo["DERROTA"]
    resumo["Aproveitamento_%"] = (
        resumo["VITÓRIA"] / resumo["Total"] * 100
    ).round(2)

    return resumo.reset_index()

# =========================
# 4. RESUMO GERAL
# =========================

total_partidas = len(df)
vitorias = (df["resultado"] == "VITÓRIA").sum()
derrotas = (df["resultado"] == "DERROTA").sum()
aproveitamento = round((vitorias / total_partidas) * 100, 2)

resumo_geral = pd.DataFrame({
    "Métrica": [
        "Total de partidas",
        "Vitórias",
        "Derrotas",
        "Aproveitamento (%)"
    ],
    "Valor": [
        total_partidas,
        vitorias,
        derrotas,
        aproveitamento
    ]
})

# =========================
# 5. ANÁLISES
# =========================

resumo_ano = criar_resumo(df, "ano")
resumo_piso = criar_resumo(df, "piso")
resumo_tipo_torneio = criar_resumo(df, "tipo_torneio")
resumo_faixa_ranking = criar_resumo(df, "faixa_ranking_adversario")

# =========================
# 6. TOP VITÓRIAS
# =========================

top_vitorias = (
    df[df["resultado"] == "VITÓRIA"]
    .sort_values("ranking_adversario")
    [
        [
            "data_torneio",
            "ano",
            "torneio",
            "tipo_torneio",
            "piso",
            "adversario",
            "ranking_adversario",
            "placar",
            "fase"
        ]
    ]
    .head(10)
)

# =========================
# 7. DERROTAS CONTRA ADVERSÁRIOS FORTES
# =========================

derrotas_fortes = (
    df[df["resultado"] == "DERROTA"]
    .sort_values("ranking_adversario")
    [
        [
            "data_torneio",
            "ano",
            "torneio",
            "tipo_torneio",
            "piso",
            "adversario",
            "ranking_adversario",
            "placar",
            "fase"
        ]
    ]
    .head(10)
)

# =========================
# 8. EVOLUÇÃO DO RANKING DO JOÃO
# =========================

evolucao_ranking = (
    df[
        [
            "data_torneio",
            "ano",
            "torneio",
            "ranking_joao"
        ]
    ]
    .dropna(subset=["ranking_joao"])
    .sort_values("data_torneio")
)

# =========================
# 9. EXPORTAR RELATÓRIO EXCEL
# =========================

with pd.ExcelWriter(arquivo_saida, engine="openpyxl") as writer:
    resumo_geral.to_excel(writer, sheet_name="Resumo Geral", index=False)
    resumo_ano.to_excel(writer, sheet_name="Resumo por Ano", index=False)
    resumo_piso.to_excel(writer, sheet_name="Resumo por Piso", index=False)
    resumo_tipo_torneio.to_excel(writer, sheet_name="Resumo Torneio", index=False)
    resumo_faixa_ranking.to_excel(writer, sheet_name="Resumo Ranking Adv", index=False)
    top_vitorias.to_excel(writer, sheet_name="Top Vitorias", index=False)
    derrotas_fortes.to_excel(writer, sheet_name="Derrotas Fortes", index=False)
    evolucao_ranking.to_excel(writer, sheet_name="Evolucao Ranking", index=False)

# =========================
# 10. RESULTADO NO TERMINAL
# =========================

print("=" * 60)
print("RELATÓRIO HISTÓRICO JOÃO FONSECA")
print("=" * 60)

print("\nRESUMO GERAL")
print(resumo_geral)

print("\nRESUMO POR ANO")
print(resumo_ano)

print("\nRESUMO POR PISO")
print(resumo_piso)

print("\nRESUMO POR TIPO DE TORNEIO")
print(resumo_tipo_torneio)

print("\nTOP 10 VITÓRIAS")
print(top_vitorias)

print("\nArquivo gerado com sucesso:")
print(arquivo_saida)