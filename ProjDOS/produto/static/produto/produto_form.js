document.addEventListener('DOMContentLoaded', function () {
    const precoCampo = document.getElementById('preco');
    const saldoEstoqueCampo = document.getElementById('saldo_estoque');

    // Formata o valor inicial do campo de preço
    if (precoCampo) {
        formatarMoeda(precoCampo);
    }

    // Define o valor inicial do campo de quantidade em estoque
    if (saldoEstoqueCampo && !saldoEstoqueCampo.value) {
        saldoEstoqueCampo.value = 0;
    }

    const confirmBtn = document.getElementById('confirmSaveBtn');
    if (confirmBtn) {
        confirmBtn.addEventListener('click', function () {
            document.getElementById('editForm').submit();
        });
    }
});

function formatarMoeda(campo) {
    // Se já estiver formatado, remove tudo que não for número
    let valor = campo.value.replace(/\D/g, '');

    // Se o valor inicial vier como decimal (ex: 1234.56), trata diferente
    if (!valor && campo.value) {
        // Tenta converter para centavos
        let floatVal = parseFloat(campo.value.replace(',', '.'));
        if (!isNaN(floatVal)) {
            valor = String(Math.round(floatVal * 100));
        }
    }

    if (!valor) {
        campo.value = 'R$0,00';
        return;
    }

    // Limite máximo (9999999 centavos = R$99.999,99)
    if (valor.length > 7) valor = valor.slice(0, 7);

    valor = (parseFloat(valor) / 100).toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    });

    campo.value = valor;
}

function verificarQuantidade(campo) {
    if (parseInt(campo.value) > 99999) {
        campo.value = 99999;
    }
    if (!campo.value) {
        campo.value = 0;
    }
}