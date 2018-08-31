ymaps.ready(init);
var myMap;
var x;
var y;
var coords;
var coordsoftown;
var mesto;
var text;
var urlzapr;
var asd=['Саратовская область','Московская область'];
function myfunction () {
   var pot;
   pot=document.getElementById("in").value;
   var str1 = "<br>Ваши координаты: "
   if (mesto[0]=='Московская область'){
   document.getElementById("out").value='Мы не знаем Москву'} else {
    urlzapr="http://127.0.0.1:8000/api/VIBOR?region="+mesto[0].replace(" ","%20")+"&moshn="+pot+'&lng='+x+'&ltg='+y;
   console.log(mesto[0]);
   HttpGet(urlzapr);
   
}}

function HttpGet (aUrl) {
        var x = new XMLHttpRequest();
        x.open("GET", aUrl, true);
        x.onreadystatechange = function () {document.getElementById("out").value= x.responseText;}
        x.send(null);
    }


function init () {
    myMap = new ymaps.Map("map", {
        center: [69.2751, 173.048], // Углич
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
            var myPlacemark = new ymaps.GeoObject({
                geometry: {
                    type: "Point",
                    coordinates: coords
                }
});
  myMap.geoObjects.removeAll(myPlacemark);
  myMap.geoObjects.add(myPlacemark);          
 getAddress(coords);// выполняется только 429 раз!!!
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
function getAddress(coords) {
        ymaps.geocode(coords).then(function (res) {
            var firstGeoObject = res.geoObjects.get(0);
            mesto=firstGeoObject.getAdministrativeAreas();
            console.log(mesto[0]);
 });}