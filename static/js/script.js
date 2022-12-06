const targetElement = document.querySelector(".target-element");
let page = 0;
let nextPage;
let keyword = null;
let url = `/api/attractions?page=${page}`;
let isLoading = false;
const searchButton = document.querySelector(".button");
const categoryList = document.querySelector(".category-list");
const clear = document.querySelector(".clear");

// Get data function
function getAttractionsData() {
    url = `/api/attractions?page=${page}`;
    if (keyword !== null) {
        url += `&keyword=${keyword}`;
    }
    isLoading = true;

    fetch(url).then(function(res) {
        return res.json();
    }).then(function(data) {
        nextPage = data["nextPage"];
        page = nextPage;
        for (let i = 0; i < data.data.length; i++) {
            const attractions = document.querySelector(".attractions");
            const attraction = document.createElement("div");
            const attractionPage = document.createElement("a");
            const img = document.createElement("img");
            const mask = document.createElement("div");
            const title = document.createElement("span");
            const titleText = document.createTextNode(data.data[i]["name"]);
            const text = document.createElement("div");
            const mrt = document.createElement("span");
            const mrtText = document.createTextNode(data.data[i]["mrt"]);
            const category = document.createElement("span");
            const categoryText = document.createTextNode(data.data[i]["category"]);

            attraction.className = "attraction";

            img.src = data.data[i]["images"][0];
            img.alt = `${data.data[i]["name"]} 的景點頁面`;
            img.title = `${data.data[i]["name"]} 的景點頁面`;
            attractionPage.href = `/attraction/${data.data[i]["id"]}`;
            attractionPage.appendChild(img);
            attraction.appendChild(attractionPage);//

            title.appendChild(titleText);
            title.className = "title";
            mask.className = "mask";
            mask.title = `${data.data[i]["name"]}`;
            mask.appendChild(title);
            attraction.appendChild(mask);

            mrt.appendChild(mrtText);
            mrt.className = "mrt";
            text.appendChild(mrt);

            category.appendChild(categoryText);
            category.className = "category";
            text.appendChild(category);

            text.className = "text";
            attraction.appendChild(text);

            attractions.appendChild(attraction);
        }
        if (data.data.length === 0) {
            const attractions = document.querySelector(".attractions");
            attractions.innerText = "查無資料";
            attractions.style.fontSize = "20px";
        }
        isLoading = false;
    })
};

// Search function
searchButton.addEventListener("click", () => {
    page = 0;
    document.querySelectorAll(".attraction").forEach(child => {
        child.remove();
    })
    keyword = document.querySelector("#input").value;
    getAttractionsData();
    categoryList.style.visibility = "hidden";
    clear.style.visibility = "hidden";
});

// Get data when loading index page
getAttractionsData();

function callback(entry) {
    if (entry[0].isIntersecting & page !== null & isLoading === false) {
        getAttractionsData();
    }
};

// IntersectionObserver API
const options = {
    root: null,
    rootMargin: '0px',
    threshold: [0]
};

let observer = new IntersectionObserver(callback, options);

observer.observe(targetElement);

// Get categories list data and collapse function
const categoryUrl = "/api/categories";
fetch(categoryUrl).then(function (res) {
    return res.json();
}).then(function (data) {
    // Generate category list
    for (let i = 0; i < data.data.length; i ++) {
        const category = document.createElement("div");
        category.className = "categoryName";
        const categoryText = document.createTextNode(data.data[i]);
        category.appendChild(categoryText);
        categoryList.appendChild(category);
    }

    // Category collapse
    const input = document.querySelector("#input");
    input.addEventListener("click", () => {
        categoryList.style.visibility = "visible";
        clear.style.visibility = "visible";
    });

    clear.addEventListener("click", () => {
        categoryList.style.visibility = "hidden";
        clear.style.visibility = "hidden";
    });

    // Get user click value of category list
    categoryList.addEventListener("click", (targetElement) => {
        if (targetElement.target.className === "categoryName") {
            const text = targetElement.target.innerText;
            input.value = text;
            categoryList.style.visibility = "hidden";
            clear.style.visibility = "hidden";
        }
    }) 
});