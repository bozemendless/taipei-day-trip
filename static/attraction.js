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
