#!/bin/bash
set -euo pipefail

echo "=== CONFIGURAÇÃO DO AMBIENTE ==="

# Cria ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

echo "Ativando ambiente virtual..."
source venv/bin/activate

echo "Instalando dependências Python..."
pip install --upgrade pip
pip install matplotlib pandas numpy tabulate

echo " Ambiente configurado com sucesso!"
echo ""
echo " Para executar o experimento, use:"
echo "   ./run_testes.sh"
