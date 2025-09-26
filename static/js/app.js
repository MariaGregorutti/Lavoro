// Ouvinte que aguarda até que todo o conteúdo HTML da página esteja totalmente carregado e o DOM esteja pronto
window.document.addEventListener("DOMContentLoaded", function () {

    // Seleciona o elemento HTML que tem o ID 'tresRiscos', geralmente um botão/menu hamburguer
    const botaoTresbarras = document.getElementById('tresRiscos');

    // Verifica se o elemento 'botaoTresbarras' foi encontrado para evitar erros caso não exista no DOM
    if (botaoTresbarras) {

        // Adiciona um evento que será disparado toda vez que o usuário clicar no botão 'tresRiscos'
        botaoTresbarras.addEventListener('click', function() {

            // Busca no DOM o primeiro elemento que possui a classe 'fundobarra2'
            const fundoBarra3 = document.querySelector('.fundobarra2');

            // Verifica se o elemento com a classe 'fundobarra2' foi encontrado para evitar erro de null
            if (fundoBarra3) {

                // Remove a classe CSS 'fundobarra2' desse elemento para "desligar" o estilo antigo
                fundoBarra3.classList.remove('fundobarra2');

                // Adiciona a classe CSS 'fundobarra3' para "ligar" um novo estilo (exemplo: abrir menu, mudar cor, tamanho, etc)
                fundoBarra3.classList.add('fundobarra3');

            } else {
                // Caso não encontre, pode exibir um erro no console para ajudar no debug
                console.error("Elemento com a classe 'fundobarra2' não encontrado!");
            }
        });
    } else {
        // Caso o botão não exista, loga um aviso para não passar despercebido
        console.warn("Botão com ID 'tresRiscos' não encontrado no DOM!");
    }

    // Seleciona o elemento HTML com ID 'Fechar', geralmente um botão para fechar/fechar menu
    const fechar = document.getElementById('Fechar');

    // Verifica se o botão de fechar existe para evitar erros
    if (fechar) {

        // Adiciona evento para escutar cliques no botão de fechar
        fechar.addEventListener('click', function() {

            // Busca o primeiro elemento que possui a classe 'fundobarra3' (estado ativo/aberto do menu)
            const fundoBarra2 = document.querySelector('.fundobarra3');
            

            // Verifica se o elemento foi encontrado para evitar erro caso não exista
            if (fundoBarra2) {

                // Remove a classe 'fundobarra3' para desligar o estilo ativo
                fundoBarra2.classList.remove('fundobarra3');

                // Adiciona a classe 'fundobarra2' para voltar ao estilo original (menu fechado)
                fundoBarra2.classList.add('fundobarra2');
                
            } else {
                // Caso não encontre, avisa no console
                console.error("Elemento com a classe 'fundobarra3' não encontrado!");
            }
        });

    } else {
        // Caso o botão de fechar não exista, avisa no console
        console.warn("Botão com ID 'Fechar' não encontrado no DOM!");
    }

});


