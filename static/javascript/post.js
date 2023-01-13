const element = document.getElementsByClassName("drop__zone__element")[0];
const inputElement = document.getElementById("formFile");

element.addEventListener("dragover", (e) => {
    e.preventDefault()
    element.classList.remove("dashed-border")
})
element.addEventListener("dragleave", (e) => {
    element.classList.add("dashed-border")
})
element.addEventListener("drop", (e) => {
    e.preventDefault()
    if (e.dataTransfer.files.length) {

        inputElement.files = e.dataTransfer.files

        updateThumbNail(element, e.dataTransfer.files[0])
    }
})
element.addEventListener("click", (e) => {
    inputElement.click()
})
inputElement.addEventListener("change", (e) => {
    if (inputElement.files.length) {
        element.classList.remove("dashed-border")
        updateThumbNail(element, inputElement.files[0])
    }
})

const reader = new FileReader();

function updateThumbNail(element, file) {
    const label = document.getElementById("file_label");
    label.innerHTML = file.name

    if (file.type.startsWith("image/")) {

        reader.readAsDataURL(file);
        reader.onload = () => {
            const drop_zone = document.getElementById("droped__image");
            var img = document.createElement('img');
            img.src = reader.result
            drop_zone.innerHTML = "";
            drop_zone.appendChild(img);
            drop_zone.style.height = "auto"
            img.style.width = "100%"
            img.style.height = "200px"
        }
    }


}


function postEdit(id) {
    fetch(`/editblog/${id}`, {
        method: 'GET',
        headers: {
            'Content-Type': "application/json"
        },
        body: Json.stringfy({
            key: null
        }).then(response => response.json()).then(data => console.log(data))

    })
}