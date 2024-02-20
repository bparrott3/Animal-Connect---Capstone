document.addEventListener('DOMContentLoaded', function() {
    fetchProfiles(); // Call this function initially to load all pets
});

function fetchProfiles() {
    const typeFilter = document.getElementById('typeFilter').value;
    const breedFilter = document.getElementById('breedFilter').value;
    // Include other filters as needed

    fetch(`/api/profiles?type=${typeFilter}&breed=${breedFilter}`)
    .then(response => response.json())
    .then(data => {
        displayProfiles(data); // Assumes your endpoint returns an array of profiles
    })
    .catch(error => console.error('Error fetching profiles:', error));
}

function filterProfiles() {
    // Fetch new profiles based on filter criteria
    // For demonstration, using the same function, but in practice, you might filter on the server or adjust the fetched dataset
    fetchProfiles(); 
}

function displayProfiles(profiles) {
    const container = document.querySelector('ul'); // Assuming the profiles will be displayed in a <ul>, adjust selector as needed
    container.innerHTML = ''; // Clear existing profiles

    profiles.forEach(profile => {
        const profileElement = document.createElement('li');
        profileElement.innerHTML = `
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
                <img src="${profile.image}" alt="Animal Image" style="width:100px; height:auto; margin-right: 20px;">
                <div>
                    <div>Type: ${profile.type}</div>
                    <div>Breed: ${profile.breed}</div>
                    <div>Disposition: ${profile.disposition}</div>
                    <div>Availability: ${profile.availability}</div>
                    <div>Description: ${profile.description}</div>
                </div>
            </div>
        `;
        container.appendChild(profileElement);
    });
}
