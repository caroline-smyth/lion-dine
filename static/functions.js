//triggered when user signs in.
//gets user's basic profile info.
//hides sign in button.
function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
  document.getElementById('signInButton').style.display = 'none';

}

//gets user's google credential and stores it in localStorage.
function handleCredentialResponse(response) {
  // Decode the credential response
  const responsePayload = jwt_decode(response.credential);

  //enforce columbia/barnard email
  if (!responsePayload.email.endsWith('@columbia.edu') && !responsePayload.email.endsWith('@barnard.edu')) {
    alert('Please use your Columbia or Barnard email to sign in.');
    return;
  }
  
  // Store the credential in localStorage
  localStorage.setItem('googleCredential', response.credential);
  localStorage.setItem('userName', responsePayload.name);
  localStorage.setItem('userImage', responsePayload.picture);
  
  // Change background color to light blue when logged in
  document.body.style.backgroundColor = '#e6f3ff';  // light blue
  console.log('User logged in:', responsePayload.email);  // Debug log
}

//removes user's google credential from localStorage when they sign out.
function handleSignOut() {
  localStorage.removeItem('googleCredential');
  
  // Change background back to white when logged out
  document.body.style.backgroundColor = 'white';
  console.log('User logged out');  // Debug log

  google.accounts.id.revoke(localStorage.getItem('googleCredential'), done => {
    console.log('Token revoked');
  });
}

//checks if user is logged in when page loads.
//if user is logged in, changes background color to light blue.
window.onload = function() {
  const credential = localStorage.getItem('googleCredential');
  if (credential) {
    const payload = jwt_decode(credential);
    // Check if token is expired
    const expirationTime = payload.exp * 1000;
    if (Date.now() < expirationTime) {
      document.body.style.backgroundColor = '#e6f3ff';  // light blue
      document.getElementById('signInButton').style.display = 'none';
      console.log('User is logged in:', payload.email);  // Debug log
    } else {
      // Token expired, remove it
      localStorage.removeItem('googleCredential');
      document.body.style.backgroundColor = 'white';
      console.log('Token expired');  // Debug log
    }
  }
};

//updates the time on the page.
function updateTime() {
  var now = new Date();
  var options = { 
      weekday: 'short', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric', 
      hour: '2-digit', 
      minute: '2-digit', 
      hour12: true,
      timeZone: 'America/New_York'
  };
  var currentTimeString = now.toLocaleString('en-US', options);
  document.getElementById('current-time').textContent = currentTimeString;
}

//updates the time on the page immediately, then every second.
updateTime();
setInterval(updateTime, 1000);

//closes the form when the user clicks outside of it.
function closeForm() {
  document.getElementById("myForm").style.display = "none";
}

//opens popup form when button is clicked,
//and populates the form with the listing id.
function openForm(button) {
  const form = document.getElementById("myForm");
  const listingIdInput = form.querySelector('input[name="listing_id"]');
  const listingId = button.getAttribute('data-listing-id');
  
  listingIdInput.value = listingId;
  form.style.display = "block";
}

// Close the form when clicking outside of it
window.onclick = function(event) {
  const form = document.getElementById("myForm");
  if (event.target == form) {
    closeForm();
  }
}