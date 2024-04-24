const extendedSearchForm = document.getElementById('extendedSearchForm');
const categorySelect = document.getElementById('category');
const tagCheckboxes = document.querySelectorAll('.tag-search input[type="checkbox"]');

function saveSelection() {
    const selectedCategoryValue = categorySelect.value;
    const selectedCategoryText = categorySelect.options[categorySelect.selectedIndex].textContent;
    localStorage.setItem('selectedCategory', JSON.stringify({
        value: selectedCategoryValue,
        text: selectedCategoryText
    }));

    const selectedTags = [];
    tagCheckboxes.forEach(function (checkbox) {
        if (checkbox.checked) {
            selectedTags.push({value: checkbox.value, text: checkbox.nextSibling.textContent.trim()});
        }
    });
    localStorage.setItem('selectedTags', JSON.stringify(selectedTags));
}

function loadSelection() {
    const savedCategory = JSON.parse(localStorage.getItem('selectedCategory'));
    if (savedCategory) {
        categorySelect.value = savedCategory.value;
    }

    const savedTags = JSON.parse(localStorage.getItem('selectedTags'));
    if (savedTags) {
        savedTags.forEach(function (savedTag) {
            const tagCheckbox = document.querySelector(`.tag-search input[value="${savedTag.value}"]`);
            if (tagCheckbox) {
                tagCheckbox.checked = true;
            }
        });
    }
}

window.addEventListener('load', function () {
    loadSelection();
});

extendedSearchForm.addEventListener('change', function () {
    saveSelection();
});

categorySelect.addEventListener('change', function () {
    extendedSearchForm.submit()
});