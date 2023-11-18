#!/bin/bash

# Script para configurar e iniciar um projeto Flask com Firebase e Cryptography

echo "Iniciando a configuração do projeto Flask..."

# Atualizar o pip para a versão mais recente
echo "Atualizando o pip para a versão mais recente..."
python3 -m pip install --upgrade pip && echo "Pip atualizado com sucesso!" || echo "Falha ao atualizar o pip."

# Verificar se o Flask já está instalado e instalá-lo se necessário
echo "Verificando a instalação do Flask..."
if ! python3 -m flask --version; then
    echo "Instalando o Flask..."
    if python3 -m pip install Flask; then
        echo "Flask instalado com sucesso!"
    else
        echo "Falha ao instalar o Flask."
        exit 1
    fi
else
    echo "Flask já está instalado."
fi

# Instalar o Firebase Admin SDK
echo "Instalando Firebase Admin SDK..."
if pip install firebase-admin; then
    echo "Firebase Admin SDK instalado com sucesso!"
else
    echo "Falha ao instalar o Firebase Admin SDK."
    exit 1
fi

# Instalar a biblioteca Cryptography
echo "Instalando a biblioteca Cryptography..."
if pip install cryptography; then
    echo "Biblioteca Cryptography instalada com sucesso!"
else
    echo "Falha ao instalar a biblioteca Cryptography."
    exit 1
fi

# Executar o arquivo app.py com Python 3
echo "Executando app.py..."
python3 public/app.py