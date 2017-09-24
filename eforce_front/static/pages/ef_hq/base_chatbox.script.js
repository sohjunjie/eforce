var poll_crisis_chat_interval;

$(document).ready(function() {

  init_chatbox_crisis_list();

  event_on_send_chat_msg();

});

function event_on_send_chat_msg(){

  $( "#send_chat_msg_form" ).submit(function( e ) {

    var for_crisis_id = $("#msg_for_crisis_id").val();
    var this_sender = CONST_THIS_READABLE_USER_GROUP;
    var api_url = CONST_CMO_DOMAIN + "cmowebservice/responseincidentchat.aspx";

    if(for_crisis_id.trim() == ""){
        e.preventDefault();
        return
    }

    var payload = {
          Incident_ID: for_crisis_id,
          Sender: this_sender,
          Description: $("#msg_to_send").val()
    };

    $.ajax({
      type: "POST",
      data: payload,
      dataType: 'json',
      url: api_url,
      success: function(data, status){
          $("#msg_to_send").val("");
          load_chatbox_crisis_conversation(for_crisis_id, do_toggle=false);
      },
      error: function(err) {
          console.log('error');
      }

    });

    e.preventDefault();
  });

}


function event_start_poll_on_select_chat_crisis(){

  clearInterval(poll_crisis_chat_interval);
  poll_crisis_chat_interval = setInterval(poll_chatbox_conversation, 8000);
}


function poll_chatbox_conversation(){

  console.log('a');

  var cmo_crisis_id = $("#msg_for_crisis_id").val();
  var api_url = CONST_CMO_DOMAIN + "cmowebservice/viewincidentchat.aspx?ID=" + cmo_crisis_id;

  $.ajax({
    type: "GET",
    dataType: 'json',
    url: api_url,
    success: function(data, status){

        var crisisChatMsgDetail;
        $("#cmo_chat_crisis_messages_lists").empty();

        $.each(data, function(i, item){
                crisisChatMsgDetail = {
                  cmoCrisisId: cmo_crisis_id,
                  crisisMsgId: item.ID,
                  crisisChatSender: item.Sender,
                  crisisChatDate: item.Date,
                  crisisChatMsg: item.Description
                };

                if(item.Sender != CONST_THIS_READABLE_USER_GROUP){
                  $("#crisisChatMsgLeftTemplate").tmpl(crisisChatMsgDetail).appendTo("#cmo_chat_crisis_messages_lists");
                }else{
                  $("#crisisChatMsgRightTemplate").tmpl(crisisChatMsgDetail).appendTo("#cmo_chat_crisis_messages_lists");
                }
        });

        $("#cmo_chat_crisis_messages_lists").scrollTo($("#cmo_chat_crisis_messages_lists").children().last());

    },
    error: function(err) {
        console.log('error');
    }

  });

}


function load_chatbox_crisis_conversation(cmo_crisis_id, do_toggle=true){

  var api_url = CONST_CMO_DOMAIN + "cmowebservice/viewincidentchat.aspx?ID=" + cmo_crisis_id;
  $("#msg_for_crisis_id").val(cmo_crisis_id);

  $.ajax({
    type: "GET",
    dataType: 'json',
    url: api_url,
    success: function(data, status){

        var crisisChatMsgDetail;
        $("#cmo_chat_crisis_messages_lists").empty();

        $.each(data, function(i, item){
                crisisChatMsgDetail = {
                  cmoCrisisId: cmo_crisis_id,
                  crisisMsgId: item.ID,
                  crisisChatSender: item.Sender,
                  crisisChatDate: item.Date,
                  crisisChatMsg: item.Description
                };

                if(item.Sender != CONST_THIS_READABLE_USER_GROUP){
                  $("#crisisChatMsgLeftTemplate").tmpl(crisisChatMsgDetail).appendTo("#cmo_chat_crisis_messages_lists");
                }else{
                  $("#crisisChatMsgRightTemplate").tmpl(crisisChatMsgDetail).appendTo("#cmo_chat_crisis_messages_lists");
                }
        });

        if(do_toggle){
            $("#chatItemAndMsgToggler").click();
        }

        $("#cmo_chat_crisis_messages_lists").scrollTo($("#cmo_chat_crisis_messages_lists").children().last());

        event_start_poll_on_select_chat_crisis();

    },
    error: function(err) {
        console.log('error');
    }

  });


}

function init_chatbox_crisis_list(){

  var api_url = CONST_CMO_DOMAIN + "cmowebservice/viewincident.aspx?status=0";

  $.ajax({
    type: "GET",
    dataType: 'json',
    url: api_url,
    success: function(data, status){

        var crisisChatItemDetail;
        $("#cmo_chat_crisis_lists").empty();

        $.each(data, function(i, item){
                crisisChatItemDetail = {
                  cmoCrisisId: item.ID,
                  crisisDescription: item.Description,
                  crisisDate: item.Date,
                  crisisScale: item.Severity,
                  crisisLocAddress: item.Loc_Address
                };
                $("#crisisChatItemTemplate").tmpl(crisisChatItemDetail).appendTo("#cmo_chat_crisis_lists");
        });

    },
    error: function(err) {
        console.log('error');
    }

  });


}

function toggle_chatbox_display() {
    var x = document.getElementById('cmo_chat_box');
    if (x.style.display === 'none') {
        x.style.display = 'block';
    } else {
        x.style.display = 'none';
    }
}
