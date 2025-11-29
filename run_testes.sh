#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -d "venv" ] || ! python3 -c "import matplotlib, pandas, numpy, tabulate" 2>/dev/null; then
    bash ./setup.sh
fi

source venv/bin/activate

OUTPUT_CSV="resultados_completos.csv"

REPETICOES=10
TAMANHOS=$(seq 50 50 10000; seq 5500 500 30000)
TAMANHOS_SWAP="65000 70000"

TIPOS=("estatico_rapido" "estatico_lento" "dinamico_rapido" "dinamico_lento")

rm -f "$OUTPUT_CSV" info_sistema.txt

echo "Tamanho,Iteracao,Tipo,Tempo_ms" > "$OUTPUT_CSV"

{
    echo "INFORMAÇÕES DO SISTEMA"
    echo "======================="
    echo "Data: $(date)"
    echo "CPU: $(lscpu | grep 'Model name' | cut -d: -f2 | xargs)"
    echo "Cache L1: $(lscpu | grep 'L1d cache' | cut -d: -f2 | xargs)"
    echo "Cache L2: $(lscpu | grep 'L2 cache' | cut -d: -f2 | xargs)"
    echo "Cache L3: $(lscpu | grep 'L3 cache' | cut -d: -f2 | xargs)"
    echo "RAM: $(free -h | grep Mem | awk '{print $2}')"
} > info_sistema.txt

echo "========== TESTES NORMAIS =========="

for SIZE in $TAMANHOS; do
    echo "TAM=${SIZE}"
    
    for T in "${TIPOS[@]}"; do
        gcc -O2 -march=native -std=c99 "${T}.c" -o "$T" -D TAM=$SIZE
    done
    
    for ((i=1;i<=REPETICOES;i++)); do
        for T in "${TIPOS[@]}"; do
            # Tenta executar. Se falhar (ex: segfault), avisa e continua.
            if tempo=$(./"$T"); then
                echo "$SIZE,$i,$T,$tempo" >> "$OUTPUT_CSV"
            else
                echo "AVISO: Falha ao executar $T com TAM=$SIZE (provavelmente memória insuficiente). Ignorando." >&2
            fi
        done
    done
done

echo ""
echo "========== TESTES DE SWAP =========="

for SIZE in $TAMANHOS_SWAP; do
    RAM_GB=$(echo "scale=1; $SIZE * $SIZE * 12 / 1024 / 1024 / 1024" | bc)
    echo "TAM=${SIZE} (~${RAM_GB}GB)"
    
    for T in "${TIPOS[@]}"; do
        gcc -O2 -march=native -std=c99 "${T}.c" -o "$T" -D TAM=$SIZE
    done
    
    for T in "${TIPOS[@]}"; do
        if tempo=$(./"$T"); then
            echo "$SIZE,1,$T,$tempo" >> "$OUTPUT_CSV"
        else
             echo "AVISO: Falha ao executar $T com TAM=$SIZE (Swap). Ignorando." >&2
        fi
    done
    
    sleep 2
done

echo ""
echo "========== GERANDO GRÁFICOS =========="
python3 gerar_graficos.py

echo ""
echo "Concluído!"
echo "Arquivos: $OUTPUT_CSV, estatisticas.csv, info_sistema.txt, comparacao_memorias.png, estatisticas_30k.png"
