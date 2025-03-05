//js for other offshoot projects

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

function openForm(button) {
  if (button) {
    const listingId = button.getAttribute('data-listing-id');
    document.querySelector("#myForm input[name='listing_id']").value = listingId;
  }
  document.getElementById("myForm").style.display = "block";
}
