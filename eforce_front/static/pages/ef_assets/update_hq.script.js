$(document).ready(function() {

    event_getSearchUnresolvedCrisisSelect2();

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

      // GET EF HQ INSTRUCTIONS
      $.ajax({
        type: "GET",
        dataType: 'json',
        url: "api/v1.0/crisis/case/" + crisisSelected.id + "/ef/group/instruction/",
        success: function(data, status){
            data = data.data

            var EFHQInstructions = [];
            $.each(data, function(i, item) {
                EFHQInstructions.push({
                  instructionDetails: item.text,
                  instructionSentDateTime: moment(item.created_datetime).format('DD MMM YYYY h:mm a'),
                  instructionForceLat: item.force_lat,
                  instructionForceLng: item.force_lng,
                });
            });

            $("#crisis_instruction_viewer").empty();
            $("#crisisInstructionTemplate").tmpl(EFHQInstructions).appendTo("#crisis_instruction_viewer");

        },
        error: function(err) {
            console.log('error');
        }

      });

    });
}

function event_getSearchUnresolvedCrisisSelect2(){
    $("#unresolvedCrisisSelect2").select2({
        placeholder: "Select a crisis for sending HQ updates",
        ajax: {
            url: "/api/v1.0/crisis/search/",
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term, // search term
                    page: params.page,
                    thisusergroup: "true"
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
