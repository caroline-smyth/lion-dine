// --- GOOGLE SIGN IN ---

//triggered when user signs in.
//gets user's basic profile info.
//hides sign in button.
function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
  document.getElementById('g_id_signin').style.display = 'none';

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
  localStorage.setItem('userEmail', responsePayload.email);

  //hide sign in button
  document.getElementById('g_id_signin').style.display = 'none';

  //display profile icon
  const profileIcon = document.getElementById('profile-icon');
  profileIcon.src = responsePayload.picture;
  document.getElementById('profile-menu').style.display = 'inline-block';

  //toggle dropdown
  profileIcon.addEventListener('click', function() {
    this.parentElement.classList.toggle('active');
  });

  console.log('User logged in:', responsePayload.email);  // Debug log
}

//removes user's google credential from localStorage when they sign out.
//also removes other information from localStorage.
function handleSignOut() {
  localStorage.removeItem('googleCredential');
  localStorage.removeItem('userName');
  localStorage.removeItem('userImage');
  localStorage.removeItem('userEmail');

  //hide profile icon and show sign in button
  document.getElementById('profile-menu').style.display = 'none';
  document.getElementById('g_id_signin').style.display = 'block';

  console.log('User logged out');  // Debug log

  google.accounts.id.revoke(localStorage.getItem('googleCredential'), done => {
    console.log('Token revoked');
  });
}


// --- UTILITY FUNCTIONS ---

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
  const currentTimeString = now.toLocaleString('en-US', options);
  document.getElementById('current-time').textContent = currentTimeString;
}

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

// --- INITIALIZATION AND EVENT LISTENERS ---

//checks if user is logged in when page loads.
//initialize time and set up event listeners.
window.onload = function() {
  const credential = localStorage.getItem('googleCredential');
  if (credential) {
    const payload = jwt_decode(credential);
    // Check if token is expired
    const expirationTime = payload.exp * 1000;
    if (Date.now() < expirationTime) {
      document.getElementById('g_id_signin').style.display = 'none';

      //display profile icon
      const profileIcon = document.getElementById('profile-icon');
      profileIcon.src = payload.picture;
      document.getElementById('profile-menu').style.display = 'inline-block';

      //toggle dropdown
      profileIcon.addEventListener('click', function() {
        this.parentElement.classList.toggle('active');
      });

      console.log('User is logged in:', payload.email);  // Debug log
    } else {
      // Token expired, remove it
      localStorage.removeItem('googleCredential');
      console.log('Token expired');  // Debug log
    }
  }

  //updates the time on the page immediately, then every second.
  updateTime();
  setInterval(updateTime, 1000);


  document.getElementById('postListingsButton').addEventListener('click', function(event) {
    const credential = localStorage.getItem('googleCredential');
    if (!credential) {
      event.preventDefault(); // Stop the default navigation.
      alert('Please sign in with your Columbia/Barnard email to post listings.');
      //window.location.href = '/market';
      document.getElementById('g_id_signin').style.display = 'block';
    }
  });
};

// attach click listeners to all contact buttons
document.querySelectorAll('.contact-button').forEach(function(button) {
  button.addEventListener('click', function(event) {
    //pull name/user from local storage set during signin
    var userName = localStorage.getItem('userName');
    var userEmail = localStorage.getItem('userEmail');

  // if not signed in, prompt to sign in
  if(!userName || !userEmail || (!userEmail.endsWith('@columbia.edu') && !userEmail.endsWith('@barnard.edu'))) {
    alert('Please sign in with your Columbia/Barnard email.')
    document.getElementById('g_id_signin').style.display='block';
    return;
  }

  //populate hidden fields in contact form
  document.getElementById('sender_name').value = userName;
  document.getElementById('sender_email').value = userEmail;

  //pull listing id from contact button
  var listingId = this.getAttribute('data-listing-id');
  if (listingId) {
    document.getElementById('listing_id').value = listingId;
  }

  //for debugging, display text in popup
  document.getElementById('userNameDisplay').textContent = userName;
  document.getElementById('userEmailDisplay').textContent = userEmail;

    document.getElementById('myForm').style.display = 'block';
  });
});

// Close the form when clicking outside of it
window.onclick = function(event) {
  const form = document.getElementById("myForm");
  if (event.target == form) {
    closeForm();
  }
}


