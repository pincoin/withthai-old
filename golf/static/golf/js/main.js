function intcomma(number) {
    return number.toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
}

$(document).ready(function () {
    $('#id_round_date, #id_round_time, #id_pax').on('change', function () {
        const round_date = $('#id_round_date').val().split('-');
        const round_time = $('#id_round_time').val().split(':');
        const pax = $('#id_pax').val();

        if (round_date && round_time && pax) {
            const rdate = new Date(parseInt(round_date[0], 10),
                parseInt(round_date[1], 10) - 1,
                parseInt(round_date[2], 10));

            const rtime = new Date(2020, 0, 1,
                parseInt(round_time[0], 10),
                parseInt(round_time[1], 10));

            // check whether holiday/weekends or not
            let weekday = 0;

            if (rdate.getDay() === 6 || rdate.getDay() === 0) {
                weekday = 1;
            }

            let out = false;

            for (i = 0; i < holidays.length; i++) {
                const holiday = holidays[i].split('-');

                if (rdate.getTime() === new Date(parseInt(holiday[0], 10),
                    parseInt(holiday[1], 10) - 1,
                    parseInt(holiday[2], 10)).getTime()) {
                    out = true;
                    weekday = 1;
                    break;
                }

                if (out)
                    break;
            }

            let out1 = false;

            for (i = 0; i < rates.length; i++) {
                if (rates[i]['weekday'] === weekday) {
                    // check whether round date is within season
                    const season_start = rates[i]['season_start'].split('-');
                    const season_end = rates[i]['season_end'].split('-');

                    if (rdate.getTime() >= new Date(parseInt(season_start[0], 10),
                        parseInt(season_start[1], 10) - 1,
                        parseInt(season_start[2], 10)).getTime()
                        && rdate.getTime() <= new Date(parseInt(season_end[0], 10),
                            parseInt(season_end[1], 10) - 1,
                            parseInt(season_end[2], 10)).getTime()) {
                        // check whether round time is within round time
                        const slot_start = rates[i]['slot_start'].split(':');
                        const slot_end = rates[i]['slot_end'].split(':');

                        if (rtime.getTime() >= new Date(2020, 0, 1,
                            parseInt(slot_start[0], 10), parseInt(slot_start[1], 10))
                            && rtime.getTime() <= new Date(2020, 0, 1,
                                parseInt(slot_end[0], 10), parseInt(slot_end[1], 10))) {
                            $('#green-fee-block').removeClass('is-hidden');
                            $('#id_green_fee').val(intcomma(rates[i]['green_fee']));

                            $('#total-block').removeClass('is-hidden');
                            $('#id_total').val(intcomma(rates[i]['green_fee'] * pax));

                            out1 = true;
                            break;
                        }
                    }
                }
                if (out1) {
                    break;
                }
            }

            if (!out1) {
                $('#green-fee-block').addClass('is-hidden');
                $('#total-block').addClass('is-hidden');
            }

            console.log(out);
        }
    });
});
