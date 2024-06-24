ymaps.ready(init);

function init() {

    let myMap = new ymaps.Map("map", {
        center: [59.94, 30.39],
        zoom: 10
    }, {
        searchControlProvider: 'yandex#search'
    });

    let req = new XMLHttpRequest();
    req.open("GET", "/company_on_map/companies");
    req.send();

    req.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let companies = JSON.parse(this.responseText);

            for (const company of Object.values(companies)) {
                let object = ymaps.geocode(`${company['addr'][0]['PROVINCE']}, ${company['addr'][0]['CITY']}, ${company['addr'][0]['ADDRESS_1']}`)
                object.then(function (res) {
                    let coor = res.geoObjects.properties._data.metaDataProperty.GeocoderResponseMetaData.Point.coordinates
                    myMap.geoObjects.add(new ymaps.Placemark([coor[1], coor[0]], {balloonContent: `<strong>${company['title']}</strong>` + '\n' + `${company['addr'][0]['PROVINCE']}, ${company['addr'][0]['ADDRESS_1']}`},));
                })
            }
        }
    };


}