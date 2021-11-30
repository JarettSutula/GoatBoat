/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function myProfileDropdown() {
  document.getElementById("myProfileDropdown").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

/* When the user clicks on a mentor name on the results page,
enter the name into the submission field*/
function enterMentorName(clicked_id) {
  document.getElementById('id_mentorusername').value = clicked_id;
}