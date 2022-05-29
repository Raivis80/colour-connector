var colorCollapsible = document.getElementById("color-block");
colorCollapsible.addEventListener("show.bs.collapse", function () {
  picker = document.querySelectorAll(".color-picker");
  document.querySelector("#color-collapse-btn").classList.add("active");
  this.addEventListener("hide.bs.collapse", function () {
    document.querySelector("#color-collapse-btn").classList.remove("active");
  });
  picker.forEach((mood) => {
    mood.addEventListener("click", function () {
        document.querySelector("#color-input").value =
          this.style.backgroundColor;
          document.querySelector("#color-change-form").submit();
      },{ once: true });
  });
});


var moodCollapsible = document.getElementById("mood-block");
moodCollapsible.addEventListener("show.bs.collapse", function () {
  picker = document.querySelectorAll(".mood-picker");
  document.querySelector("#mood-collapse-btn").classList.add("active");
  this.addEventListener("hide.bs.collapse", function () {
    document.querySelector("#mood-collapse-btn").classList.remove("active");
  });
  picker.forEach((mood) => {
    mood.addEventListener("click", function () {
      document.querySelector("#mood-input").value = this.dataset.mood;
      document.querySelector("#mood-change-form").submit();
    }, { once: true });
    });
});


// Send message
function choice(elem) {
  allElements = document.getElementsByClassName("color-picker-friend");
  var color = elem.style.backgroundColor;
  document.getElementById("color").value = color;
  elem.classList.add("active");
  for (var i = 0; i < allElements.length; i++) {
    if (allElements[i] != elem) {
      allElements[i].classList.remove("active");
    }
  }
}




