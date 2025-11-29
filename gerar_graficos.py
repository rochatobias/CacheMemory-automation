import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("resultados_completos.csv")
stats = df.groupby(["Tamanho","Tipo"])["Tempo_ms"].agg(["mean","std"])
stats.to_csv("estatisticas.csv")

cores = {
    "estatico_rapido": "#2ecc71",
    "estatico_lento": "#e74c3c",
    "dinamico_rapido": "#3498db",
    "dinamico_lento": "#f39c12"
}

# Gráfico 1: Tempo Normal (até 30000)
df_normal = df[df["Tamanho"] <= 30000]
stats_normal = df_normal.groupby(["Tamanho","Tipo"])["Tempo_ms"].agg(["mean","std"])

plt.figure(figsize=(12,7))

for tipo in sorted(df_normal["Tipo"].unique()):
    subset = stats_normal.loc[pd.IndexSlice[:, tipo], :]
    tamanhos = subset.index.get_level_values(0)
    medias = subset["mean"]
    desvios = subset["std"]
    
    plt.errorbar(tamanhos, medias, yerr=desvios, 
                 label=tipo.replace("_", " ").title(),
                 marker='o', markersize=4, linewidth=2,
                 color=cores.get(tipo, None), alpha=0.8,
                 capsize=3, capthick=1)

plt.xlabel("Tamanho da Matriz (NxN)", fontsize=12, fontweight='bold')
plt.ylabel("Tempo Médio (ms)", fontsize=12, fontweight='bold')
plt.title("Performance Normal - Impacto da Localidade de Cache (até 30k)", 
          fontsize=14, fontweight='bold', pad=20)
plt.legend(loc='best', fontsize=10, framealpha=0.9)
plt.grid(True, alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig("comparacao_memorias.png", dpi=300, bbox_inches='tight')

# Gráfico 2: Desvio Padrão (até 30000) - Análise de Variabilidade
df_stats = df[df["Tamanho"] <= 30000]
stats_30k = df_stats.groupby(["Tamanho","Tipo"])["Tempo_ms"].agg(["mean","std"])

plt.figure(figsize=(12,7))

tamanhos_selecionados = [50, 1000, 5000, 10000, 15000, 20000, 25000, 30000]
tipos = sorted(df_stats["Tipo"].unique())

# Número de tamanhos e tipos
n_tam = len(tamanhos_selecionados)
n_tipos = len(tipos)

# Posição dos grupos
x_positions = np.arange(n_tam)

# Largura de cada barra
largura = 0.18   # valor fixo evita colapso dos rótulos

# Plot das barras
for i, tipo in enumerate(tipos):
    desvios = []
    for tam in tamanhos_selecionados:
        try:
            desvio = stats_30k.loc[(tam, tipo), "std"]
            desvios.append(desvio)
        except KeyError:
            desvios.append(0)
    
    # deslocamento dentro de cada grupo
    offset = (i - (n_tipos - 1) / 2) * largura

    plt.bar(
        x_positions + offset,
        desvios,
        width=largura,
        label=tipo.replace("_", " ").title(),
        color=cores.get(tipo, None),
        alpha=0.8,
        edgecolor="black",
        linewidth=0.7
    )

plt.xlabel("Tamanho da Matriz (NxN)", fontsize=12, fontweight='bold')
plt.ylabel("Desvio Padrão (ms)", fontsize=12, fontweight='bold')
plt.title("Variabilidade de Performance - Desvio Padrão (até 30k)", fontsize=14, fontweight='bold')

# Labels do eixo X (apenas nas posições centrais)
plt.xticks(
    x_positions,
    [str(t) for t in tamanhos_selecionados],
    rotation=45,
    ha='right'
)

plt.legend(loc='upper left', fontsize=10)
plt.grid(True, axis='y', linestyle='--', alpha=0.35)

plt.tight_layout()
plt.savefig("estatisticas_30k.png", dpi=300, bbox_inches='tight')

# Gráfico 3: Comparação com SWAP (até 35k com demarcação em 30k)
df_swap = df[df["Tamanho"] <= 35000]
stats_swap = df_swap.groupby(["Tamanho","Tipo"])["Tempo_ms"].agg(["mean","std"])

plt.figure(figsize=(12,7))

for tipo in sorted(df_swap["Tipo"].unique()):
    subset = stats_swap.loc[pd.IndexSlice[:, tipo], :]
    tamanhos = subset.index.get_level_values(0)
    medias = subset["mean"]
    desvios = subset["std"]
    
    plt.errorbar(tamanhos, medias, yerr=desvios, 
                 label=tipo.replace("_", " ").title(),
                 marker='o', markersize=4, linewidth=2,
                 color=cores.get(tipo, None), alpha=0.8,
                 capsize=3, capthick=1)

# Linha vertical tracejada em 30k marcando início do SWAP
plt.axvline(x=30000, color='red', linestyle='--', linewidth=2.5, alpha=0.8, 
            label='Início SWAP (30k)')

plt.xlabel("Tamanho da Matriz (NxN)", fontsize=12, fontweight='bold')
plt.ylabel("Tempo Médio (ms)", fontsize=12, fontweight='bold')
plt.title("Impacto do SWAP na Performance (até 35k)", 
          fontsize=14, fontweight='bold', pad=20)
plt.legend(loc='best', fontsize=10, framealpha=0.9)
plt.grid(True, alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig("comparacao_memorias_com_swap.png", dpi=300, bbox_inches='tight')

print("Gráficos gerados: comparacao_memorias.png, estatisticas_30k.png, comparacao_memorias_com_swap.png")
