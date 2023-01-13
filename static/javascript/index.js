//!calling api for searching any keyword
function Search(value) {
    var value = document.getElementsByClassName("index__search")[0].value
    if (value == "") {
        value = document.getElementsByClassName("index__search")[1].value
    }

    let users = [];
    fetch('/searchkey', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                key: value
            })
        })
        .then(response => response.json())
        .then(data => {
            if (window.getComputedStyle(document.getElementsByClassName("search__container")[0], null).display == "block") {
                const parent = document.getElementsByClassName("search__users")[0];
                func(data.Users, parent)
            } else {
                const parent = document.getElementsByClassName("search__users")[1];
                func(data.Users, parent)
            }
        });
    // var data = await response.json();
}

function func(users, parent) {
    if (users == undefined) {
        parent.innerHTML = "";
    }
    parent.innerHTML = "";
    for (let i = 0; i < users.length; i++) {
        const box = `
                            <a href="/${users[i][0]}" class="searched__user d-flex">
                                    <div class="searched__user__profile">
                                        <span class="text-profile profile__image" style="transform:translateY(2px);">${users[i][0][0]}</span>
                                    </div>
                                    <div class="searched__user__name">
                                        <span class="span1 text-light">${users[i][0]}</span>
                                        <span class="span2 text-light">${users[i][1]}</span>
                                    </div>
                                    </a>
                                   
                                    
                                    `;
        // document.body.innerHTML = box;
        parent.innerHTML += box;
    }
}

//! disabling the search box if clicked outside
document.addEventListener("click", (e) => {
    if (e.target.id != "search_keyword" && e.target.id != "search_users") {
        DisableSearch()
    }
})

function DisableSearch() {
    if (window.getComputedStyle(document.getElementsByClassName("search__container")[0], null).display == "block") {
        const parent = document.getElementsByClassName("search__users")[0];
        parent.innerHTML = "";
    } else {
        const parent = document.getElementsByClassName("search__users")[1];
        parent.innerHTML = "";
    }
}

//function to adding class list
var labels = document.getElementsByTagName('LABEL');

function findLabel(htmlfor) {
    for (var i = 0; i < labels.length; i++) {
        if (labels[i].htmlFor == htmlfor) {
            //  if (elem)
            //     elem.label = labels[i];
            return labels[i];
        }
    }
}
//! Searching ends here






//?for email label transition
document.getElementById("email").addEventListener("focus", () => {
    var ele = findLabel("email");
    ele.style.transform = "translate(5px, 17px)"

})
document.getElementById("email").addEventListener("blur", () => {
    var ele = findLabel("email");
    var input_value = document.getElementById("email").value;
    if (input_value == "") ele.style.transform = "translate(5px, 40px)"
})

//?for password label transition
document.getElementById("password").addEventListener("focus", () => {
    var ele = findLabel("password");
    ele.style.transform = "translate(5px, 17px)"
})
document.getElementById("password").addEventListener("blur", () => {
    var ele = findLabel("password");
    var input_value = document.getElementById("password").value;
    if (input_value == "") ele.style.transform = "translate(5px, 40px)"
})

//? for username label transition
document.getElementById("username").addEventListener("focus", () => {
    var ele = findLabel("username");
    ele.style.transform = "translate(5px, 17px)"
})
document.getElementById("username").addEventListener("blur", () => {
    var ele = findLabel("username");
    var input_value = document.getElementById("username").value;
    if (input_value == "") ele.style.transform = "translate(5px, 40px)"
})

//?for confirm_password label transition
document.getElementById("password_confirm").addEventListener("focus", () => {
    var ele = findLabel("password_confirm");
    ele.style.transform = "translate(5px, 17px)"
})
document.getElementById("password_confirm").addEventListener("blur", () => {
    var ele = findLabel("password_confirm");
    var input_value = document.getElementById("password_confirm").value;
    if (input_value == "") ele.style.transform = "translate(5px, 40px)"
})


function checkValuesOfLabels() {
    let input_value1 = document.getElementById("email").value;
    var ele = findLabel("email");
    if (input_value1 == "") ele.style.transform = "translate(5px, 40px)";
    else {
        ele.style.transform = "translate(5px, 17px)";
    }

    let input_value2 = document.getElementById("password").value;
    var ele = findLabel("password");
    if (input_value2 == "") ele.style.transform = "translate(5px, 40px)";
    else {
        ele.style.transform = "translate(5px, 17px)";
    }

    let input_value3 = document.getElementById("username").value;
    var ele = findLabel("username");
    if (input_value3 == "") ele.style.transform = "translate(5px, 40px)";
    else {
        ele.style.transform = "translate(5px, 17px)";
    }

    let input_value4 = document.getElementById("password_confirm").value;
    var ele = findLabel("password_confirm");
    if (input_value4 == "") ele.style.transform = "translate(5px, 40px)";
    else {
        ele.style.transform = "translate(5px, 17px)";
    }
}
checkValuesOfLabels()



//?read more and read less function in javascript




function expandDescription(e) {
    const id = e.target.dataset.id;
    const desc_id = "description" + id;
    e.target.style.display = "none";
    const readless_id = "readless" + id;
    document.getElementById(readless_id).style.display = "inline-block";
    const element = document.getElementById(desc_id);
    element.style.height = "auto";
}


function shrinkDescription(e) {
    const id = e.target.dataset.id;
    const desc_id = "description" + id;
    e.target.style.display = "none";
    const readless_id = "readmore" + id;
    document.getElementById(readless_id).style.display = "inline-block";
    const element = document.getElementById(desc_id);
    element.style.height = "45px";
}

function slide(id, mainId, hideID1, hideId2) {
    document.getElementById(id).click();
    document.getElementById(mainId).style.width = "80%";
    document.getElementById(hideID1).style.width = "0";
    document.getElementById(hideId2).style.width = "0";
}