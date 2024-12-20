// Существующее CSS-правило: .hover-style:hover { color: red; }

let el = document.querySelector('.news_detail'); // Наш элемент
el.onmouseover = () => el.classList.add('news_detail'); // При наведении станет красным
el.onmouseout = () => el.classList.remove('news_detail'); // Возвращаем первоначальное состояние при уходе курсора