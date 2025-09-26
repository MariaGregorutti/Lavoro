window.document.addEventListener("DOMContentLoaded", function () {
  
        const botaoTresbarras = document.getElementById('tresRiscos')

        botaoTresbarras.addEventListener('click', function() {
                const fundoBarra3 = document.querySelector('.fundobarra2');
                fundoBarra3.classList.remove('fundobarra2');
                fundoBarra3.classList.add('fundobarra3');;
        });        

        const fechar = document.getElementById('Fechar')

        fechar.addEventListener('click', function() {
                const fundoBarra2 = document.querySelector('.fundobarra3');
                fundoBarra2.classList.remove('fundobarra3');
                fundoBarra2.classList.add('fundobarra2');;
        });        


})

