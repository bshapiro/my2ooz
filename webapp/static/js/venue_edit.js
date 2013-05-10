$(document).ready(function () {

    elements = $('.required');
    for (var i = 0; i < elements.length; i++) {
      $(elements[i]).append("<div class='required_text'>    *required</div>");
    }


    $.ajax({
      type: "POST",
      url: "/my2ooz/check_auth",
    }).done(function( data) {
      console.log(data);
      if (data != "False") {
	$('#logout_items').attr('style', '');
	}
    });


    $.ajax({
      type: "POST",
      url: "/my2ooz/venue_info",
    }).done(function( data) {
      elements = $('[name]');
      for (var i = 0; i < elements.length; i++) {
        $(elements[i]).attr('value', data[$(elements[i]).attr('name')]);
      }
    });



    $("#logout_items").mouseover(function() {
        $("#logout_box").fadeIn();
    });

     $("#logout_items").mouseleave(function() {
        $("#logout_box").fadeOut();
    });

    $('#login_header').click(function() {
        if ($('#login_information').is(':visible')) {
            $('#login_information').hide('slide');
        } else {
            $('#login_information').show('slide');
        }
    });


    $('#venue_header').click(function() {
        if ($('#venue_information').is(':visible')) {
            $('#venue_information').hide('slide');
        } else {
            $('#venue_information').show('slide');
        }
    });

    $('#calendar_header').click(function() {
        if ($('#calendar_information').is(':visible')) {
            $('#calendar_information').hide('slide');
        } else {
            $('#calendar_information').show('slide');
        }
    });

    var buttonpressed;
    $('.save').click( function() {
        buttonpressed = $(this).attr('id');
    });

    $("#form_object").submit(function(e){
        $.post(
           "/my2ooz/venue_update",
           $("#form_object").serialize(),
            function(data){
               console.log(data);
           }
       );

        if (buttonpressed == "save1") {
          $('#success1').show('slow');
          setTimeout(function(){
            $('#success1').hide('slow');
          }, 5000);
        } else {
          $('#success2').show('slow');
           setTimeout(function(){
                $('#success2').hide('slow');
           }, 5000);
        }

        return false;
    });


    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();

    $('#calendar').fullCalendar({
      header: {
        left: 'prev,next today',
        center: 'title',
        right: 'month,basicWeek,basicDay'
      },
      editable: true,
      events: [{
        }
      ]
    });

    resetEditButtons();

    $('.fc-button').click(function () {
      resetEditButtons();
    });

    $('#calendar_information').hide();

    var cur_date_object;
    var cur_parent;



    $('#save_event').click(function() {
      var eventSource = new Object();
      eventSource.title = $('#event_title').val(); // this should be string
      eventSource.start = cur_date_object; // this should be date object
      eventSource.end = cur_date_object;

      var events = new Array();
      events[0] = eventSource;
      $(cur_parent).find('input').remove();
      $('#calendar').fullCalendar('addEventSource', events);
      $('#calendar').fullCalendar('rerenderEvents');
      $('#new_event').hide();
      $('.overlay').fadeOut('fast');
      $('#event_form')[0].reset();
    });

    $('#cancel_event').click(function() {
      $('#new_event').hide();
      $('.overlay').fadeOut('fast');
      $('#event_form')[0].reset();
    });


  });

function parseDate(input) {
  var parts = input.match(/(\d+)/g);
  // new Date(year, month [, date [, hours[, minutes[, seconds[, ms]]]]])
  return new Date(parts[0], parts[1]-1, parts[2]); // months are 0-based
}

    function resetEditButtons() {
      $('.edit_button').remove();
      elements = $('.fc-day-content');
      for (var i = 0; i < elements.length; i++) {
        $(elements[i]).append("<input class='edit_button rounded-corners clickable' value='Edit'/>");
      }

      $('.edit_button').click(function() {
      cur_parent = $(this).parent();
      console.log(cur_parent);
      var cur_date = $(this).parent().parent().parent().attr('data-date');
      cur_date_object = parseDate(cur_date);
      var cur_date_string = cur_date_object.toDateString();
      $('#date').text(cur_date_string);
      $('.overlay').fadeIn('slow');
      $('#new_event').show();

    });
    }
