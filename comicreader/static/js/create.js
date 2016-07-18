$( function() {
  $( "#sortable" ).sortable();
  $( "#sortable" ).disableSelection();
} );

$('#search-deviantart').keypress(function (e) {
  var key = e.which;
  if(key == 13){
    $("#progressbar").fadeTo(2000 , 100)
    $(this).blur();
    var url = $(this).val();
    getDeviantArt(url);
    $(this).attr("placeholder", url);
    $(this).val('');
    //stuff
    $("#progressbar").fadeTo(2000 , 0)
  }});

  function getDeviantArt(url) {
    $.ajax({
        url: '/fetch/url',
        data:{
          "address": url,
        },
        success: function(json) {
          console.log(json);
        }
    });
  }
