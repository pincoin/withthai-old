$('#round_date').flatpickr({
    minDate: new Date().fp_incr(1),
    maxDate: new Date().fp_incr(30),
    defaultDate: new Date().fp_incr(1)
});

$('#round_time').flatpickr({
    enableTime: true,
    noCalendar: true,
    time_24hr: true,
    dateFormat: "H:i",
    minTime: "06:00",
    maxTime: "20:00",
    minuteIncrement: 10,
    defaultDate: "06:00"
});
