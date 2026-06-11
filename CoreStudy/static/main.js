document.addEventListener("DOMContentLoaded", function() {
    // 1. Fechar Toasts Automaticamente
    setTimeout(function() {
        let toasts = document.querySelectorAll('.alert-toast');
        toasts.forEach(t => { t.style.opacity = '0'; setTimeout(() => t.remove(), 300); });
    }, 4000);

    // 2. Destacar o Menu Ativo Dinamicamente
    const currentPath = window.location.pathname;
    const menuLinks = document.querySelectorAll('.sidebar-menu li a');
    
    menuLinks.forEach(link => {
        if (currentPath === link.getAttribute('href') || (link.getAttribute('href') !== '/admin' && currentPath.startsWith(link.getAttribute('href') + '/'))) {
            if(link.getAttribute('href') === '/admin' && currentPath !== '/admin') return;
            link.classList.add('active');
        }
    });

    // 3. Recolher e Expandir Menu
    const toggleBtn = document.getElementById('toggle-sidebar');
    const html = document.documentElement; // Controla a página inteira de uma vez

    if(toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            html.classList.toggle('mini');
            
            // Salva o estado atual
            if (html.classList.contains('mini')) {
                localStorage.setItem('sidebarState', 'mini');
            } else {
                localStorage.removeItem('sidebarState');
            }
        });
    }
});

// Máscara de telefone
function mascaraTelefone(event) {
    let input = event.target;
    let telefone = input.value.replace(/\D/g, ""); 
    if (telefone.length > 10) { telefone = telefone.replace(/^(\d{2})(\d{5})(\d{4}).*/, "($1) $2-$3"); } 
    else if (telefone.length > 5) { telefone = telefone.replace(/^(\d{2})(\d{4})(\d{0,4}).*/, "($1) $2-$3"); } 
    else if (telefone.length > 2) { telefone = telefone.replace(/^(\d{2})(\d{0,5})/, "($1) $2"); }
    input.value = telefone;
}