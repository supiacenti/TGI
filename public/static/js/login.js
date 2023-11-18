const wrapper = document.querySelector(".wrapper"),
      signupHeader = document.querySelector(".signup header"),
      loginHeader = document.querySelector(".login header");
    loginHeader.addEventListener("click", () => {
      wrapper.classList.add("active");
    });
    signupHeader.addEventListener("click", () => {
      wrapper.classList.remove("active");
    });
    document.addEventListener("DOMContentLoaded", function () {
      const urlParams = new URLSearchParams(window.location.search);
      const autoClick = urlParams.get('autoclick');

      if (autoClick) {
        const loginHeader = document.querySelector(".login header");
        loginHeader.click();
      }
    });
    function validarSenha() {
      var senha = document.getElementById("passtohash").value;
      var regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{10,}$/;

      if (!regex.test(senha)) {
        alert("The password must contain at least one capital letter, one special symbol, numbers and be at least 10 characters long.");
        return false;
      }

      return true;
    }

    document.getElementById("signupForm").onsubmit = validarSenha;
    function validarEmail() {
      var email = document.getElementById("email").value;
      var regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;

      if (!regex.test(email)) {
        alert("Please enter a valid email address.");
        return false;
      }

      return true;
    }

    document.getElementById("signupForm").onsubmit = function () {
      return validarSenha() && validarEmail();
    };