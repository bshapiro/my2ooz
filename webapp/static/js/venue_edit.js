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
