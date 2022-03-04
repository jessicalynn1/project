'use strict';
// console.log('js is working')

//ENDED UP NOT USING THIS!!
// imports api data and seeds it; call function from api_client file


// function DisneyData() {
//     fetch('https://api.themeparks.wiki/preview/parks/DisneylandResortMagicKingdom/waittime', {
//         headers: {
//             'Content-Type': 'application/json',
//             'Access-Control-Allow-Origin':'*',

//         },
//         mode: 'no-cors'
//     })
//     .then((response) => response.json())
//     .then((data) => {
//         console.log(data.results); 
//         return data
//     })
//     .then((data) => {
//         const results = data["results"]
//         const ride_list = []
//         const rides_html = document.querySelector("#rides");
//         for (let i = 0; i < results.length; i += 1) {
//             ride_list.push(results[i]["name"])
//         }
//         rides_html.textContent = ride_list;
//     })
//     .catch(console.error);
// }
    
// DisneyData()

