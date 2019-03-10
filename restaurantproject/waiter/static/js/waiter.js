// TODO: At the moment, the user needs to touch the screen at least once for the vibrations to work? Fix this?
// NOTE: These hacks seem very unreliable? The behaviour of the vibrations is unpredictable? Code reordering might cause them to stop working?

// Save datetime of latest call fetched.
var prevLatestCallDateTime = '0';
var lastCallTime = '0';
const getCalls = () => {
    fetch(`/waiter/calls`).then(response => response.json()).then(responseJson => {
        const callsTable = document.getElementById('table-calls');
        const calls = responseJson.calls
        // Delete existing non-header rows.
        while (callsTable.rows.length > 1) {
            callsTable.deleteRow(1);
        }
        
        // Compare datetime of latest call fetched with the previously saved then-latest call datetime.
        if (calls.length > 0) {
            lastCallTime = calls[0].datetime
        }

        for (let call of responseJson.calls) {
            // Append new row. Arg -1 causes row to be inserted at the last position (appended).
            const callRow = callsTable.insertRow(-1);

            // Append cells. Arg -1 causes each cell to be inserted at the last position in the row (appended).
            const sectionNoCell = callRow.insertCell(-1);
            const tableNoCell = callRow.insertCell(-1);
            const datetimeCell = callRow.insertCell(-1);
            sectionNoCell.innerHTML = call.sectionNo;
            tableNoCell.innerHTML = call.tableNo;

            /* Expected datetime format is 2019-02-26 15:08:04.440589+00:00, 
             * but we just want the time (HH:mm:ss) component, 
             * which begins at the 11th position, and is 8 chars long. */
            datetimeCell.innerHTML = call.datetime.substring(11, 11 + 8);
        }

        return responseJson;
    }).then(responseJson => {
        // If at least 1 new call was made, cause a vibration.
        // HACK: setTimeout causes encapsulated function to execute after stack is cleared. Apparently this makes vibrate() work more often?
        setTimeout(function() {
            if (lastCallTime > prevLatestCallDateTime) {
                prevLatestCallDateTime = lastCallTime;
                document.getElementById('nodisplay-button-vibration').click();
            }
        });
    });
};

// HACK: These calls might overlap? 
setInterval(getCalls, 5000);
getCalls();

function vibrate() {
    // TODO: Check if vibrate(...) is supported
    window.navigator.vibrate(333);
};