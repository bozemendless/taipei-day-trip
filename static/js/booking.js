const bookingUrl = "/api/booking"

// Get booking data
const attractionData = {
    "id": null,
    "name": null,
    "address": null,
    "image": null,
    "date": null,
    "time": null
};
function getBookingData() {
    fetch(bookingUrl)
    .then(res => {return res.json();})
    .then(data => {
        if (data.data !== null) {
            attractionData.id = data.data.attractions.id;
            attractionData.name = data.data.attractions.name;
            attractionData.address = data.data.attractions.address;
            attractionData.image = data.data.attractions.image;
            attractionData.date = data.data.date;
            attractionData.time = data.data.time;
            // Render img
            const bookingImgDiv = document.querySelector(".booking-img");
            const img = document.createElement("img");
            img.src = attractionData.image;
            bookingImgDiv.appendChild(img);
            // Render attraction name
            const bookingTitleDiv = document.querySelector(".booking-title");
            const bookingName = document.createElement("span");
            bookingName.className = "body-bold";
            const bookingNameText = document.createTextNode(attractionData.name);
            bookingName.appendChild(bookingNameText);
            bookingTitleDiv.appendChild(bookingName);
            // Render booking date
            const bookingDateDiv = document.querySelector(".booking-date");
            const bookingDateSpan = document.createElement("span");
            const bookingDateSpanText = document.createTextNode(attractionData.date);
            bookingDateSpan.className = "body-medium";
            bookingDateSpan.appendChild(bookingDateSpanText);
            bookingDateDiv.appendChild(bookingDateSpan);
            // Render booking time
            let time;
            if (data.data.time === "morning") {
                time = "早上 9 點到下午 1 點";
            }
            if (data.data.time ==="afternoon") {
                time = "下午 1 點到下午 5 點";
            }
            const bookingTimeDiv = document.querySelector(".booking-time");
            const bookingTimeSpan = document.createElement("span");
            const bookingTimeSpanText = document.createTextNode(time);
            bookingTimeSpan.className = "body-medium";
            bookingTimeSpan.appendChild(bookingTimeSpanText);
            bookingTimeDiv.appendChild(bookingTimeSpan);
            // Render booking price
            const bookingFeeInner = document.querySelector(".booking-fee-inner");
            const bookingFeeInnerText = document.createTextNode(data.data.price);
            bookingFeeInner.appendChild(bookingFeeInnerText);
            // Render booking address
            const bookingPlaceDiv = document.querySelector(".booking-place");
            const bookingPlaceSpan = document.createElement("span");
            const bookingPlaceSpanText = document.createTextNode(attractionData.address);
            bookingPlaceSpan.className = "body-medium";
            bookingPlaceSpan.appendChild(bookingPlaceSpanText);
            bookingPlaceDiv.appendChild(bookingPlaceSpan);
            // Show block when receiving data
            
            const hr = document.querySelectorAll("hr");
            const userContact = document.querySelector(".user-contact"); 
            const creditInformation = document.querySelector(".credit-information"); 
            const bookingPrice = document.querySelector(".booking-price") 
            const bookingButton = document.querySelector(".booking-button"); 
            const displayNoneArray = [userContact, creditInformation, bookingPrice, bookingButton];
            for (let i = 0; i < hr.length; i ++) {
                hr[i].style.display = "block";
            }
            displayNoneArray.forEach(element => {
                element.style.display = "block";}
            )

            const mediaQuery = window.matchMedia("screen and (min-width: 1200px)");
            const bookingFlexContainer = document.querySelector(".booking-flex-container");
            if (mediaQuery.matches) {
                bookingFlexContainer.style.display = "flex";
            } else {
                bookingFlexContainer.style.display = "block";
            }
            window.addEventListener("resize", () => {
                if (mediaQuery.matches) {
                    bookingFlexContainer.style.display = "flex";
                } else {
                    bookingFlexContainer.style.display = "block";
                }
            });
        }
        if (data.data === null) {
            const noBooking = document.querySelector(".no-booking");
            noBooking.style.display = "block";
        }
        
    });
}

// Create a new booking 
function createBooking() {
    const date = document.querySelector("#date-input");
    const firstHalfDay = document.querySelector("#first-half-day"); 
    const secondHalfDay = document.querySelector("#second-half-day");
    let time = null;
    let price = null;
    if (firstHalfDay.checked) {
        time = "morning";
        price = 2000;
    }
    if (secondHalfDay.checked) {
        time = "afternoon"
        price = 2500;
    }

    // Prevent repeated warning messages
    document.querySelectorAll('.blank-warning').forEach( warning => {
        warning.remove();
    });

    if (!firstHalfDay.checked & !secondHalfDay.checked) {
        const inputTimeDiv = document.querySelector(".time")
        const noTime = document.createElement("span");
        noTime.textContent = "請選擇時間";
        noTime.classList.add("blank-warning");
        inputTimeDiv.appendChild(noTime)
    }
    if (date.value === "") {
        const inputDateDiv = document.querySelector(".date");
        const noDate = document.createElement("span");
        noDate.textContent = "請選擇日期";
        noDate.classList.add("blank-warning");
        inputDateDiv.appendChild(noDate);
    }
    const attraction = {
        "attractionId": attractionId,
        "date": date.value,
        "time": time,
        "price": price
    }
    const options = {
        method: "POST",
        headers: {
        "Content-Type": "application/json"
        },
        body: JSON.stringify(attraction)
    };
    if (date.value !== "" & time !== null & price !== null) {
        fetch(bookingUrl, options)
        .then(res => {return res.json();})
        .then(data => {
        if (data.ok) {
            document.location.href = "/booking";
        }
    })
    }
}

function deleteBooking() {
    const options = {
        method: "DELETE"
    }
    fetch(bookingUrl, options)
    .then(res => {
        return res.json();
    })
    .then(data => {
        if (data.ok) {
            location.reload();
        }
        if (data.error) {
            console.log(data.message);
        }
    });
}


// Get booking data when loading /booking
if (location.pathname === "/booking") {
    getBookingData();
}

// DELETE booking
if (location.pathname === "/booking") {
    const deleteButton = document.querySelector(".delete-button");
    deleteButton.addEventListener("click", () => {
        deleteBooking();
    });
}