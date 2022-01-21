// imports api data and seeds it; call function from api_client file

function testDisneyAPI () {

    fetch('https://api.themeparks.wiki/preview/parks/DisneylandResortMagicKingdom/waittime')
        .then(response => response.json())
        .then(data => {
            const results = data["results"]
            const ride_list = []
            const rides_html = document.querySelector("#rides");

            for (let i = 0; i < results.length; i += 1) {
                ride_list.push(results[i]["name"])
            }
            rides_html.textContent = ride_list;
        });
}

testDisneyAPI()