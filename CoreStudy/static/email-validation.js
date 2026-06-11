function configurarValidacaoEmail(input) {
    if (!input) {
        return;
    }

    const mensagem = document.getElementById(input.dataset.emailFeedback);
    const permiteAdmin = input.dataset.allowAdmin === "true";
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

    function validarEmail() {
        const valor = input.value.trim();
        const emailValido = emailRegex.test(valor);
        const adminValido = permiteAdmin && valor.toLowerCase() === "admin";

        input.classList.remove("input-valid", "input-invalid");

        if (valor === "") {
            input.setCustomValidity("");
            if (mensagem) {
                mensagem.textContent = "";
            }
            return;
        }

        if (emailValido || adminValido) {
            input.setCustomValidity("");
            input.classList.add("input-valid");
            if (mensagem) {
                mensagem.textContent = emailValido ? "Email valido." : "";
            }
            return;
        }

        input.setCustomValidity("Digite um email valido, como nome@dominio.com.");
        input.classList.add("input-invalid");
        if (mensagem) {
            mensagem.textContent = "Digite um email valido, como nome@dominio.com.";
        }
    }

    input.addEventListener("input", validarEmail);
    input.addEventListener("blur", validarEmail);
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-email-validation]").forEach(configurarValidacaoEmail);
});
