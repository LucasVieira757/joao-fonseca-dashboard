import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# CONFIGURAÇÃO
# =========================================================

st.set_page_config(
    page_title="João Fonseca Performance Center",
    page_icon="🎾",
    layout="wide"
)

ARQUIVO = "joao_fonseca_historico_tratado.xlsx"

CORES = {
    "VITÓRIA": "#16A34A",
    "DERROTA": "#DC2626",
    "azul": "#1D4ED8",
    "verde": "#16A34A",
    "amarelo": "#F59E0B",
    "vermelho": "#DC2626",
    "cinza": "#64748B",
    "fundo": "#F8FAFC",
    "card": "#FFFFFF"
}

# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>
    .main {
        background-color: #F8FAFC;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 900;
        color: #0F172A;
        margin-bottom: 0px;
    }

    .hero-subtitle {
        color: #64748B;
        font-size: 16px;
        margin-bottom: 24px;
    }

    .metric-card {
        background: white;
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #E2E8F0;
        box-shadow: 0px 8px 20px rgba(15, 23, 42, 0.05);
    }

    .metric-label {
        color: #64748B;
        font-size: 14px;
        font-weight: 600;
    }

    .metric-value {
        color: #0F172A;
        font-size: 30px;
        font-weight: 900;
    }

    .insight-box {
        background: #EFF6FF;
        border-left: 6px solid #2563EB;
        padding: 18px;
        border-radius: 14px;
        margin-top: 12px;
        margin-bottom: 12px;
        color: #0F172A;
        font-weight: 600;
    }

    .positive-box {
        background: #ECFDF5;
        border-left: 6px solid #16A34A;
        padding: 16px;
        border-radius: 14px;
        font-weight: 600;
    }

    .warning-box {
        background: #FEF3C7;
        border-left: 6px solid #F59E0B;
        padding: 16px;
        border-radius: 14px;
        font-weight: 600;
    }

    .danger-box {
        background: #FEF2F2;
        border-left: 6px solid #DC2626;
        padding: 16px;
        border-radius: 14px;
        font-weight: 600;
    }

    .section-title {
        font-size: 26px;
        font-weight: 900;
        color: #0F172A;
        margin-top: 20px;
        margin-bottom: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# FUNÇÕES
# =========================================================

@st.cache_data
def carregar_dados():
    df = pd.read_excel(ARQUIVO)
    df["data_torneio"] = pd.to_datetime(df["data_torneio"])
    df["mes_ano"] = df["data_torneio"].dt.to_period("M").astype(str)
    return df


def calcular_resumo(base):
    total = len(base)
    vitorias = (base["resultado"] == "VITÓRIA").sum()
    derrotas = (base["resultado"] == "DERROTA").sum()
    aproveitamento = (vitorias / total * 100) if total > 0 else 0

    return total, vitorias, derrotas, aproveitamento


def card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def aproveitamento_por_coluna(base, coluna):
    resumo = (
        base.groupby([coluna, "resultado"])
        .size()
        .unstack(fill_value=0)
    )

    if "VITÓRIA" not in resumo.columns:
        resumo["VITÓRIA"] = 0

    if "DERROTA" not in resumo.columns:
        resumo["DERROTA"] = 0

    resumo["Total"] = resumo["VITÓRIA"] + resumo["DERROTA"]
    resumo["Aproveitamento_%"] = (resumo["VITÓRIA"] / resumo["Total"] * 100).round(2)

    return resumo.reset_index()


def maior_sequencia_vitorias(base):
    base = base.sort_values("data_torneio")
    sequencia_atual = 0
    maior = 0

    for resultado in base["resultado"]:
        if resultado == "VITÓRIA":
            sequencia_atual += 1
            maior = max(maior, sequencia_atual)
        else:
            sequencia_atual = 0

    return maior


def melhor_vitoria(base):
    vitorias = base[base["resultado"] == "VITÓRIA"].dropna(subset=["ranking_adversario"])
    if vitorias.empty:
        return "Não disponível"

    linha = vitorias.sort_values("ranking_adversario").iloc[0]
    return f'{linha["adversario"]} #{int(linha["ranking_adversario"])}'


def gerar_insight_ranking(base):
    top50 = base[base["ranking_adversario"] <= 50]
    fora100 = base[base["ranking_adversario"] > 100]

    taxa_top50 = calcular_resumo(top50)[3] if len(top50) > 0 else 0
    taxa_fora100 = calcular_resumo(fora100)[3] if len(fora100) > 0 else 0

    if taxa_top50 < taxa_fora100:
        return "João apresenta maior dificuldade contra adversários de ranking elevado, especialmente dentro do Top 50."
    return "João demonstra competitividade relevante mesmo contra adversários de ranking elevado."


# =========================================================
# DADOS
# =========================================================

df = carregar_dados()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🎾 Navegação")

pagina = st.sidebar.radio(
    "Escolha a página",
    [
        "Visão Geral",
        "Adversários",
        "Torneios",
        "Scout"
    ]
)

st.sidebar.divider()

anos = sorted(df["ano"].dropna().unique())
pisos = sorted(df["piso"].dropna().unique())
resultados = sorted(df["resultado"].dropna().unique())

ano_sel = st.sidebar.multiselect("Ano", anos, default=anos)
piso_sel = st.sidebar.multiselect("Piso", pisos, default=pisos)
resultado_sel = st.sidebar.multiselect("Resultado", resultados, default=resultados)

df_filtrado = df[
    (df["ano"].isin(ano_sel)) &
    (df["piso"].isin(piso_sel)) &
    (df["resultado"].isin(resultado_sel))
].copy()

# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="hero-title">JOÃO FONSECA PERFORMANCE CENTER</div>
    <div class="hero-subtitle">
        Produto analítico para leitura de evolução, performance, adversários e oportunidades competitivas.
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# PÁGINA 1 — VISÃO GERAL
# =========================================================

if pagina == "Visão Geral":

    total, vitorias, derrotas, aproveitamento = calcular_resumo(df_filtrado)

    ranking_atual = df.sort_values("data_torneio")["ranking_joao"].dropna().iloc[-1]
    melhor_ranking = df["ranking_joao"].min()
    melhor_vit = melhor_vitoria(df)

    col_foto, col1, col2, col3, col4 = st.columns([1.1, 1, 1, 1, 1])

    with col_foto:
        st.markdown("### 🎾 João Fonseca")
        st.markdown("Atleta analisado")
        st.markdown("**Base histórica ATP coletada via Python**")

    with col1:
        card("Ranking atual na base", f"#{int(ranking_atual)}")

    with col2:
        card("Melhor ranking na base", f"#{int(melhor_ranking)}")

    with col3:
        card("Partidas analisadas", total)

    with col4:
        card("Aproveitamento", f"{aproveitamento:.2f}%")

    col5, col6, col7 = st.columns(3)

    with col5:
        card("Vitórias", vitorias)

    with col6:
        card("Derrotas", derrotas)

    with col7:
        card("Melhor vitória", melhor_vit)

    st.markdown('<div class="section-title">📈 Evolução da Carreira</div>', unsafe_allow_html=True)

    resumo_ano = aproveitamento_por_coluna(df_filtrado, "ano")
    ranking_ano = (
        df_filtrado.dropna(subset=["ranking_joao"])
        .groupby("ano")["ranking_joao"]
        .min()
        .reset_index()
        .rename(columns={"ranking_joao": "Melhor Ranking"})
    )

    evolucao = resumo_ano.merge(ranking_ano, on="ano", how="left")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=evolucao["ano"],
        y=evolucao["Melhor Ranking"],
        mode="lines+markers+text",
        name="Melhor ranking",
        text=evolucao["Melhor Ranking"].apply(lambda x: f"#{int(x)}" if pd.notna(x) else ""),
        textposition="top center",
        line=dict(width=4, color="#2563EB"),
        yaxis="y1"
    ))

    fig.add_trace(go.Bar(
        x=evolucao["ano"],
        y=evolucao["VITÓRIA"],
        name="Vitórias",
        marker_color="#16A34A",
        opacity=0.65,
        yaxis="y2"
    ))

    fig.add_trace(go.Scatter(
        x=evolucao["ano"],
        y=evolucao["Aproveitamento_%"],
        mode="lines+markers+text",
        name="Aproveitamento %",
        text=evolucao["Aproveitamento_%"].apply(lambda x: f"{x:.1f}%"),
        textposition="bottom center",
        line=dict(width=3, color="#F59E0B", dash="dot"),
        yaxis="y3"
    ))

    fig.update_layout(
        height=520,
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(title="Ano"),
        yaxis=dict(
            title="Ranking",
            autorange="reversed",
            side="left"
        ),
        yaxis2=dict(
            title="Vitórias",
            overlaying="y",
            side="right",
            showgrid=False
        ),
        yaxis3=dict(
            title="Aproveitamento %",
            overlaying="y",
            side="right",
            anchor="free",
            position=0.95,
            showgrid=False
        ),
        legend=dict(orientation="h", y=1.12)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="insight-box">Insight: a leitura combinada entre ranking, vitórias e aproveitamento mostra se a evolução está vindo apenas por volume de jogos ou por ganho real de competitividade.</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="section-title">🎾 Mapa de desempenho por piso</div>', unsafe_allow_html=True)

    piso = aproveitamento_por_coluna(df_filtrado, "piso").sort_values("Aproveitamento_%", ascending=False)

    melhor_piso = piso.iloc[0]["piso"]
    pior_piso = piso.iloc[-1]["piso"]

    fig_piso = px.bar(
        piso,
        x="piso",
        y="Aproveitamento_%",
        text="Aproveitamento_%",
        color="piso",
        color_discrete_map={
            "Hard": "#16A34A",
            "Clay": "#F59E0B",
            "Grass": "#DC2626"
        },
        hover_data=["VITÓRIA", "DERROTA", "Total"]
    )

    fig_piso.update_layout(
        height=420,
        yaxis_title="Aproveitamento (%)",
        xaxis_title="Piso",
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False
    )

    st.plotly_chart(fig_piso, use_container_width=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            f'<div class="positive-box">Melhor piso: {melhor_piso}</div>',
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f'<div class="danger-box">Maior oportunidade de melhoria: {pior_piso}</div>',
            unsafe_allow_html=True
        )

# =========================================================
# PÁGINA 2 — ADVERSÁRIOS
# =========================================================

elif pagina == "Adversários":

    st.markdown('<div class="section-title">🧠 Análise de Adversários</div>', unsafe_allow_html=True)

    confrontos = (
        df_filtrado.groupby("adversario")
        .agg(
            partidas=("adversario", "count"),
            vitorias=("resultado", lambda x: (x == "VITÓRIA").sum()),
            derrotas=("resultado", lambda x: (x == "DERROTA").sum()),
            melhor_ranking_adversario=("ranking_adversario", "min")
        )
        .reset_index()
    )

    confrontos["aproveitamento_%"] = (
        confrontos["vitorias"] / confrontos["partidas"] * 100
    ).round(2)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Quem ele mais enfrentou?")
        mais_enfrentados = confrontos.sort_values("partidas", ascending=False).head(10)

        fig = px.bar(
            mais_enfrentados,
            x="partidas",
            y="adversario",
            orientation="h",
            text="partidas",
            color="partidas",
            color_continuous_scale="Blues"
        )

        fig.update_layout(height=450, yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Melhor vitória da carreira")
        top_vitorias = (
            df_filtrado[df_filtrado["resultado"] == "VITÓRIA"]
            .dropna(subset=["ranking_adversario"])
            .sort_values("ranking_adversario")
            [
                [
                    "data_torneio",
                    "torneio",
                    "piso",
                    "adversario",
                    "ranking_adversario",
                    "placar",
                    "fase"
                ]
            ]
            .head(10)
        )

        st.dataframe(top_vitorias, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Contra quem ele nunca venceu?")
        nunca_venceu = confrontos[
            (confrontos["vitorias"] == 0) &
            (confrontos["derrotas"] > 0)
        ].sort_values(["partidas", "melhor_ranking_adversario"], ascending=[False, True])

        st.dataframe(nunca_venceu, use_container_width=True)

    with col4:
        st.subheader("Contra quem ele sempre vence?")
        sempre_vence = confrontos[
            (confrontos["derrotas"] == 0) &
            (confrontos["vitorias"] > 0)
        ].sort_values(["partidas", "melhor_ranking_adversario"], ascending=[False, True])

        st.dataframe(sempre_vence, use_container_width=True)

    st.markdown(
        f'<div class="insight-box">Insight automático: {gerar_insight_ranking(df_filtrado)}</div>',
        unsafe_allow_html=True
    )

    ranking = aproveitamento_por_coluna(df_filtrado, "faixa_ranking_adversario")

    fig_rank = px.bar(
        ranking,
        x="faixa_ranking_adversario",
        y="Aproveitamento_%",
        text="Aproveitamento_%",
        color="Aproveitamento_%",
        color_continuous_scale="RdYlGn",
        hover_data=["VITÓRIA", "DERROTA", "Total"]
    )

    fig_rank.update_layout(
        title="Taxa de vitória por faixa de ranking",
        height=450,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(fig_rank, use_container_width=True)

# =========================================================
# PÁGINA 3 — TORNEIOS
# =========================================================

elif pagina == "Torneios":

    st.markdown('<div class="section-title">🏆 Performance por Torneios</div>', unsafe_allow_html=True)

    torneio = aproveitamento_por_coluna(df_filtrado, "tipo_torneio")
    torneio = torneio.sort_values("Total", ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Presença por categoria")

        fig = px.pie(
            torneio,
            values="Total",
            names="tipo_torneio",
            hole=0.45
        )

        fig.update_layout(height=430)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Taxa de vitória por categoria")

        fig = px.bar(
            torneio,
            x="tipo_torneio",
            y="Aproveitamento_%",
            text="Aproveitamento_%",
            color="Aproveitamento_%",
            color_continuous_scale="RdYlGn",
            hover_data=["VITÓRIA", "DERROTA", "Total"]
        )

        fig.update_layout(height=430, xaxis_title="Categoria", yaxis_title="Aproveitamento (%)")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Grand Slams")

    slams = df_filtrado[
        df_filtrado["torneio"].isin(
            ["Australian Open", "Roland Garros", "Wimbledon", "Us Open"]
        )
    ]

    if len(slams) > 0:
        resumo_slams = aproveitamento_por_coluna(slams, "torneio")

        fig_slams = px.bar(
            resumo_slams,
            x="torneio",
            y="Aproveitamento_%",
            text="Aproveitamento_%",
            color="Aproveitamento_%",
            color_continuous_scale="RdYlGn",
            hover_data=["VITÓRIA", "DERROTA", "Total"]
        )

        st.plotly_chart(fig_slams, use_container_width=True)
    else:
        st.info("Não há dados de Grand Slam no filtro atual.")

    melhor_categoria = torneio.sort_values("Aproveitamento_%", ascending=False).iloc[0]["tipo_torneio"]

    st.markdown(
        f'<div class="insight-box">Insight: melhor performance em {melhor_categoria}. Isso ajuda a entender em qual nível competitivo João converte melhor suas oportunidades.</div>',
        unsafe_allow_html=True
    )

# =========================================================
# PÁGINA 4 — SCOUT
# =========================================================

elif pagina == "Scout":

    st.markdown('<div class="section-title">🔍 Scout — Inteligência Competitiva</div>', unsafe_allow_html=True)

    total, vitorias, derrotas, aproveitamento = calcular_resumo(df_filtrado)

    piso = aproveitamento_por_coluna(df_filtrado, "piso").sort_values("Aproveitamento_%", ascending=False)
    melhor_piso = piso.iloc[0]["piso"]
    pior_piso = piso.iloc[-1]["piso"]

    melhor_vit = melhor_vitoria(df_filtrado)
    sequencia = maior_sequencia_vitorias(df_filtrado)

    media_ranking_adv = df_filtrado["ranking_adversario"].mean()

    top50 = df_filtrado[df_filtrado["ranking_adversario"] <= 50]
    top100 = df_filtrado[df_filtrado["ranking_adversario"] <= 100]

    taxa_top50 = calcular_resumo(top50)[3] if len(top50) > 0 else 0
    taxa_top100 = calcular_resumo(top100)[3] if len(top100) > 0 else 0

    c1, c2, c3 = st.columns(3)

    with c1:
        card("Melhor piso", melhor_piso)
        card("Pior piso", pior_piso)

    with c2:
        card("Melhor vitória", melhor_vit)
        card("Maior sequência", f"{sequencia} vitórias")

    with c3:
        card("Média ranking adversários", f"#{media_ranking_adv:.0f}")
        card("Aproveitamento geral", f"{aproveitamento:.2f}%")

    st.markdown('<div class="section-title">Top 50 vs Top 100</div>', unsafe_allow_html=True)

    comparativo = pd.DataFrame({
        "Grupo": ["Contra Top 50", "Contra Top 100"],
        "Aproveitamento_%": [round(taxa_top50, 2), round(taxa_top100, 2)],
        "Partidas": [len(top50), len(top100)]
    })

    fig = px.bar(
        comparativo,
        x="Grupo",
        y="Aproveitamento_%",
        text="Aproveitamento_%",
        color="Aproveitamento_%",
        color_continuous_scale="RdYlGn",
        hover_data=["Partidas"]
    )

    fig.update_layout(height=430, yaxis_title="Aproveitamento (%)")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Conclusões Automáticas</div>', unsafe_allow_html=True)

    if melhor_piso == "Hard":
        st.markdown(
            '<div class="positive-box">João performa melhor em quadras rápidas, com maior aproveitamento no piso Hard.</div>',
            unsafe_allow_html=True
        )

    if pior_piso == "Grass":
        st.markdown(
            '<div class="danger-box">Performance inconsistente em gramado. Grass aparece como principal oportunidade de melhoria.</div>',
            unsafe_allow_html=True
        )

    if taxa_top50 < taxa_top100:
        st.markdown(
            '<div class="warning-box">Existe queda de aproveitamento quando o nível dos adversários sobe. Isso indica dificuldade natural contra jogadores de ranking elevado.</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="insight-box">Leitura executiva: o perfil atual mostra potencial competitivo, força em quadras rápidas e necessidade de observar melhor a performance contra adversários de elite.</div>',
        unsafe_allow_html=True
    )

# =========================================================
# RODAPÉ
# =========================================================

st.divider()

st.caption(
    "Projeto desenvolvido com Python, Pandas, Plotly e Streamlit. Dados tratados para fins de análise esportiva e portfólio."
)