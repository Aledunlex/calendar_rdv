function load_in(){
    $('#spinner').show();
}

function load_out(){
    $('#spinner').hide();
}

function addCalendarEvent(day, month, year){
  load_in();
    $.ajax({
          url:"addCalendarEvent",
          method:"POST",
          data:{day:day, month:month, year:year},
          success:function(data) {
            load_out();
            $('#modal_body').html(data);
            $('#modal_launcher').click();
        },
        error:function(data) {
            load_out();
            
        }
     });
}

function addUserGroup(idGroup){
  load_in();
    $.ajax({
          url:"addUserGroup",
          method:"POST",
          data:{id_group:idGroup},
          success:function(data) {
            load_out();
            $('#modal_body').html(data);
            $('#modal_launcher').click();
        },
        error:function(data) {
            load_out();

        }
     });
}

function addNewEvent(){
  load_in();
    let day = $('#day').val();
    let month = $('#month').val();
    let year = $('#year').val();
    let meeting_date = $('#date_meeting').val();
    let id_group = $('#id_group').val();
    let name = $('input[name="name"]').val();
    let description = $('input[name="description"]').val();
    let place = $('input[name="place"]').val();
    $.ajax({
          url:"create_evenement",
          method:"POST",
          data:{
            day:day,
            month:month,
            year:year,
            date_meeting:meeting_date, 
            id_group:id_group, 
            name:name, 
            description:description, 
            place:place},
          success:function(data) {
            load_out();
            $('#modal_body').html(data);
        },
        error:function(data) {
            load_out();
            
        }
     });
}

function displayEvent(id){
  load_in();
    $.ajax({
          url:"/display_event",
          method:"POST",
          data:{id_event:id},
          success:function(data) {
            load_out();
            $('#modal_body').html(data);
            $('#modal_launcher').click();
        },
        error:function(data) {
            load_out();
            
        }
     });
}

function deleteEvent(id){
  load_in();
    $.ajax({
          url:"/delete_event",
          method:"POST",
          data:{id_event:id},
          success:function(data) {
            load_out();
            $('#modal_body').html(data);
        },
        error:function(data) {
            load_out();
        }
    });
}

function copyInviteLink() {
  // Get the text field
  var copyText = $("#inviteLink");
  var content = copyText.text();
  // Copy the text inside the text field
  navigator.clipboard.writeText(content);
  $('#inviteLink').text('Copié !');
  $('#inviteLink').css('color', 'green');
  // Sleep 1 second
  setTimeout(function(){
    $('#inviteLink').text(content);
    $('#inviteLink').css('color', 'black');
  }, 1000);

}