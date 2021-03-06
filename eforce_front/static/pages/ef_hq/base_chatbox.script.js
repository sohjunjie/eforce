var poll_crisis_chat_interval;
var poll_chat_max_id_interval;
var refresh_interval = 1000;
var chatmaxid = 0;

$(document).ready(function() {

  init_chatbox_crisis_list();

  event_on_send_chat_msg();

  event_start_poll_chat_max_id();

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
  poll_crisis_chat_interval = setInterval(poll_chatbox_conversation, refresh_interval);
}

function poll_chatbox_conversation(){

  let cmo_crisis_id = $("#msg_for_crisis_id").val();
  let api_url = CONST_CMO_DOMAIN + "cmowebservice/viewincidentchat.aspx?ID=" + cmo_crisis_id;

  $.ajax({
    type: "GET",
    dataType: 'json',
    url: api_url,
    success: function(data, status){

        var crisisChatMsgDetail;
        $("#cmo_chat_crisis_messages_lists").empty();
        if(data.length == 0) {
          $("#NoChatMessageTemplate").tmpl().appendTo("#cmo_chat_crisis_messages_lists");
        }

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

  let api_url = CONST_CMO_DOMAIN + "cmowebservice/viewincidentchat.aspx?ID=" + cmo_crisis_id;
  let cmo_crisis_title = $("#cmo_crisis_id_" + cmo_crisis_id + "_title").text();
  $("#msg_for_crisis_id").val(cmo_crisis_id);
  $("#cmo_chat_box_crisis_title").text(cmo_crisis_title);

  $.ajax({
    type: "GET",
    dataType: 'json',
    url: api_url,
    success: function(data, status){

        let crisisChatMsgDetail;
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

  let api_url = CONST_CMO_DOMAIN + "cmowebservice/viewincident.aspx?status=0";

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

  let api_maxchatid_url = CONST_CMO_DOMAIN + "cmowebservice/chatmaxid.aspx?ID=0";
  $.ajax({
    type: "GET",
    dataType: 'json',
    url: api_maxchatid_url,
    success: function(data, status){
        chatmaxid = data[0].TotalChatCount;
    },
    error: function(err) {
        console.log('error');
    }

  });

}

function toggle_chatbox_display() {
    let x = document.getElementById('cmo_chat_box');
    if (x.style.display === 'none') {
        x.style.display = 'block';
    } else {
        x.style.display = 'none';
    }
}

function event_start_poll_chat_max_id(){
  clearInterval(poll_chat_max_id_interval);
  poll_chat_max_id_interval = setInterval(onchange_chatmaxid_create_toast, refresh_interval);
}

function onchange_chatmaxid_create_toast(){
  let api_maxchatid_url = CONST_CMO_DOMAIN + "cmowebservice/chatmaxid.aspx?ID=0";
  $.ajax({
    type: "GET",
    dataType: 'json',
    url: api_maxchatid_url,
    success: function(data, status){
        if (chatmaxid != data[0].TotalChatCount) {
          $.toast("You have a new message from NESIMS chat");
          play_chat_notification_sound();
        }
        chatmaxid = data[0].TotalChatCount;
    },
    error: function(err) {
        console.log('error');
    }

  });
}

function play_chat_notification_sound(){
  let audio = new Audio(static_url + 'sounds/alert.mp3');
  audio.play();
}
