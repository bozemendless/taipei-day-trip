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
    const carousel = document.querySelector(".carousel");
    const img = document.createElement("img");
    img.src = data.data["images"][0];
    carousel.appendChild(img);

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
});



/*
//address ###
address:臺北市  北投區中山路、光明路沿線"

category
"養生溫泉"

description
"北投溫泉從日據時代便有盛名，深受喜愛泡湯的日人自然不會錯過，瀧乃湯、星乃湯、鐵乃湯就是日本人依照溫泉的特性與療效給予的名稱，據說對皮膚病、神經過敏、氣喘、風濕等具有很好的療效，也因此成為了北部最著名的泡湯景點之一。新北投溫泉的泉源為大磺嘴溫泉，泉質屬硫酸鹽泉，PH值約為3~4之間，水質呈黃白色半透明，泉水溫度約為50-90℃，帶有些許的硫磺味 。目前北投的溫泉旅館、飯店、會館大部分集中於中山路、光明路沿線以及北投公園地熱谷附近，總計約有44家，每一家都各有其特色，多樣的溫泉水療以及遊憩設施，提供遊客泡湯養生，而鄰近的景點也是非常值得造訪，例如被列為三級古蹟的三寶吟松閣、星乃湯、瀧乃湯以及北投第一家溫泉旅館「天狗庵」，都有著深遠的歷史背景，而北投公園、北投溫泉博物館、北投文物館、地熱谷等，更是遊客必遊的景點，來到北投除了可以讓溫泉洗滌身心疲憊，也可以順便了解到北投溫泉豐富的人文歷史。"

images
(6) ['https://www.travel.taipei/d_upload_ttn/sceneadmin/pic/11000848.jpg', 'https://www.travel.taipei/d_upload_ttn/sceneadmin/pic/11002891.jpg', 'https://www.travel.taipei/d_upload_ttn/sceneadmin/…/E70/F65/1e0951fb-069f-4b13-b5ca-2d09df1d3d90.JPG', 'https://www.travel.taipei/d_upload_ttn/sceneadmin/…538/F274/e7d482ba-e3c0-40c3-87ef-3f2a1c93edfa.JPG', 'https://www.travel.taipei/d_upload_ttn/sceneadmin/…767/F581/9ddde70e-55c2-4cf0-bd3d-7a8450582e55.jpg', 'https://www.travel.taipei/d_upload_ttn/sceneadmin/…891/F188/77a58890-7711-4ca2-aebe-4aa379726575.JPG']

name
: 
"新北投溫泉區"
transport
: 
"新北投站下車，沿中山路直走即可到達

*/