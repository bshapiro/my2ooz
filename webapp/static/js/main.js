$(document).ready( function () {


    $("#login_items").mouseover(function() {
        $("#login_box").fadeIn();
    });

     $("#login_items").mouseleave(function() {
        $("#login_box").fadeOut();
    });

     $("#register_items").mouseover(function() {
        $("#register_box").fadeIn();
    });

     $("#register_items").mouseleave(function() {
        $("#register_box").fadeOut();
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


});
