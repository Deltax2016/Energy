ymaps.ready(init);
var myMap;
var x;
var y;
var coords;



function myfunction () {
   var pot;
   
   pot=document.getElementById("in").value;

   document.getElementById("out").value=pot;

}

function httpGet(theUrl)
{
    var xhr = new XMLHttpRequest();
xhr.open("GET", theUrl, true);
xhr.onreadystatechange = function() {
  if (xhr.readyState == 4) {
    // JSON.parse does not evaluate the attacker's scripts.
    var resp = JSON.parse(xhr.responseText);
  }
}
xhr.send();
}

function init () {
    myMap = new ymaps.Map("map", {
        center: [57.5262, 38.3061], // Углич
        zoom: 11
    }, {
        balloonMaxWidth: 200,
        searchControlProvider: 'yandex#search'
    });

    // Обработка события, возникающего при щелчке
    // левой кнопкой мыши в любой точке карты.
    // При возникновении такого события откроем балун.
 /*  myMap.events.observe(myMap,myMap.events.click,function(){

  myCollection.removeAll();
});*/




    myMap.events.add('click', function (e) {
              coords = e.get('coords');
            x=coords[0].toPrecision(6);
            y=coords[1].toPrecision(6);
            console.log(x);
            console.log(y);
            var text = httpGet("https://maps.googleapis.com/maps/api/place/textsearch/json?query=river&radius=6000&language=ru&opennow&location="+x+","+y+"&key=AIzaSyDMkPyS3cWd1qIDDXYQHSLJ4PrV6ILkgVw");
            console.log(text);
            var myPlacemark = new ymaps.GeoObject({
                geometry: {
                    type: "Point",
                    coordinates: coords
                }
});
  myMap.geoObjects.removeAll(myPlacemark);
        myMap.geoObjects.add(myPlacemark);
    
var myCoords = coords;


    // Обработка события, возникающего при щелчке
    // правой кнопки мыши в любой точке карты.
    // При возникновении такого события покажем всплывающую подсказку
    // в точке щелчка.
    myMap.events.add('contextmenu', function (e) {
        myMap.hint.open(e.get('coords'), 'Кто-то щелкнул правой кнопкой');
    });
    
    // Скрываем хинт при открытии балуна.
    myMap.events.add('balloonopen', function (e) {
        myMap.hint.close();
    });
  
// После того как метка была создана, ее
// можно добавить на карту.

});
}

/*
   var myPlacemark = new ymaps.Placemark([57.5432, 38.3134], {
    // Хинт показывается при наведении мышкой на иконку метки.
    hintContent: 'Содержимое всплывающей подсказки',
    // Балун откроется при клике по метке.
    balloonContent: 'Содержимое балуна'
});

// После того как метка была создана, ее
// можно добавить на карту.
myMap.geoObjects.add(myPlacemark);
}
*/