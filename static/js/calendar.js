
'use strict';
   
document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        initialDate: '2021-06-07',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
    });

    calendar.render();
    
    // TODO Breakout into utility function if needed
    $.ajax({
        type: "POST",
        url: "/calendar.json",
        success: function(res) {

        calendar.addEvent({id: '1', title: 'HI', start: '2021-06-19'});

        for (i = 0; i < res.length; i++) {
            calendar.addEvent(res[i]);
            console.log(res[i]);
        }
        // console.log("YOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO");
        calendar.render();
        } 
    });
});
