'use strict';

// imports api data and seeds it; call function from api_client file

// function testDisneyAPI () {

//     fetch('https://api.themeparks.wiki/preview/parks/DisneylandResortMagicKingdom/waittime')
//         .then(response => response.json())
//         .then(data => {
            // for (const ride of data) {
            //     document.querySelector("#rides")
            //     .insertAdjacentHTML("beforeend", `<li>${ride.name}</li>`);
            // }

            // const results = data["results"]
//             const ride_list = []
//             const rides_html = document.querySelector("#rides");

//             for (let i = 0; i < data.length; i += 1) {
//                 ride_list.push(data[i]["name"])
//             }
//             rides_html.textContent = ride_list;
//         });
// }

// testDisneyAPI()


function testDisneyAPI () {

    fetch("https://api.themeparks.wiki/preview/parks/DisneylandResortMagicKingdom/waittime")
    .then(response => response.json())
    .then(apiResponse => {
        for (const result of apiResponse.results) {
            document.querySelector("#rides").insertAdjacentHTML("beforeend", `<li>${result.name}</li>`);
            print(result)
        }
    });
}

testDisneyAPI()