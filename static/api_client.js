'use strict';
console.log('js is working')

// imports api data and seeds it; call function from api_client file

// res = requests.get('https://api.themeparks.wiki/preview/parks/DisneylandResortMagicKingdom/waittime')
// response = json.loads(res.text)

// for i in response:
//     print(i['name'])

// return render_template("rides.html")


function DisneyData() {
    fetch('https://api.themeparks.wiki/preview/parks/DisneylandResortMagicKingdom/waittime', {
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin':'*',

        },
        mode: 'no-cors'
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data.results); 
        return data
    })
    .then((data) => {
        const results = data["results"]
        const ride_list = []
        const rides_html = document.querySelector("#rides");
        for (let i = 0; i < results.length; i += 1) {
            ride_list.push(results[i]["name"])
        }
        rides_html.textContent = ride_list;
    })
    .catch(console.error);
}
    
DisneyData()





// const Themeparks = require("themeparks");

// const DisneylandResort = new ThemeParks.Parks.DisneylandResortMagicKingdom();


// const CheckWaitTimes = () => {
//     DisneylandResortMagicKingdom.GetWaitTimes().then((rideTimes) => {
//         rideTimes.forEach((ride) => {
//             console.log(`${ride.name}: ${ride.waitTime} minutes wait (${ride.status})`);
//         });
//     }).catch((error) => {
//         console.error(error);
//     }).then(() => {
//         setTimeout(CheckWaitTimes, 1000 * 60 * 5); 
//     });
// };
// CheckWaitTimes();


// const Parks = {};
// for (const park in ThemeParks.Parks) {
//   Parks[park] = new ThemeParks.Parks[park]();
// }

// // print each park's name, current location, and timezone
// for (const park in Parks) {
//   console.log(`* ${Parks[park].Name} [${Parks[park].LocationString}]: (${Parks[park].Timezone})`);
// }








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


// function testDisneyAPI () {

//     fetch("https://api.themeparks.wiki/preview/parks/DisneylandResortMagicKingdom/waittime", {mode: 'no-cors'})
//     .then(response => response.json())
//     .then(apiResponse => {
//         console.log(apiResponse)
        // for (const result of apiResponse.results) {
        //     document.querySelector("#rides").insertAdjacentHTML("beforeend", `<li>${result.name}</li>`);
        //     print(result)
        //     console.log(result)
        // }
//     })
// };

// testDisneyAPI()
