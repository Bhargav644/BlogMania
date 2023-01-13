document.getElementById("profile__upload").addEventListener("mouseover", () => {
    document.getElementById("camera-icon").style.display = "inline-block";
})
document.getElementById("profile__upload").addEventListener("mouseout", () => {
    document.getElementById("camera-icon").style.display = "none";
})

document.getElementById("profile__upload").addEventListener("click", () => {
    document.getElementById("profile__upload__input").click();
})

document.getElementById("profile__upload__input").addEventListener("change", () => {
    document.getElementById("profile__upload__submit").click();
});

const toastTrigger = document.getElementById('liveToastBtn')
const toastLiveExample = document.getElementById('liveToast')
if (toastTrigger) {
    // toastTrigger.addEventListener('click', () => {
    function showToast(id, title) {
        document.getElementById("blog-title-toast").innerHTML = title.toUpperCase();
        document.getElementById("blog-id-toast").innerHTML = id;
        const toast = new bootstrap.Toast(toastLiveExample)
        toast.show()
    }
    // })
}


function deleteblog() {
    const id = document.getElementById("blog-id-toast").innerHTML;
    console.log(id)
    fetch(`/deleteblog/${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                key: null
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            document.location.reload(true)
        });
}