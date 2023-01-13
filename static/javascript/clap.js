function clapped(id, isClapped) {
    if (isClapped == false) {

        fetch(`/unclap/${id}`, {
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

    } else {
        fetch(`/clap/${id}`, {
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
                document.location.reload(true)
                console.log(data)
            });
    }
}