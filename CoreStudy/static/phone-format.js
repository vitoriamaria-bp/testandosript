function formatarTelefoneBrasil(valor) {
    const numeros = valor.replace(/\D/g, "").slice(0, 11);

    if (numeros.length <= 2) {
        return numeros;
    }

    if (numeros.length <= 7) {
        return `(${numeros.slice(0, 2)}) ${numeros.slice(2)}`;
    }

    return `(${numeros.slice(0, 2)}) ${numeros.slice(2, 7)}-${numeros.slice(7)}`;
}

function configurarTelefone(grupo) {
    const codigo = grupo.querySelector("[data-phone-country]");
    const numero = grupo.querySelector("[data-phone-number]");
    const completo = grupo.querySelector("[data-phone-full]");

    function atualizarTelefone() {
        if (codigo.value === "+55") {
            numero.value = formatarTelefoneBrasil(numero.value);
        }

        completo.value = `${codigo.value} ${numero.value.trim()}`.trim();
    }

    if (completo.value) {
        const partes = completo.value.match(/^(\+\d+)\s*(.*)$/);
        if (partes) {
            codigo.value = partes[1];
            numero.value = partes[2];
        } else {
            numero.value = completo.value;
        }
    }

    numero.addEventListener("input", atualizarTelefone);
    codigo.addEventListener("change", atualizarTelefone);
    grupo.closest("form").addEventListener("submit", atualizarTelefone);
    atualizarTelefone();
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-phone-field]").forEach(configurarTelefone);
});
