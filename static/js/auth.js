const signinSignupButton = document.querySelector(".signin-signup-button");
const logoutButton = document.querySelector(".logout")
const signinDiv = document.querySelector(".sign-in");
const signupDiv = document.querySelector(".sign-up");
const lightBoxMask = document.querySelector(".lightbox-mask");
const closeButton = document.querySelectorAll(".close-button");
const switchToSignup = document.querySelector(".switch-to-signup");
const switchToSignin = document.querySelector(".switch-to-signin");
const signinButton = document.querySelector(".signin-button");
const signupButton = document.querySelector(".signup-button");
const signinEmail = document.querySelector("#signin-email");
const signinPassword = document.querySelector("#signin-password");
const signupName = document.querySelector("#signup-name");
const signupEmail = document.querySelector("#signup-email");
const signupPassword = document.querySelector("#signup-password");
const signinMessage = document.querySelector(".signin-message");
const signupMessage = document.querySelector(".signup-message");
const signinMessageSpan = document.querySelector(".signin-message span");
const signupMessageSpan = document.querySelector(".signup-message span");
const directToBookingButton = document.querySelector(".direct-to-booking-button");

signinSignupButton.addEventListener("click", () => {
    signinDiv.style.visibility = "visible";
    lightBoxMask.style.visibility = "visible";
})

for (let i = 0; i < closeButton.length; i ++) {
    closeButton[i].addEventListener("click", () => {
        signinDiv.style.visibility = "hidden";
        signupDiv.style.visibility = "hidden";
        lightBoxMask.style.visibility = "hidden";
    })
}

switchToSignup.addEventListener("click", () => {
    signinDiv.style.visibility = "hidden";
    signupDiv.style.visibility = "visible";
    signinEmail.value = "";
    signinPassword.value = "";
    signinDiv.className = "sign-in";
    signupDiv.className = "sign-up";
    signinMessageSpan.innerText = "";
})

switchToSignin.addEventListener("click", () => {
    signinDiv.style.visibility = "visible";
    signupDiv.style.visibility = "hidden";
    signupName.value = "";
    signupEmail.value = "";
    signupPassword.value = "";
    signinDiv.className = "sign-in";
    signupDiv.className = "sign-up";
    signupMessageSpan.innerText = "";
})

lightBoxMask.addEventListener("click", () => {
    signinDiv.style.visibility = "hidden";
    signupDiv.style.visibility = "hidden";
    lightBoxMask.style.visibility = "hidden";
    signinEmail.value = "";
    signinPassword.value = "";
    signupName.value = "";
    signupEmail.value = "";
    signupPassword.value = "";
    signinDiv.className = "sign-in";
    signupDiv.className = "sign-up";
    signinMessageSpan.innerText = "";
    signupMessageSpan.innerText = "";
})

// Check if logging status is valid
const getStatusUrl = "/api/user/auth";
fetch(getStatusUrl)
.then(res => {return res.json();})
.then(data => {
    if (data.data === null) {
        signinSignupButton.style.display = "list-item";
        directToBookingButton.addEventListener("click", () => {
            signinSignupButton.click();
        })
    }
    if (data.data !== null) {
        signinSignupButton.style.display = "none";
        logoutButton.style.display = "list-item";
        directToBookingButton.addEventListener("click", () => {
            location.href = "/booking"
        })
    }
    if (data.data !== null & location.pathname === "/booking") {
        const usernameSpan = document.querySelector(".username");
        const usernameSpanText = document.createTextNode(data.data.name);
        usernameSpan.appendChild(usernameSpanText);
    }
    if (data.data === null & location.pathname === "/booking") {
        document.location.href = "/";
    }
    const startBookButton = document.querySelector(".start-book-button");
    if (data.data !== null & location.pathname.startsWith("/attraction/")) {
        startBookButton.addEventListener("click", () => {
            createBooking();
        })
    }
    if (data.data === null & location.pathname.startsWith("/attraction")) {
        startBookButton.addEventListener("click", () => {
            signinSignupButton.click();
        })
    }
})

signinButton.addEventListener("click", () => {
    const signinUrl = "/api/user/auth";
    const user = {
        "email": signinEmail.value,
        "password": signinPassword.value
    }
    const options = {
        method: "PUT",
        headers: {
        "Content-Type":'application/json;charset=utf-8'
        },
        body: JSON.stringify(user)
    };
    fetch(signinUrl, options)
    .then(res => {return res.json();})
    .then(data => {
        if (!data.ok) {
            signinDiv.className = "sign-in signin-message30";
            signinMessageSpan.innerText = data.message;
            signinMessage.className = "signin-message fail";
        }
        if (data.ok) {
            location.reload();
        }
    });
});

signupButton.addEventListener("click", () => {
    const signupUrl = "/api/user";
    const user = {
        "name": signupName.value,
        "email": signupEmail.value,
        "password": signupPassword.value
    }
    const options = {
        method: "POST",
        headers: {
        "Content-Type":'application/json;charset=utf-8'
        },
        body: JSON.stringify(user)
    };
    fetch(signupUrl, options)
    .then(res => {return res.json();})
    .then(data => {
        if (!data.ok) {
            signupDiv.className = "sign-up signup-message30";
            signupMessageSpan.innerText = data.message;
            signupMessage.className = "signup-message fail";
        }
        if (data.ok) {
            signupMessage.className = "signup-message success";
            signupDiv.className = "sign-up signup-message30";
            signupMessageSpan.innerText = "註冊成功";
        }
    })
});

logoutButton.addEventListener("click", () => {
    const logoutUrl = "/api/user/auth";
    const options = {
        method: "DELETE",
    }
    fetch(logoutUrl, options)
    .then((res) => {return res.json();})
    .then((data) => {
        if (data.ok) {
            location.reload();
        }
    });
});