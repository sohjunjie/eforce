var loadnextcrisis = "";
var crisisresolve = "";

$( document ).ready(function() {

  load_presentCrisis();
  event_searchManageCrisisList();
  event_searchPresentCrisis();
  event_searchPastCrisis();
  event_crisis_details_modal();

});

function event_crisis_details_modal() {

  $('body').on('click', '.crisis-modal-launcher', function(){
    let crisisId = $(this).attr('id').replace('crisis-id-', '');
    let p = $(this).parent();
    let crisisTitle = p.contents().not(p.children()).text();
    $('#crisis-detail-modal-title').text(crisisTitle);
    get_efupdate_crisis_details(crisisId);

  });

}

function get_efupdate_crisis_details(crisisId){

  var api_url = "/api/v1.0/crisis/case/" + crisisId + "/ef/update/";

  $.ajax({
    type: "GET",
    dataType: 'json',
    url: api_url,
    success: function(data, status){
      $('#crisis-detail-timeline').empty();

      data = data.data;
      let eforce_locs = {};
      let thisCrisisUpdateDate = null;

      $.each(data, function(i, item) {
        let crisisEfUpdateDetail = {
            crisisTimehhmm: moment(item.created_datetime).format('hh:mm'),
            crisisEFAssetName: item.get_readable_sent_by,
            crisisUpdateDescription: item.description,
            crisisLat: item.force_lat,
            crisisLng: item.force_lng,
            crisisEFAssetImageUrl: item.by_group.image_url,
            crisisForceSizeSent: item.force_size,
            crisisForceCasualty: item.force_casualty
        };

        if(!(item.get_readable_sent_by in eforce_locs)){
          eforce_locs[item.get_readable_sent_by] = [];
        }
        eforce_locs[item.get_readable_sent_by].push({
          forceLatLng: {lat: item.force_lat, lng: item.force_lng},
          crisisEFAssetImageUrl: item.by_group.image_url
        })

        if(thisCrisisUpdateDate != moment("2017-09-26T14:37:34.512425Z").format('DD MMM. YYYY')){
          thisCrisisUpdateDate = moment("2017-09-26T14:37:34.512425Z").format('DD MMM. YYYY');
          $("#manageCrisisTimelineDateItemTemplate").tmpl({crisisUpdateDate: thisCrisisUpdateDate}).appendTo("#crisis-detail-timeline");
        }

        $("#manageCrisisTimelineItemTemplate").tmpl(crisisEfUpdateDetail).appendTo("#crisis-detail-timeline");
      });

    },
    error: function(err) {
      return null;
    }
  });

}

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

              var crisisDetail = {
                                  crisisId: item.id,
                                  crisisTitle: item.title,
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

            var crisisDetail = {
                                crisisId: item.id,
                                crisisTitle: item.title,
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

            var crisisDetail = {
                                crisisId: item.id,
                                crisisTitle: item.title,
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
