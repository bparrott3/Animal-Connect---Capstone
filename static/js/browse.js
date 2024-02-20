document.addEventListener('DOMContentLoaded', function() {
    fetchProfiles(); // Call this function initially to load all pets
});

function fetchProfiles() {
    fetch('/animal_profiles')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        displayProfiles(data); // Assumes your endpoint is adjusted to return JSON
    })
    .catch(error => console.error('Error fetching profiles:', error));
}

function filterProfiles() {
    fetchProfiles();
}

function displayProfiles(profiles) {
    const container = document.querySelector('.pets-container'); // Ensure this matches your HTML
    container.innerHTML = ''; // Clear existing profiles
    
    profiles.forEach(profile => {
        const profileElement = document.createElement('div');
        profileElement.className = 'pet-profile';
        profileElement.innerHTML = `
            <img src="${profile.image}" alt="Animal Image" style="width:100px; height:auto; margin-right: 20px;">
            <div>
                <div>Type: ${profile.type}</div>
                <div>Breed: ${profile.breed}</div>
                <div>Disposition: ${profile.disposition}</div>
                <div>Availability: ${profile.availability}</div>
                <div>Description: ${profile.description}</div>
            </div>
        `;
        container.appendChild(profileElement);
    });
}
