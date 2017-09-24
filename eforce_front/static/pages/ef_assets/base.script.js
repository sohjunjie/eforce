$(document).ready(function() {

  if(location.protocol == 'https:'){
    socket = new WebSocket("wss://" + window.location.host + "/efassets/");
  }else{
    socket = new WebSocket("ws://" + window.location.host + "/efassets/");
  }

  socket.onmessage = function(e) {

      var msg = push_django_msg_notification(JSON.parse(e.data));

      if(msg != ''){
        var notificationDesc = {notificationDesc: msg + "<br/> Please refresh!"}
        $("#pushNotificationTemplate").tmpl(notificationDesc).prependTo("#efassets_notification_wrapper");
      }

  }

});

function push_django_msg_notification(data){

    var return_msg;
    switch(data.created_type) {
        case 'crisis':
            return_msg = create_crisis_alert_msg(data);
            break;
        case 'group_instruction':

            break;
    }

    return return_msg;
}

function create_crisis_alert_msg(data){
    var return_msg = "";
    return_msg += "Crisis Alert: " + data.title;
    return return_msg;
}

function create_group_instruction_msg(data){

    var return_msg = "";

    var psuedo_groupname = $("#user-group-name").text()
    if(psuedo_groupname.trim() != data.readable_to_group_name)
      return return_msg;

    $.ajax({
      type: "GET",
      dataType: 'json',
      url: "api/v1.0/this/user/group/",
      success: function(ajax_data, status){
          ajax_data = ajax_data.data
          if(ajax_data.id == data.to_group_id){
            return_msg += "<b>" + data.for_crisis_title + "</b><br/>";
            return_msg += "Instruction alert: " + data.instruction_text + "<br/>";
          }
      },
      error: function(err) {console.log('error');}
    });

    return return_msg;

}
