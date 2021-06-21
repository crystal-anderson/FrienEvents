'use strict';

const eventModal = new bootstrap.Modal(document.querySelector('#eventModal'));

const domCal = document.getElementById('calendar');
const calendar = new FullCalendar.Calendar(domCal, {
    themeSystem: 'bootstrap',
    initialView: 'dayGridMonth',
    headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    eventClick: (info) => {
        info.jsEvent.preventDefault();

        console.log(info.event);

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
            console.log(res);

            // If event successfully deleted, remove from FullCalendar
            const eventObj = calendar.getEventById(eventId);
            eventObj.remove();
        });
    });
}



$.get(`/api/user/${domCal.dataset.userId}/events`, (res) => {

    console.log('Events from GET request:');
    console.log(res);

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
