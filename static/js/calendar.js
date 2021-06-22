'use strict';

const eventModal = new bootstrap.Modal(document.querySelector('#eventModal'));

let current_user = document.getElementById('current_user')

const domCal = document.getElementById('calendar');
const calendar = new FullCalendar.Calendar(domCal, {
    themeSystem: 'bootstrap',
    initialView: 'dayGridMonth',
    headerToolbar: {
        left: 'dayGridMonth,timeGridWeek,timeGridDay today',
        center: 'title',
        right: current_user ? 'custom1 prevYear,prev,next,nextYear' : 'prevYear,prev,next,nextYear'
      },
      footerToolbar: {
        right: 'prev,next'
      },
      customButtons: {
        custom1: {
          text: 'add event',
          click: function() {
              alert('clicked custom button!')
          }
        }
      },
    eventClick: (info) => {
        info.jsEvent.preventDefault();

        document.querySelector('#eventModalTitle').innerText = info.event.title;
        document.querySelector('#eventModalStart').innerText = info.event.start;
        document.querySelector('#eventModalUrl').setAttribute('href', info.event.url);

        buildDeleteHandler(info.event.id);

        eventModal.show();
    }
});


function buildDeleteHandler(eventId) {
    document.querySelector('#eventModalDelete').addEventListener('click', () => {
        $.post(`/api/remove-event/${eventId}`, (res) => {
            
            // If event successfully deleted, remove from FullCalendar
            const eventObj = calendar.getEventById(eventId);
            eventObj.remove();
        });
    });
}


$.get(`/api/user/${domCal.dataset.userId}/events`, (res) => {

    for (const event of res) {
        // Convert event to FullCalendar-compatible event obj
        // Add event obj to calendar
        calendar.addEvent({
            id: event.event_id,
            title: event.title,
            start: event.start,
            url: event.url
        });
    }

    calendar.render();
});
