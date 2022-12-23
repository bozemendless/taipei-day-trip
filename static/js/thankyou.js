// Get order number from url
const orderNumber = location.search.slice(8);
const getOrderDataUrl = `/api/order/${orderNumber}`;

fetch(getOrderDataUrl)
.then(res => {return res.json();})
.then(data => {
    // If order number exists
    if (data.data !== null & data.data.status === 0) {
        // Fix RWD
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

        // Show words of thanks
        const thanksForPurchase = document.querySelector(".thanks-for-purchase");
        thanksForPurchase.textContent = "感謝您的購買";

        const orderNumberSpan = document.querySelector(".order-number");
        orderNumberSpan.textContent = data.data.number;

        // Render image
        const bookingImgDiv = document.querySelector(".booking-img");
        const img = document.createElement("img");
        img.src = data.data.trip.attraction.image;
        bookingImgDiv.appendChild(img);

        // Render attraction title
        const bookingTitleDiv = document.querySelector(".booking-title");
        const bookingTitleSpan = document.createElement("span");
        const bookingTitleTextNode = document.createTextNode(data.data.trip.attraction.name);
        bookingTitleSpan.appendChild(bookingTitleTextNode);
        bookingTitleDiv.appendChild(bookingTitleSpan);
        bookingTitleSpan.className = "button-bold";
        
        // Render date
        const bookingDateDiv = document.querySelector(".booking-date");
        const bookingDateSpan = document.createElement("span");
        const bookingDateTextNode = document.createTextNode(data.data.trip.date);
        bookingDateSpan.appendChild(bookingDateTextNode);
        bookingDateDiv.appendChild(bookingDateSpan);
        bookingDateSpan.className = "body-medium";

        // Render time
        let time;
        if (data.data.trip.time === "morning") {
            time = "早上 9 點到下午 1 點";
        }
        if (data.data.trip.time === "afternoon") {
            time = "下午 1 點到下午 5 點";
        }
        const bookingTimeDiv = document.querySelector(".booking-time");
        const bookingTimeSpan = document.createElement("span");
        const bookingTimeTextNode = document.createTextNode(time);
        bookingTimeSpan.appendChild(bookingTimeTextNode);
        bookingTimeDiv.appendChild(bookingTimeSpan);
        bookingTimeSpan.className = "body-medium";

        // Render price
        const bookingFeeDiv = document.querySelector(".booking-fee");
        const bookingFeeSpan = document.createElement("span");
        const bookingFeeTextNode = document.createTextNode(`${data.data.price} 元`);
        bookingFeeSpan.appendChild(bookingFeeTextNode);
        bookingFeeDiv.appendChild(bookingFeeSpan);
        bookingFeeSpan.className = "body-medium";

        // Render address
        const bookingPlaceDiv = document.querySelector(".booking-place");
        const bookingPlaceSpan = document.createElement("span");
        const bookingPlaceTextNode = document.createTextNode(data.data.trip.attraction.address);
        bookingPlaceSpan.appendChild(bookingPlaceTextNode);
        bookingPlaceDiv.appendChild(bookingPlaceSpan);
        bookingPlaceSpan.className = "body-medium";
    }

    // If order number not exist
    if (data.data === null | data.data.status !== 0) {
        // Show words of thanks
        const thanksForPurchase = document.querySelector(".thanks-for-purchase");
        thanksForPurchase.textContent = "Oops！您的訂單似乎出現錯誤。";
        const orderNumberSpan = document.querySelector(".order-number");
        orderNumberSpan.textContent = orderNumber;

        const contactWaring = document.querySelector(".contact-warning");
        contactWaring.style = "display: none";
        const noOrderNumberInformation = document.querySelector(".no-booking");
        noOrderNumberInformation.style = "display: block;";
    }
})