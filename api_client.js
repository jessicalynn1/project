// imports api data and seeds it; call function from api_client file

function pokemonAPIFunction () {

    fetch('https://pokeapi.co/api/v2/berry/')
        .then(response => response.json())
        .then(data => {
            const results = data["results"]
            const berry_list = []
            const berries_html = document.querySelector("#berries");

            for (let i = 0; i < results.length; i += 1) {
                berry_list.push(results[i]["name"])
            }
            berries_html.textContent = berry_list;
        });
}

pokemonAPIFunction()