document.addEventListener('DOMContentLoaded', function() {
    fetchProfiles(); // Call this function initially to load all pets
});

function fetchProfiles() {
    // Placeholder: Replace with actual AJAX call to fetch profiles
    const profiles = [
        { name: "Buddy", type: "Dog", breed: "Labrador", disposition: "Friendly", availability: "Available", description: "Loves walks", image: "buddy.jpg" },
        { name: "Whiskers", type: "Cat", breed: "Siamese", disposition: "Shy", availability: "Adopted", description: "Quiet and loves to cuddle", image: "whiskers.jpg" },
        // Add more profiles as needed
    ];

    displayProfiles(profiles);
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
