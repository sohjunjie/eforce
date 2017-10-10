$( document ).ready(function() {

  init_manageCrisisWrapperList();

});

function init_manageCrisisWrapperList(){

  // var query_params = {};
  // query_params['q'] = page;
  // var query_string = $.param(query_params);
  // "/api/v1.0/crisis/search/" + query_string

        $.ajax({
          type: "GET",
          dataType: 'json',
          url: "/api/v1.0/crisis/search/",
          success: function(data, status){

              $("#manageCrisisWrapper").empty();

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
