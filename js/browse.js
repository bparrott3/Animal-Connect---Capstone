document.addEventListener('DOMContentLoaded', () => {
    loadAnimals();
});

function loadAnimals() {
    // Placeholder for where we will fetch animal data from the back-end
    const animals = [
        { name: "Max", type: "Dog", breed: "Labrador", img: "/path/to/image" },
        // Add more animals
    ];

    const container = document.querySelector('.pets-container');
    animals.forEach(animal => {
        const element = document.createElement('div');
        element.className = 'pet-profile';
        element.innerHTML = `
            <img src="${animal.img}" alt="${animal.name}">
            <div class="info">
                <h3>${animal.name}</h3>
                <p>${animal.type} - ${animal.breed}</p>
            </div>
        `;
        container.appendChild(element);
    });
}
