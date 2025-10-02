
window.document.addEventListener("DOMContentLoaded", function () {


    const botaoTresbarras = document.getElementById('tresRiscos'); 
    if (botaoTresbarras) {
        botaoTresbarras.addEventListener('click', function() {
            const fundoBarra3 = document.querySelector('.fundobarra2');
            if (fundoBarra3) {
                fundoBarra3.classList.remove('fundobarra2');
                fundoBarra3.classList.add('fundobarra3');

            } else {
                console.error("Elemento com a classe 'fundobarra2' não encontrado!");
            }
        });
        
    } else {
        console.warn("Botão com ID 'tresRiscos' não encontrado no DOM!");
    }

    const fechar = document.getElementById('Fechar');
    if (fechar) {
        fechar.addEventListener('click', function() {
            const fundoBarra2 = document.querySelector('.fundobarra3');
            if (fundoBarra2) {
                fundoBarra2.classList.remove('fundobarra3');
                fundoBarra2.classList.add('fundobarra2');
                
            } else {
                console.error("Elemento com a classe 'fundobarra3' não encontrado!");
            }
        });

    } else {
        console.warn("Botão com ID 'Fechar' não encontrado no DOM!");
    }

    const stars = document.querySelectorAll("#stars span");
    const result = document.querySelector(".result");
    let selected = 0;

    stars.forEach(star => {
    star.addEventListener("click", () => {
        selected = star.dataset.value; // pega o valor da estrela clicada

        // pinta até a estrela selecionada
        stars.forEach(s => {
            s.classList.toggle("active", s.dataset.value <= selected);
        });

            // atualiza o texto
            result.textContent = `${selected} estrela${selected > 1 ? "s" : ""}`;
        });
    });

});


