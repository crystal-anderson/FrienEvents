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

        // Update the eventModal
        document.querySelector('#eventModalTitle').innerText = info.event.title;
        // eventModalStart
        document.querySelector('#eventModalStart').innerText = info.event.start;
        // eventModalUrl
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


// function removeEvent(event_id) {
//     $.post(
//         url: "/remove-event/" + event_id
//         );
// }



$.get(`/api/user/${domCal.dataset.userId}/events`, (res) => {
    // `res` is array of event objects that look like this:
    // {"event_id": event.event_id,
    // "title" : event.site_title,
    // "start" : event.event_date.isoformat(),
    // "url" : event.event_url,}

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







// Step 2
// Implement in JS?
  // Example code from bootstrap docs
// exampleModal.addEventListener('show.bs.modal', function (event) {
// mor example from BS docs:
  // (event) => {
  // Button that triggered the modal
//   var button = event.relatedTarget
//   // Extract info from data-bs-* attributes
//   var recipient = button.getAttribute('data-bs-whatever')
//   // If necessary, you could initiate an AJAX request here
//   // and then do the updating in a callback.
//   //
//   // Update the modal's content.
//   var modalTitle = exampleModal.querySelector('.modal-title')
//   var modalBodyInput = exampleModal.querySelector('.modal-body input')

//   modalTitle.textContent = 'New message to ' + recipient
//   modalBodyInput.value = recipient
// })

// Add eventClick handler when creating calendar
// in handler function, call myModal.show() to show modal window


