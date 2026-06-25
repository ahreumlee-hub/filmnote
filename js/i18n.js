document.addEventListener('DOMContentLoaded', function () {
    const root = document.documentElement;
    const buttons = document.querySelectorAll('.lang-toggle button');
    const stored = localStorage.getItem('filmnoteLang');
    const initial = stored === 'en' ? 'en' : 'ko';

    function setLanguage(lang) {
        root.lang = lang;
        document.body.dataset.lang = lang;
        localStorage.setItem('filmnoteLang', lang);

        document.querySelectorAll('[data-ko][data-en]').forEach(function (node) {
            node.textContent = node.dataset[lang];
        });

        document.querySelectorAll('[data-hover-ko][data-hover-en]').forEach(function (node) {
            node.setAttribute('data-hover', node.dataset[lang === 'en' ? 'hoverEn' : 'hoverKo']);
        });

        buttons.forEach(function (button) {
            button.classList.toggle('is-active', button.dataset.lang === lang);
            button.setAttribute('aria-pressed', button.dataset.lang === lang ? 'true' : 'false');
        });
    }

    buttons.forEach(function (button) {
        button.addEventListener('click', function () {
            setLanguage(button.dataset.lang);
        });
    });

    setLanguage(initial);
});
