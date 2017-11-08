$( document ).ready(function() {

  jQuery.extend({
    getQueryParameters : function(str) {
  	  return (str || document.location.search).replace(/(^\?)/,'').split("&").map(function(n){return n = n.split("="),this[n[0]] = n[1],this}.bind({}))[0];
    }
  });

  // scroll to and expand crisis boxes automatically when navigating url with #crisis_id
  if(window.location.hash) {
      $("#crisis_instruction_wrapper").scrollTo(window.location.hash);
      var queryParams = $.getQueryParameters(location.search);
      $(window.location.hash + "_" + queryParams["target"]).collapse('toggle');
  }

});

// TODO: ADD API FOR MARK CRISIS READ
function mark_crisis_as_read(crisis_id){


  $.ajax({
    type: "POST",
    dataType: 'json',
    url: "/api/v1.0/crisis/" + crisis_id + "/mark/read/",
    beforeSend: function(xhr, settings) {
        $.ajaxSettings.beforeSend(xhr, settings);
    },
    success: function(data, status){

      $("#crisis_id_" + crisis_id).closest("i").removeClass('fa-circle-o');
      $("#crisis_id_" + crisis_id).closest("i").addClass('fa-check');

    },
    error: function(err) {
        console.log(err);
    }

  });

}

// TODO: ADD API FOR MARK COMBAT STRATEGY READ
function mark_combat_strategy_as_read(combat_strategy_id){


  $.ajax({
    type: "POST",
    dataType: 'json',
    url: "/api/v1.0/strategy/" + combat_strategy_id + "/mark/read/",
    beforeSend: function(xhr, settings) {
        $.ajaxSettings.beforeSend(xhr, settings);
    },
    success: function(data, status){

      $("#strategy_id_" + combat_strategy_id).find("i").removeClass('fa-circle-o');
      $("#strategy_id_" + combat_strategy_id).find("i").addClass('fa-check');

    },
    error: function(err) {
        console.log(err);
    }

  });

}

// TODO: ADD API FOR MARK EFASSETS UPDATE READ
function mark_efassets_update_as_read(efassets_update_id){


  $.ajax({
    type: "POST",
    dataType: 'json',
    url: "/api/v1.0/efassets/update/" + efassets_update_id + "/mark/read/",
    beforeSend: function(xhr, settings) {
        $.ajaxSettings.beforeSend(xhr, settings);
    },
    success: function(data, status){

      $("#efupdate_id_" + efassets_update_id).find("i").removeClass('fa-circle-o');
      $("#efupdate_id_" + efassets_update_id).find("i").addClass('fa-check');

    },
    error: function(err) {
        console.log(err);
    }

  });

}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});
