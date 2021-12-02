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

/* Opens mentor details section in mentor matching results */
function openMentorDetails(mentor_id) {
   	var list = document.getElementById("details"+mentor_id);

     if(list.style.width == "0px"){
            list.style.display = "block";
            setTimeout(function(){
                list.style.width = "400px";
             }, 20);
        } else if(list.style.width == "400px") {
            list.style.width = "0px";
             setTimeout(function(){
                list.style.display = "none";
             }, 20);
        }
}

/* When the user clicks on a mentee name on the results page,
enter the name into the submission field*/
function enterMenteeName(clicked_id) {
  document.getElementById('id_menteeusername').value = clicked_id;
}