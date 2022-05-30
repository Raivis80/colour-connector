
if (window.location.pathname === "/profile"){
  var colorCollapsible = document.getElementById("color-block");
  colorCollapsible.addEventListener("show.bs.collapse", function () {
    let picker = document.querySelectorAll(".color-picker");
    document.querySelector("#color-collapse-btn").classList.add("active");
    this.addEventListener("hide.bs.collapse", function () {
      document.querySelector("#color-collapse-btn").classList.remove("active");
    });
    picker.forEach((color) => {
      color.addEventListener("click", function () {
        this.classList.add("active");
        for (var i = 0; i < picker.length; i++) {
          if (picker[i] != this) {
            picker[i].classList.remove("active");
          }
        }
      });
    });
  });


  var moodCollapsible = document.getElementById("mood-block");
  moodCollapsible.addEventListener("show.bs.collapse", function () {
    let picker = document.querySelectorAll(".mood-picker");
    document.querySelector("#mood-collapse-btn").classList.add("active");
    this.addEventListener("hide.bs.collapse", function () {
      document.querySelector("#mood-collapse-btn").classList.remove("active");
    });
    picker.forEach((mood) => {
      mood.addEventListener("click", function () {
        this.classList.add("active");
        for (var i = 0; i < picker.length; i++) {
          if (picker[i] != this) {
            picker[i].classList.remove("active");
          }
        }
      });
      });
  });
};

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

// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        document.querySelector(".color-invalid").classList.remove("d-block");
        var color = document.getElementById("color").value;
        if (form.checkValidity() && color !== "") {
          // trigger custom event hx-trigger="bs-send"
        	htmx.trigger(form, "bsSend");
          console.log('bsSend')
          form.submit();
          
        }
        if (color === "") {
          event.preventDefault();
          event.stopPropagation();
          document.querySelector(".color-invalid").classList.add("d-block");
        }
        console.log('prevent')       
        event.preventDefault()
        event.stopPropagation()

        form.classList.add('was-validated')
      }, false)
    })
})()




