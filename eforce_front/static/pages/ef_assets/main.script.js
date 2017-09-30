$( document ).ready(function() {

  // scroll to and expand crisis boxes automatically when navigating url with #crisis_id
  if(window.location.hash) {
      $("#crisis_instruction_wrapper").scrollTo(window.location.hash);
      $(window.location.hash + "_instructions").collapse('toggle');
  }

});


function mark_instruction_as_read(instr_id){


  $.ajax({
    type: "POST",
    dataType: 'json',
    url: "/api/v1.0/instruction/" + instr_id + "/mark/read/",
    beforeSend: function(xhr, settings) {
        $.ajaxSettings.beforeSend(xhr, settings);
    },
    success: function(data, status){

      $("#instruction_id_" + instr_id).find("i").removeClass('fa-circle-o');
      $("#instruction_id_" + instr_id).find("i").addClass('fa-check');

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
