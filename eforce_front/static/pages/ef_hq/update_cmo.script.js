$(document).ready(function() {

    $("#unresolvedCrisisSelect2").select2();

    event_getUnreadCrisisSelect2();

    event_getUnresolvedCrisisSelect2Details();

});


function event_getUnresolvedCrisisSelect2Details(){
    $("#unresolvedCrisisSelect2").on("change", function (e) {

      var crisisSelected = $("#unresolvedCrisisSelect2").select2('data')[0];
      $("#inputForCrisis").val(crisisSelected.id);
      $.ajax({
        type: "GET",
        dataType: 'json',
        url: "api/v1.0/crisis/case/" + crisisSelected.id + "/",
        success: function(data, status){
            data = data.data


            var crisisDetail = {crisisTitle: data.title,
                                crisisDescription: data.description,
                                crisisDatetime: moment(data.created_datetime).format('DD MMM YYYY h:mm a'),
                                crisisScale: data.scale
                                };

            $("#crisis_detail_viewer").empty();
            $("#crisisDetailTemplate").tmpl(crisisDetail).appendTo("#crisis_detail_viewer");

        },
        error: function(err) {
            console.log('error');
        }

      });

      $.ajax({
        type: "GET",
        dataType: 'json',
        url: "api/v1.0/crisis/case/" + crisisSelected.id + "/ef/update/",
        success: function(data, status){
            data = data.data

            var crisisEFUpdates = [];
            $.each(data, function(i, item) {
                crisisEFUpdates.push({
                  crisisByUserGroup: item.get_readable_sent_by,
                  crisisUpdateDatetime: moment(item.created_datetime).format('DD MMM YYYY h:mm a'),
                  crisisUpdateDescription: item.description,
                  crisisUpdateForceCasualty: item.force_casualty,
                  crisisUpdateForceLat: item.force_lat,
                  crisisUpdateForceLng: item.force_lng,
                  crisisUpdateForceSize: item.force_size,
                  crisisUpdateKnownCasualty: item.known_casualty,
                  crisisUpdateKnownDead: item.known_dead,
                  crisisImageUrl: item.by_group.image_url
                });
            });

            $("#crisis_update_viewer").empty();
            $("#crisisUpdateTemplate").tmpl(crisisEFUpdates).appendTo("#crisis_update_viewer");

        },
        error: function(err) {
            console.log('error');
        }

      });

    });
}

function event_getUnreadCrisisSelect2(){
    $("#unresolvedCrisisSelect2").select2({
        ajax: {
            url: "/api/v1.0/crisis/unread/search/",
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term, // search term
                    page: params.page,
                };
            },
            processResults: function (data, params) {
                params.page = params.page || 1;
                return {
                    results: $.map(data.results, function (item) {
                        return {
                            text: item.title,
                            id: item.id
                        }
                    }),
                    pagination: {
                        more: (params.page * 20) < data.count
                    }
                };
            },
            cache: true
        },
        escapeMarkup: function (markup) { return markup; }, // let our custom formatter work
        minimumInputLength: 0
    });
}
