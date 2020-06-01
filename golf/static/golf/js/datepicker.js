$('#id_round_date').flatpickr();

$('#id_round_time').flatpickr({
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
    time_24hr: true,
    minTime: "06:00",
    maxTime: "19:30",
    defaultDate: "06:00",
    minuteIncrement: 10
});