
window.document.addEventListener("DOMContentLoaded", function () {


    const botaoTresbarras = document.getElementById('tresRiscos'); 
    if (botaoTresbarras) {
        botaoTresbarras.addEventListener('click', function() {

            console.log('vsjvbxjh')
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

    /*Estrela Js*/ 

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
            if (result){
            result.textContent = `${selected} estrela${selected > 1 ? "s" : ""}`;
            }
        });

    });

    //Limitar Caractere telefone

    const telefone = document.getElementById('telefone');/* pega a inforção do input*/
    if (telefone){
    const limite = 11;

    telefone.addEventListener('input', function() { //O addEventListener é para funcionar com evento e o input
                                                    //é um evento e o function é uma função anonima onde ele pega as
                                                    //as informações do telefone

      if (this.value.length > limite) { //this refere-se ao próprio elemento HTML que disparou o evento
                                        //(neste caso, o input com o id="telefone").this.value.length retorna a
                                        //quantidade de caracteres que o usuário digitou no campo.

        this.value = this.value.slice(0, limite); //this.value.slice(0, limite) usa o método slice() para "fatiar"
                                                  //a string de texto do campo.
                                                  //O resultado é uma nova string com no máximo 11 caracteres,
                                                  //que é então atribuída de volta ao valor do campo (this.value = ...),
                                                  //efetivamente "cortando" qualquer caractere extra que o usuário tenha
                                                  //digitado
      }
    });
   }
});

// Check caixa no selecionar



