function updateTime() {
  var now = new Date();
  var options = { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric', 
      hour: '2-digit', 
      minute: '2-digit', 
      second: '2-digit',
      hour12: true  
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