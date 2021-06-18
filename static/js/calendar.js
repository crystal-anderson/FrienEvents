'use strict';
   

const domCal = document.getElementById('calendar');

const calendar = new FullCalendar.Calendar(domCal, {
    initialView: 'dayGridMonth',
    initialDate: '2021-06-07',
    headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay'
    }
});

function getData() {

    $.ajax({
        type: "POST",
        url: "/calendar.json/" + domCal.dataset.userId,
        success: function(res) {

            for (var i = 0; i < res.length; i++) {
                calendar.addEvent(res[i]);
                
                // TODO add event listener for each element
            }
        } 
    });
}

// TODO add a class level event listener for fc-event-title. target 

// function removeEvent(event_id) {

//      calendar.getEvents()
//      calender.removeEvent()
//     $.post(
//         url:"/remove-event" + event_id
//     );
// }
// HANDLE ACTION?? HANDLE DATA?? RENDER REQUEST? CURRENT DATA!???

document.addEventListener('DOMContentLoaded', function() {
    calendar.render();
    getData();
},  calendar);

// TODO update function

// TODO add listeners or tap into the calendars listener

// TODO add event listener to objects
