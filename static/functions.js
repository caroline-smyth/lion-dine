function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
}

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

updateTime();
setInterval(updateTime, 1000);

document.addEventListener('DOMContentLoaded', function() {
  const upvoteButtons = document.querySelectorAll('.fa.fa-solid.fa-circle-arrow-up');
  const downvoteButtons = document.querySelectorAll('.fa.fa-solid.fa-circle-arrow-down');
  upvoteButtons.forEach(function(button){
    button.addEventListener('click', function() {
      const votesElement = this.parentElement.querySelector('.vote-amount');
      //localStorage.setItem('votesElement', votesElement);
      if (votesElement) {
        let votes = parseInt(votesElement.innerHTML);
        votes += 1;
        votesElement.innerHTML = votes;
        reorder();
      }
      else {
        alert('error')
      }
    });
  });
  downvoteButtons.forEach(function(button){
    button.addEventListener('click', function() {
      const votesElement = this.parentElement.querySelector('.vote-amount');
      if (votesElement) {
        let votes = parseInt(votesElement.innerHTML);
        votes -= 1;
        votesElement.innerHTML = votes;
        reorder();
      }
      else {
        alert('error')
      }
    });
  });
});

function reorder() {
  cols = document.querySelectorAll('.col');
  cols.forEach(function(col){
    const menu = col.querySelector('.menu');
    const items = Array.from(menu.querySelectorAll('.item'));
    items.sort(function(a, b) {
      const votesA = parseInt(a.querySelector('.vote-amount').innerHTML);
      const votesB = parseInt(b.querySelector('.vote-amount').innerHTML);
      return votesB - votesA;
    });

    while(menu.firstChild) {
      menu.removeChild(menu.firstChild);
    }

    items.forEach(function(item) {
      menu.appendChild(item);
    });
  });
  
}

const form = document.getElementById("valentineForm");
    const linkContainer = document.getElementById("linkContainer");
    let generatedLink = "";

    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const formData = {
        senderName: document.getElementById("senderName").value,
        valentineName: document.getElementById("valentineName").value,
        diningHall: document.getElementById("diningHall").value,
        mealTime: document.getElementById("mealTime").value
      };

      try {
        const response = await fetch("/api/valentine", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData)
        });
        const data = await response.json();

        if (response.ok) {
          generatedLink = data.inviteLink;
          linkContainer.innerHTML = `
            <p>Your custom Valentine invitation link:</p>
            <a href="${generatedLink}" target="_blank">${generatedLink}</a>
          `;
        } else {
          linkContainer.innerHTML = `<p style="color:red;">Error: ${data.error || 'Unknown error'}</p>`;
        }
      } catch (err) {
        linkContainer.innerHTML = `<p style="color:red;">Something went wrong. Check console.</p>`;
        console.error(err);
      }
    });

document.addEventListener("DOMContentLoaded", function () {
  // Get modal elements
  const sellModal = document.getElementById("sellModal");
  const sellClose = document.getElementById("sellClose");
  const buyModal = document.getElementById("buyModal");
  const buyClose = document.getElementById("buyClose");

  // Attach event listener for seller listing buttons
  document.querySelectorAll(".sell-button").forEach(function (button) {
    button.addEventListener("click", function () {
      // Retrieve data attributes from the clicked button
      const otherName = button.getAttribute("data-other-name");
      const otherEmail = button.getAttribute("data-other-email");
      // Populate the hidden fields in the seller modal
      sellModal.querySelector("input[name='other_name']").value = otherName;
      sellModal.querySelector("input[name='other_email']").value = otherEmail;
      // Display the modal
      sellModal.style.display = "block";
    });
  });

  // Attach event listener for buyer listing buttons
  document.querySelectorAll(".buy-button").forEach(function (button) {
    button.addEventListener("click", function () {
      // Retrieve data attributes from the clicked button
      const otherName = button.getAttribute("data-other-name");
      const otherEmail = button.getAttribute("data-other-email");
      // Populate the hidden fields in the buyer modal
      buyModal.querySelector("input[name='other_name']").value = otherName;
      buyModal.querySelector("input[name='other_email']").value = otherEmail;
      // Display the modal
      buyModal.style.display = "block";
    });
  });

  // Close modal when clicking on the close icon
  sellClose.addEventListener("click", function () {
    sellModal.style.display = "none";
  });

  buyClose.addEventListener("click", function () {
    buyModal.style.display = "none";
  });

  // Close modal when clicking anywhere outside the modal content
  window.addEventListener("click", function (event) {
    if (event.target === sellModal) {
      sellModal.style.display = "none";
    }
    if (event.target === buyModal) {
      buyModal.style.display = "none";
    }
  });
});
