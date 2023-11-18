function mostrarSenhaModal(site, username, password) {
    // Aqui você faria a chamada ao servidor para buscar a senha, mas por simplicidade, vou omitir essa parte

    // Exemplo de como você poderia preencher o modal com os dados da senha
    document.getElementById('siteModal').innerText = 'Site: ' + site; // Substitua com os dados reais
    document.getElementById('usernameModal').innerText = 'Username: ' + username;
    document.getElementById('passwordModal').innerText = 'Password: ' + password;

    // Mostrar o modal
    var modal = document.getElementById("senhaModal");
    modal.style.display = "block";

    // Quando o usuário clica no (X), fechar o modal
    var span = document.getElementsByClassName("close")[0];
    span.onclick = function () {
        modal.style.display = "none";
    }

    // Quando o usuário clica fora do modal, fechar o modal
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}
function copiarSenha() {
    const senha = document.getElementById('passwordModal').textContent;
    navigator.clipboard.writeText(senha.split(" ")[1]).then(() => {
        alert('Password copied to clipboard!');
    }).catch(err => {
        console.error('Error', err);
    });
}
function mostrarUpdateModal(docId, username) {
    document.getElementById('usernameModal2').innerText = 'New Username: ' + username;
    // Configura a ação do formulário com o ID do documento
    var form = document.querySelector("#updateModal form");
    form.action = "/update/" + docId;

    // Mostrar o modal
    var modal = document.getElementById("updateModal");
    modal.style.display = "block";

    // Quando o usuário clica no (X), fechar o modal
    var span = modal.querySelector(".close");
    span.onclick = function () {
        modal.style.display = "none";
    }

    // Quando o usuário clica fora do modal, fechar o modal
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}

function mostrarConfirmModal(docId, username) {
    // Configura a ação do formulário com o ID do documento
    var form = document.querySelector("#confirmModal form");
    form.action = "/delete/" + docId;

    // Mostrar o modal
    var modal = document.getElementById("confirmModal");
    modal.style.display = "block";

    // Quando o usuário clica no (X), fechar o modal
    var span = modal.querySelector(".close");
    span.onclick = function () {
        modal.style.display = "none";
    }

    // Quando o usuário clica fora do modal, fechar o modal
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}

document.querySelector(".search-bar input").addEventListener('input', function () {
    var input = this.value.toLowerCase();
    var listItems = document.getElementById('userspasswords').getElementsByTagName('li');

    for (var i = 1; i < listItems.length; i++) {  // Começa com 1 para pular o cabeçalho
        var site = listItems[i].getElementsByClassName('site')[0].textContent.toLowerCase();
        var username = listItems[i].getElementsByClassName('username')[0].textContent.toLowerCase();

        if (site.includes(input) || username.includes(input)) {
            listItems[i].style.display = '';  // Mostra o item se corresponder à pesquisa
        } else {
            listItems[i].style.display = 'none';  // Oculta o item se não corresponder
        }
    }
});
function deleteItem(docId) {
    var senha = document.getElementById("confirmPassword").value;
    if (senha != null && senha != "") {
        fetch('/delete/' + docId, { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    alert('Password deleted successfully!');
                    window.location.reload();
                } else {
                    alert('Incorrect password or failed to delete the item.');
                }
            })
    }
}
function updateItem(docId) {
    fetch('/update/' + docId, { method: 'POST' })
        .then(response => {
            if (response.ok) {
                alert('Senha atualizada com sucesso!');
                window.location.reload();
            } else {
                alert('Falha ao atualizar a senha.');
            }
        })
        .catch(error => console.error('Erro:', error));
}
let sortOrder = {};  // Objeto para manter a ordem de classificação

function sortTable(column) {
    // Alternar a direção da ordenação
    sortOrder[column] = sortOrder[column] === 'asc' ? 'desc' : 'asc';

    // Obter a lista de itens
    let list = document.querySelectorAll('.li');
    list = Array.from(list);

    // Ordenar a lista
    list.sort((a, b) => {
        let textA = String(a.querySelector('.' + column).textContent);
        let textB = String(b.querySelector('.' + column).textContent);

        if (sortOrder[column] === 'asc') {
            return textA.localeCompare(textB);
        } else {
            return textB.localeCompare(textA);
        }
    });

    // Atualizar a direção do ícone
    updateIcon(column, sortOrder[column]);

    // Reordenar os elementos na página
    let container = document.getElementById('titles').parentNode;
    list.forEach(item => container.appendChild(item));
}

function updateIcon(column, direction) {
    // Limpar ícones anteriores
    document.querySelectorAll('#titles .fa').forEach(icon => {
        icon.className = 'fa fa-hand-pointer-o';
    });

    // Configurar o ícone correto
    let icon = document.getElementById(`icon-${column}`);
    if (direction === 'asc') {
        icon.className = 'fa fa-sort-up';
    } else {
        icon.className = 'fa fa-sort-down';
    }
}