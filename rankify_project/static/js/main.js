$(document).ready(function(){

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!this.crossDomain) {
        //Security settting required by Django
        xhr.setRequestHeader("X-CSRFToken", $("[name=csrfmiddlewaretoken]").val());
      }
    }
  });

  window.onpopstate = function(e) {
    fetchPage(location.pathname);
    // history.pushState('', '', location.pathname);
  };

  $("input [type=submit]").click(function(event) {
    $(".loading").css("display", "inherit");
  });

  $(".ajaxLink").click(function(event) {
    event.preventDefault();
    var targetUrl = $(this).attr('href'),
      targetTitle = $(this).attr('title');
    if(window.location.pathname != targetUrl) {
      window.history.pushState({url: "" + targetUrl + ""}, targetTitle, targetUrl);
    }
    fetchPage(targetUrl);
  });
});

function fetchPage(targetUrl) {
  $.ajax({
    type: "GET",
    url: targetUrl,
    data: { ajax: "true"},
    success: function(result){
      pageLoaded(result, targetUrl);
    },
    error: function () {
      alert('There was an error connecting to our server. Check your internet connection and try again.');
    }
  });
}

function pageLoaded (data, url) {
    $(".intro-text").html(data);
    $("title").text($(".pageTitle").text());
}
