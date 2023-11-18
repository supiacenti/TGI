async function gerarSenha() {
    const resposta = await fetch('/gerar_senha');
    const data = await resposta.json();
    document.getElementById('senha').textContent = data.senha;
}

function copiarSenha() {
    const senha = document.getElementById('senha').textContent;
    navigator.clipboard.writeText(senha).then(() => {
        alert('Password copied to clipboard!');
    }).catch(err => {
        console.error('Error', err);
    });
}