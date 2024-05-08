const dropdowns = document.querySelectorAll('.header-dropdown')

Array.prototype.forEach.call(dropdowns, dropdown => {
    const select = dropdown.querySelector('.header-select');
    const caret = dropdown.querySelector('.header-caret');
    const menu = dropdown.querySelector('.header-drop-menu');
    const options = dropdown.querySelectorAll('.header-drop-menu li');
    const selected = dropdown.querySelector('.header-selected');

    select.addEventListener('click', () => {
        select.classList.toggle('header-select-clicked');
        caret.classList.toggle('header-caret-rotate');
        menu.classList.toggle('header-drop-menu-open');
    });
    options.forEach(option => {
        option.addEventListener('click', () => {
            selected.innerText = option.innerText;
            select.classList.remove('header-select-clicked');
            caret.classList.remove('header-caret-rotate');
            menu.classList.remove('header-drop-menu-open');
            options.forEach(option => {
                option.classList.remove('active');
            });
            option.classList.add('active');
        });
    });
});