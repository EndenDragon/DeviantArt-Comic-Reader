$( function() {
  $( "#sortable" ).sortable();
  $( "#sortable" ).disableSelection();
} );

function getQueryParameters()
{
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}

$( document ).ready(function() {
    queryparameters = getQueryParameters();
    if (queryparameters.hasOwnProperty('url')) {
      $('#search-deviantart').val(decodeURIComponent(queryparameters["url"]));
      $("#progressbar").fadeTo(2000 , 100)
      var url = $('#search-deviantart').val();
      $('#search-deviantart').attr("placeholder", url);
      $('#search-deviantart').val('');
      getDeviantArt(url);
      $("#progressbar").fadeTo(2000 , 0)
    }
});

$('#search-deviantart').keypress(function (e) {
  var key = e.which;
  if(key == 13){
    $("#progressbar").fadeTo(2000 , 100)
    $(this).blur();
    var url = $(this).val();
    $(this).attr("placeholder", url);
    $(this).val('');
    getDeviantArt(url);
    $("#progressbar").fadeTo(2000 , 0)
  }});

function getDeviantArt(url) {
  $.ajax({
      url: '/fetch/url',
      data:{
        "address": url,
      },
      success: function(json) {
        if (json['is_valid_url']) {
          if (json['type'] == 'art') {
            fetchArt(json['uuid'])
          }
          if (json['type'] == 'favorites') {
            fetchFavorites(json['uuid'], json['username'])
          }
          if (json['type'] == 'gallery') {
            fetchGallery(json['uuid'], json['username'])
          }
        } else {
          Materialize.toast('Invalid DeviantArt URL Address!', 4000)
        }
      },
      error: function() {
        Materialize.toast('An error has occured while fetching URL!', 4000)
      }
  });
}

function fetchArt(uuid) {
  $.ajax({
      url: '/fetch/art',
      data:{
        "deviationid": uuid,
      },
      async: false,
      success: function(json) {
        if (json['error'] == true) {
          Materialize.toast('An error has occured while fetching art URL: ' + json['message'], 4000)
        }
        userid = userIdOperation(json['art']['author']['userid'], json['art']['author']['username'], json['art']['author']['usericon'])
        artOperation(json['art'], userid)
      },
      error: function() {
        Materialize.toast('An error has occured while fetching art URL!', 4000)
      }
  });
}

function fetchFavorites(uuid, username) {
  $.ajax({
      url: '/fetch/favorite',
      data:{
        "favoriteid": uuid,
        "username": username
      },
      async: false,
      success: function(json) {
        if (json['error'] == true) {
          Materialize.toast('An error has occured while fetching art URL: ' + json['message'], 4000)
        }
        for (var i = 0; i < json['favorite'].length; i++) {
          arrjson = json['favorite'][i]
          userid = userIdOperation(arrjson['author']['userid'], arrjson['author']['username'], arrjson['author']['usericon'])
          artOperation(arrjson, userid)
        }
      },
      error: function() {
        Materialize.toast('An error has occured while fetching art URL!', 4000)
      }
  });
}

function fetchGallery(uuid, username) {
  $.ajax({
      url: '/fetch/gallery',
      data:{
        "folderid": uuid,
        "username": username
      },
      async: false,
      success: function(json) {
        if (json['error'] == true) {
          Materialize.toast('An error has occured while fetching art URL: ' + json['message'], 4000)
        }
        for (var i = 0; i < json['favorite'].length; i++) {
          arrjson = json['favorite'][i]
          userid = userIdOperation(arrjson['author']['userid'], arrjson['author']['username'], arrjson['author']['usericon'])
          artOperation(arrjson, userid)
        }
      },
      error: function() {
        Materialize.toast('An error has occured while fetching art URL!', 4000)
      }
  });
}

function userIdOperation(uuid, username, iconurl) {
  var uid;
  $.ajax({
      url: '/database/deviationusers',
      data:{
        "method": "uuid",
        "uuid": uuid,
      },
      async: false,
      success: function(json) {
        if (json.hasOwnProperty('id')) {
          if (json['username'] != username || json['iconurl'] != iconurl) {
            $.ajax({
                url: '/database/deviationusers-update',
                data:{
                  "userid": json['id'],
                  "username": username,
                  "iconurl": iconurl
                },
                type: 'POST',
                success: function(json) {
                  uid = json['id']
                },
                error: function() {
                  Materialize.toast('An error has occured while fetching user URL [POST-UPDATE]!', 4000)
                }
            });
          }
          uid = json['id']
        }
        else {
          $.ajax({
              url: '/database/deviationusers',
              data:{
                "useruuid": uuid,
                "username": username,
                "iconurl": iconurl
              },
              type: 'POST',
              success: function(json) {
                uid = json['id']
              },
              error: function() {
                Materialize.toast('An error has occured while fetching user URL [POST]!', 4000)
              }
          });
        }
      },
      error: function() {
        Materialize.toast('An error has occured while fetching user URL!', 4000)
      }
  });
  return uid;
}

function artOperation(art, userid) {
  var thumbs = art['thumbs']
  thumbs = thumbs[thumbs.length - 1]
  $.ajax({
      url: '/database/deviations',
      data:{
        "method": "uuid",
        "uuid": art['deviationid'],
      },
      async: false,
      success: function(json) {
        if (json.hasOwnProperty('id')) {
          if (art['title'] != json['title'] || art['is_mature'] != json['mature'] || art['content']['height'] != json['height'] || art['content']['width'] != json['width'] || art['content']['src'] != json['srcurl'] || art['url'] != json['link'] || thumbs['src'] != json['thumb_src'] || thumbs['height'] != json['thumb_height'] || thumbs['width'] != json['thumb_width']) {
            $.ajax({
                url: '/database/deviations-update',
                data:{
                  "id": json['id'],
                  "title": art['title'],
                  "mature": art['is_mature'],
                  "height": art['content']['height'],
                  "width": art['content']['width'],
                  "srcurl": art['content']['src'],
                  "link": art['url'],
                  "thumb_src": thumbs['src'],
                  "thumb_height": thumbs['height'],
                  "thumb_width": thumbs['width']
                },
                type: 'POST',
                success: function(json) {
                  insertArt(json['id'], art)
                },
                error: function() {
                  Materialize.toast('An error has occured while fetching art URL [POST-UPDATE]!', 4000)
                }
            });
          }
          insertArt(json['id'], art)
        }
        else {
          $.ajax({
              url: '/database/deviations',
              data:{
                "uuid": art['deviationid'],
                "title": art['title'],
                "userid": userid,
                "mature": art['is_mature'],
                "published_time": art['published_time'],
                "height": art['content']['height'],
                "width": art['content']['width'],
                "srcurl": art['content']['src'],
                "link": art['url'],
                "thumb_src": thumbs['src'],
                "thumb_height": thumbs['height'],
                "thumb_width": thumbs['width']
              },
              type: 'POST',
              success: function(json) {
                insertArt(json['id'], art)
              },
              error: function() {
                Materialize.toast('An error has occured while fetching art URL [POST]!', 4000)
              }
          });
        }
      },
      error: function() {
        Materialize.toast('An error has occured while fetching art URL!', 4000)
      }
  });
}

function insertArt(id, art) {
  var thumbs = art['thumbs']
  thumbs = thumbs[thumbs.length - 1]
  var data = {
      id: id,
      src: thumbs['src'],
      url: art['url'],
      title: art['title'],
      author: art['author']['username']
  };
  var template = $('#hidden-template').html();
  var html = Mustache.to_html(template, data);
  $('#sortable').append(html);
}
