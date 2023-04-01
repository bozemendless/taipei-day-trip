// attraction.html
// the different amount as the selection of first-half-day(NTD 2,000) or second-half-day(NTD 2,500)
const firstHalfDay = document.querySelector("#first-half-day");
const secondHalfDay = document.querySelector("#second-half-day");
const fee2000 = document.querySelector(".fee-2000");
const fee2500 = document.querySelector(".fee-2500");

firstHalfDay.addEventListener("click", () => {
    fee2000.style.visibility = "visible";
    fee2500.style.visibility = "hidden";
});

secondHalfDay.addEventListener("click", () => {
    fee2500.style.visibility = "visible";
    fee2000.style.visibility = "hidden";
});

const attractionId = location.pathname.split("/")[2];
const url = `/api/attraction/${attractionId}`;

fetch(url).then(res => {
    return res.json();
}).then(data => {
    // image
    const pics = document.querySelector(".pics");
    for (let i = 0; i < data.data["images"].length; i ++) {
        const picWrapper = document.createElement("div");
        picWrapper.className = "pic-wrapper";
        const img = document.createElement("img");
        img.src = data.data["images"][i];
        picWrapper.appendChild(img);
        pics.appendChild(picWrapper);
    }

    // spots
    const spots = document.querySelector(".spots");
    for (let i = 0; i < data.data["images"].length; i ++) {
        const spot = document.createElement("div");
        spot.className = "spot";
        spots.appendChild(spot);
    }

    // title
    const attractionTitleDiv = document.querySelector(".attraction-title");
    const title = document.createElement("span");
    title.className = "h3-bold";
    const titleText = document.createTextNode(data.data["name"]);
    title.appendChild(titleText);
    attractionTitleDiv.appendChild(title);

    // category and mrt
    const attractionSideDiv = document.querySelector(".attraction-side");
    const sideInfo = document.createElement("span");
    sideInfo.className = "body-medium";
    const sideInfoText = document.createTextNode(`${data.data["category"]} at ${data.data["mrt"]}`);
    sideInfo.appendChild(sideInfoText);
    attractionSideDiv.appendChild(sideInfo);

    // description
    const descriptionDiv = document.querySelector(".description");
    const descriptionP = document.createElement("p");
    descriptionP.className = "content-regular";
    const descriptionPText = document.createTextNode(data.data["description"]);
    descriptionP.appendChild(descriptionPText);
    descriptionDiv.appendChild(descriptionP);

    // address
    const addressDiv = document.querySelector(".address");
    const addressP = document.createElement("p");
    addressP.className = "content-regular";
    const addressPText = document.createTextNode(data.data["address"]);
    addressP.appendChild(addressPText);
    addressDiv.appendChild(addressP);

    // transport
    const transportDiv = document.querySelector(".transport");
    const transportP = document.createElement("p");
    transportP.className = "content-regular";
    const transportPText = document.createTextNode(data.data["transport"]);
    transportP.appendChild(transportPText);
    transportDiv.appendChild(transportP);

    // carousel function
    let count = 0;
    
    const allSpot = document.querySelectorAll(".spot");
    const firstSpot = allSpot[0];
    firstSpot.className = "spot current-spot";

    // declare spotUpdate function: update 'normal' and 'current' spot style
    function spotUpdate() {
        allSpot.forEach(spot => {
            spot.className = "spot";
        });
        allSpot[count].className = "spot current-spot";
    };

    // add all spot buttons event listening to capture which is clicked
    for (let i = 0; i < allSpot.length; i ++) {
        allSpot[i].addEventListener("click", () => {
            count = i;
            pics.style.transform = `translateX(-${count * 100}%)`; // if button was clicked, it will move to corresponding image
            spotUpdate();
        })
    }

    // rightBtn
    const rightBtn = document.querySelector(".right");
    rightBtn.addEventListener("click", () => {
        if (count === data.data["images"].length -1) { // rule for dealing with carousel order
            count = -1;
        }
        count += 1;
        pics.style.transform = `translateX(-${count * 100}%)`;

        spotUpdate();
    });

    // leftBtn
    const leftBtn = document.querySelector(".left");
    leftBtn.addEventListener("click", () => {
        if (count === 0) { // rule for dealing with carousel order
            count = data.data["images"].length;
        }
        count -= 1;
        pics.style.transform = `translateX(-${count * 100}%)`;

        spotUpdate();
    });
});

// Restrict booking date cannot be past time
if (location.pathname.startsWith("/attraction/")) {
    const now = new Date();
    if (now.getDate() < 10) {
        date = "0" + now.getDate().toString();
    } else {
        date = now.getDate();
    }
    
    if (now.getMonth() < 9) {
        month = "0" + (now.getMonth() + 1).toString();
    } else {
        month = now.getMonth() + 1;
    }

    year = now.getFullYear();
    const yyyymmdd = `${year}-${month}-${date}`;
    const dateInput = document.querySelector("#date-input");
    dateInput.setAttribute("min", yyyymmdd);
}