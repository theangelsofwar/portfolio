const config=require('./src/config');
const Twit=require('twit');



const Bot=new Twit(config)

///setting time intervals
var thirtyMinutes=1800000
var hourly=3600000
var tenminutes=600000
var minut=60000
var fortyFiveSeconds=45000
var tenSeconds=10000
//follow satan, others users that have corresponding hastags to boohoo,prettylittlething,nastygal, pacsun, hollister, abercrombie
//universe, spaceX, techno music, political controversies, plant rights

function getTrendAndFollow(){



    //get list of trending hashtags
    // https://developer.twitter.com/en/docs/trends/trends-for-location/api-reference/get-trends-place.html
}