$(document).ready(function () {


    $.ajax({
      type: "POST",
      url: "/my2ooz/venue_info",
    }).done(function( data) {
      elements = $('[name]');
      console.log(elements);
      for (var i = 0; i < elements.length; i++) {
        $(elements[i]).attr('value', data[$(elements[i]).attr('name')]);
      }
    });


    $("#logout_items").mouseover(function() {
        $("#login_box").fadeIn();
    });

     $("#logout_items").mouseleave(function() {
        $("#login_box").fadeOut();
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




    $("#form_object").submit(function(){
           $.post(
               "/my2ooz/venue_update",
               $("#form_object").serialize(),
                function(data){
                   console.log(data);
               }
           );
           $('.success').show();
           return false;
    });
});
