window.addEventListener('scroll', function() {
    const box = document.getElementById('box');
    const scrollPosition = window.scrollY;

    if (scrollPosition === 0) {
        box.style.width = '852px'; // 스크롤 위치가 0일 때 너비 836px
    } else {
        box.style.width = '910px'; // 스크롤 위치가 1 이상일 때 너비 860px
    }
});
