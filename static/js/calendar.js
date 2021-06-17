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
        url: "/calendar.json/" + calendarEl.dataset.userId,
        success: function(res) {

            for (var i = 0; i < res.length; i++) {
                calendar.addEvent(res[i]);
            }
        } 
    });
});
