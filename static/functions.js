/*
var dict = {
  JohnJay: [], JJs: [], Ferris: [], FacHouse: [], Mikes: [], Dons: [], GraceDodge: [], FacShack: [], Diana: [], Hewitt: []
};
for (var key in dict) {
  var value = dict[key];
  var random = Math.floor(Math.random()* 15 + 1) 
  for (let i = 0; i < random; i++) { 
    value.push("food " + i);
  }
}
console.log(dict);

document.getElementById('output').innerHTML = "hello";
*/
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