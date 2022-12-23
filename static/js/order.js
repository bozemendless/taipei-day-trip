TPDirect.setupSDK(
    126888,
    "app_xwno92WRuemQPm4SgQBuWxDo6Vts4uop9AE3rQQRtcO26Mdv5WrLTLuM8uEJ",
    "sandbox"
);

// Display ccv field
let fields = {
    number: {
        // css selector
        element: '#card-number',
        placeholder: '**** **** **** ****'
    },
    expirationDate: {
        // DOM object
        element: document.getElementById('card-expiration-date'),
        placeholder: 'MM / YY'
    },
    ccv: {
        element: '#card-ccv',
        placeholder: 'ccv'
    }
}

TPDirect.card.setup({
    fields: fields,
    styles: {
        // Style all elements
        'input': {
            'color': 'gray'
        },
        // style valid state
        '.valid': {
            'color': 'green'
        },
        // style invalid state
        '.invalid': {
            'color': 'red'
        },
        // Media queries
        // Note that these apply to the iframe, not the root window.
        '@media screen and (max-width: 400px)': {
            'input': {
                'color': 'orange'
            }
        }
    },
    // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
    isMaskCreditCardNumber: true,
    maskCreditCardNumberRange: {
        beginIndex: 6,
        endIndex: 11
    }
})

TPDirect.card.onUpdate(function (update) {
    const submitButton = document.querySelector("#submit");
    // update.canGetPrime === true
    // --> you can call TPDirect.card.getPrime()
    if (update.canGetPrime) {
        // Enable submit Button to get prime.
        submitButton.removeAttribute("disabled");
    } else {
        // Disable submit Button to get prime.
        submitButton.setAttribute('disabled', true)
    }

})

function onSubmit(event) {
    event.preventDefault()

    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus()

    // 確認是否可以 getPrime
    if (tappayStatus.canGetPrime === false) {
        alert('can not get prime')
        return
    }

    // Get prime
    TPDirect.card.getPrime((result) => {
        if (result.status !== 0) {
            alert('get prime error ' + result.msg)
            return
        }
        // alert('get prime 成功，prime: ' + result.card.prime)

        // send prime to your server, to pay with Pay by Prime API .

        const orderUrl = "/api/orders";
        const ordersData = {
            "prime": result.card.prime,
            "order": {
                "price": 2000,
                "trip": {
                "attraction": {
                    "id": attractionData.id,
                    "name": attractionData.name,
                    "address": attractionData.address,
                    "image": attractionData.image
                },
                "date": attractionData.date,
                "time": attractionData.time
                },
                "contact": {
                "name": document.querySelector("#contact-name-input").value,
                "email": document.querySelector("#contact-email-input").value,
                "phone": document.querySelector("#contact-phone-input").value
                }
            }
        }
        const options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(ordersData),
        };
        fetch(orderUrl, options)
        .then(res => {return res.json();})
        .then(data => {
            const orderNumber = data.data.number;
            location.href = `/thankyou?number=${orderNumber}`;
        })
        // Pay By Prime Docs: https://docs.tappaysdk.com/tutorial/zh/back.html#pay-by-prime-api
    })
}