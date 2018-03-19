$(document).ready(function(){

  window.onpopstate = function(e) {
    $(".dynamic").empty();//not working
  };

  $(".ajaxLink").click(function(event) {
    event.preventDefault();
    var targetUrl = $(this).attr('href'),
      targetTitle = $(this).attr('title');
    if(window.location.pathname != targetUrl) {
      window.history.pushState({url: "" + targetUrl + ""}, targetTitle, targetUrl);
    }
    $.ajax({
      url: targetUrl,
      success: function(result){
        pageLoaded(result, targetUrl);
      },
      error: function () {
        alert('There was an error connecting to our server. Check your internet connection and try again.');
      }
    });
  });

});

function pageLoaded (data, url) {
  if(url == "/rankify/add_playlist/") {
    $(".addPlaylistArea").html(data);
  }
  else if (url == "/rankify/user/") {
    $(".userPlaylistsArea").html(data);
  }
  else if (url == "/rankify/rankings/") {
    $(".rankingsArea").html(data);
  }
}
