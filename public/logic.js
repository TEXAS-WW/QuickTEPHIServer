console.log("hello world from JS!!")


// Function to check authorization
function checkAuthorization() {
    const isAuthorized = sessionStorage.getItem('access') === 'permitted';
    if (!isAuthorized) {
        // Redirect to login or show an error message
        window.location.href = '/'; // or alert('You are not authorized');
    }
}


// Run the check before the page content loads
document.addEventListener('DOMContentLoaded', ()=> {
    const currentUrl = window.location.href;
    if (currentUrl.includes('dashboard')) {
        checkAuthorization()
    }
});



 // JavaScript to handle form submission and API call
 document.getElementById('accessForm').addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent the form from submitting the traditional way

  // Get the access code from the form
  const accessCode = document.getElementById('accessCode').value;

  // Make the API call to the Node.js server
  fetch('http://localhost:4000/verifyAccessCode', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ accessCode: accessCode })
  })
  .then( (response) => {
    if(!response.ok) throw new Error(response.status);
    else return response.json();
    //response.json()
    }
    )
  .then(data => {

      // Handle the response from the server
      document.getElementById('responseMessageSuccess').innerText = data.message;
      sessionStorage.setItem('access', 'permitted');
      setTimeout(()=>{
        window.location.href = '/dashboard';
      }, 1500)
  })
  .catch(error => {
      console.error('Error:', error);
      sessionStorage.setItem('access', '');
      document.getElementById('responseMessage').innerText = 'An error occurred. Please try again.';
  });
});


//-------------------------------------------



