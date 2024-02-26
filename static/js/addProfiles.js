// document.getElementById('addProfileForm').addEventListener('submit', function(event) {
//     event.preventDefault(); // Prevent default form submission
    
//     const formData = new FormData(this);
    
//     // Optional: Convert formData to JSON if your backend expects JSON
//     // const formJSON = Object.fromEntries(formData.entries());

//     fetch('/insert_animal_profiles', {
//         method: 'POST',
//         body: formData // or JSON.stringify(formJSON) for JSON
//         // headers: { 'Content-Type': 'application/json' }, // Uncomment if sending JSON
//     })
//     .then(response => {
//         if (!response.ok) {
//             throw new Error('Network response was not ok');
//         }
//         return response.text(); // or .json() if your server responds with JSON
//     })
//     .then(data => {
//         console.log('Success:', data);
//         // Optionally redirect or inform the user of success
//     })
//     .catch(error => {
//         console.error('Error:', error);
//     });
// });

// document.getElementById('addProfileForm').addEventListener('submit', function(event) {
//     event.preventDefault(); // Prevent the default form submission

//     const formData = new FormData(this);

//     fetch('/insert_animal_profiles', {
//         method: 'POST',
//         body: formData,
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.success) {
//             // Show a success message to the user
//             alert('Success!'); // This is a simple way to show a message. For a better user experience, use custom modal or toast notifications.

//             // Redirect after 2 seconds
//             setTimeout(() => {
//                 window.location.href = '/shelter'; // Adjust the URL to where you want to redirect
//             }, 2000);
//         }
//     })
//     .catch(error => console.error('Error:', error));
// });

