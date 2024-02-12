function filterProfiles() {
    const typeFilter = document.getElementById('typeFilter').value;
    const breedFilter = document.getElementById('breedFilter').value;
    const dispositionFilter = document.getElementById('dispositionFilter').value;
    const availabilityFilter = document.getElementById('availabilityFilter').value;
    const descriptionKeyword = document.getElementById('descriptionSearch').value.toLowerCase();

    // Assuming profiles are rendered and have data attributes for filtering
    const profiles = document.querySelectorAll('.profile'); // Ensure this selector matches your rendered profiles

    profiles.forEach(profile => {
        const type = profile.getAttribute('data-type');
        const breed = profile.getAttribute('data-breed');
        const disposition = profile.getAttribute('data-disposition');
        const availability = profile.getAttribute('data-availability');
        const description = profile.getAttribute('data-description').toLowerCase();

        const matchesFilters = (typeFilter === 'all' || type === typeFilter) &&
                                (breedFilter === 'all' || breed === breedFilter) &&
                                (dispositionFilter === 'all' || disposition === dispositionFilter) &&
                                (availabilityFilter === 'all' || availability === availabilityFilter) &&
                                description.includes(descriptionKeyword);

        profile.style.display = matchesFilters ? '' : 'none';
    });
}

function displayAnimals(animals) {
    const container = document.querySelector('.pets-container');
    container.innerHTML = ''; // Clear existing content
    animals.forEach(animal => {
        const element = document.createElement('div');
        element.className = 'pet-profile';
        element.innerHTML = `
            <img src="${animal.img}" alt="${animal.name}">
            <div class="info">
                <h3>${animal.name}</h3>
                <!-- Additional details here -->
            </div>
        `;
        container.appendChild(element);
    });
}

// Call this function initially to load all pets
filterPets();
