#!/bin/bash

# Atualizar o pip para a versão mais recente
echo "Atualizando o pip..."
python3 -m pip install --upgrade pip

# Verificar se o Flask já está instalado
echo "Verificando a instalação do Flask..."
if ! python3 -m flask --version; then
    # Instalar o Flask se não estiver instalado
    echo "Instalando o Flask..."
    python3 -m pip install Flask
else
    echo "Flask já está instalado."
fi

# Executar o arquivo app.py com Python 3
echo "Executando app.py..."
python3 public/app.py