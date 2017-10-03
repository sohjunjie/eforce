$(document).ready(function() {

    event_getSearchUserGroupSelect2();

    event_getSearchUnresolvedCrisisSelect2();

    event_getUnresolvedCrisisSelect2Details();

});

function event_getSearchUserGroupSelect2(){
    $("#userGroupSelect2").select2({
        placeholder: "Select EF Assets group to dispatch",
        ajax: {
            url: "api/v1.0/user/group/search/",
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
                            text: item.get_readable_rolename,
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


function event_getSearchUnresolvedCrisisSelect2(){
    $("#unresolvedCrisisSelect2").select2({
        placeholder: "Select a crisis to view its combat strategies",
        ajax: {
            url: "/api/v1.0/crisis/unresolved/search/",
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


function event_getUnresolvedCrisisSelect2Details(){
    $("#unresolvedCrisisSelect2").on("change", function (e) {

      // TODO: PUSH TO CRISISMARKERS

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

            // $.each(data.affected_location, function(i, item) {
            //   item.lat;
            // });

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
        url: "api/v1.0/crisis/case/" + crisisSelected.id + "/strategy/",
        success: function(data, status){
            data = data.data

            var crisisEFUpdates = [];
            $.each(data, function(i, item) {
                crisisEFUpdates.push({
                  strategyDetail: item.detail,
                  strategyDatetime: moment(item.created_datetime).format('DD MMM YYYY h:mm a')
                });
            });

            $("#crisis_strategy_viewer").empty();
            $("#crisisStrategyTemplate").tmpl(crisisEFUpdates).appendTo("#crisis_strategy_viewer");

        },
        error: function(err) {
            console.log('error');
        }

      });

    });
}
