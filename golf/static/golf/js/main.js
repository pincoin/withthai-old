$('#id_round_date, #id_round_time').on('change', function () {
    const round_date = $('#id_round_date').val();
    const round_time = $('#id_round_time').val();

    if (round_date && round_time) {
        console.log('date/time changed');
    }
});

$('#id_pax').on('change', function () {
    const pax = $('#id_pax').val();

    if (pax) {
        console.log('pax changed');
    }
});