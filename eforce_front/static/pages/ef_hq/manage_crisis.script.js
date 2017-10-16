var loadnextcrisis = "";
var crisisresolve = "";

$( document ).ready(function() {

  load_presentCrisis();
  event_searchManageCrisisList();
  event_searchPresentCrisis();
  event_searchPastCrisis();

});

function event_searchManageCrisisList(){

  $('body').on('click', '#searchCrisisBtn', function(event) {

    var query_params = {};
    query_params['q'] = $("#searchCrisisInput").val();
    query_params['resolve'] = crisisresolve;
    var query_string = $.param(query_params);
    var api_url = "/api/v1.0/crisis/search/?" + query_string;

    $.ajax({
      type: "GET",
      dataType: 'json',
      url: api_url,
      success: function(data, status){

          $("#manageCrisisWrapper").empty();

          loadnextcrisis = data.next;
          data = data.results
          $.each(data, function(i, item) {

              var crisisDetail = {crisisTitle: item.title,
                                  crisisDescription: item.description,
                                  crisisDatetime: moment(item.created_datetime).format('DD MMM YYYY h:mm a'),
                                  crisisScale: item.scale,
                                  };

              $.each(item.affected_locations, function(i, locitem) {
                crisisDetail['crisisLat'] =  locitem.lat;
                crisisDetail['crisisLng'] =  locitem.lng;
                console.log(locitem.lat);
                console.log(locitem.lng);
              });

              $("#manageCrisisItemTemplate").tmpl(crisisDetail).appendTo("#manageCrisisWrapper");

          });

      },
      error: function(err) {
          console.log('error');
      }
    });

  });

}

function event_searchPresentCrisis(){

  $('body').on('click', '#searchPresentCrisis', function(event) {
    load_presentCrisis();
  });

}

function event_searchPastCrisis(){

  $('body').on('click', '#searchPastCrisis', function(event) {
    load_pastCrisis();
  });

}

function load_pastCrisis(){
  crisisresolve = "true";
  init_manageCrisisWrapperList();

  $( "#searchPresentCrisis" ).removeClass( "active" );
  $( "#searchPastCrisis" ).addClass( "active" );

}

function load_presentCrisis(){
  crisisresolve = "false";
  init_manageCrisisWrapperList();

  $( "#searchPastCrisis" ).removeClass( "active" );
  $( "#searchPresentCrisis" ).addClass( "active" );

}

function load_next_crisis(){

  if(loadnextcrisis == null){
    alert("No more crisis");
    return;
  }
  if(loadnextcrisis == ""){
    alert("No more crisis");
    return;
  }

  $.ajax({
    type: "GET",
    dataType: 'json',
    url: loadnextcrisis,
    success: function(data, status){

        loadnextcrisis = data.next;
        data = data.results
        $.each(data, function(i, item) {

            var crisisDetail = {crisisTitle: item.title,
                                crisisDescription: item.description,
                                crisisDatetime: moment(item.created_datetime).format('DD MMM YYYY h:mm a'),
                                crisisScale: item.scale,
                                };

            $.each(item.affected_locations, function(i, locitem) {
              crisisDetail['crisisLat'] =  locitem.lat;
              crisisDetail['crisisLng'] =  locitem.lng;
              console.log(locitem.lat);
              console.log(locitem.lng);
            });

            $("#manageCrisisItemTemplate").tmpl(crisisDetail).appendTo("#manageCrisisWrapper");

        });

    },
    error: function(err) {
        console.log('error');
    }
  });

}

function init_manageCrisisWrapperList(){

  var query_params = {};
  query_params['resolve'] = crisisresolve;
  var query_string = $.param(query_params);
  var api_url = "/api/v1.0/crisis/search/?" + query_string;

  $.ajax({
    type: "GET",
    dataType: 'json',
    url: api_url,
    success: function(data, status){

        $("#manageCrisisWrapper").empty();

        loadnextcrisis = data.next;
        data = data.results
        $.each(data, function(i, item) {

            var crisisDetail = {crisisTitle: item.title,
                                crisisDescription: item.description,
                                crisisDatetime: moment(item.created_datetime).format('DD MMM YYYY h:mm a'),
                                crisisScale: item.scale,
                                };

            $.each(item.affected_locations, function(i, locitem) {
              crisisDetail['crisisLat'] =  locitem.lat;
              crisisDetail['crisisLng'] =  locitem.lng;
            });

            $("#manageCrisisItemTemplate").tmpl(crisisDetail).appendTo("#manageCrisisWrapper");

        });

    },
    error: function(err) {
        console.log('error');
    }

  });

}
