document.getElementById('predictionForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Error message
    function showError(message) {
        alert(message);
    }

    // Brazilian States Abbreviation
    const validStates = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", 
        "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"];

    // Valid Races according to IBGE
    const validRaces = [1, 2, 3, 4, 5, 9];

    // Input Validation
    function validateInputs() {
        var state = document.getElementById('state').value.toUpperCase();
        if (!validStates.includes(state)) {
            showError("State must be a valid Brazilian state abbreviation.");
            return false;
        }

        // Checking if inputs are all integers
        var inputsToCheck = [ 'age', 'sex', 'race', 'literate', 'educational_level', 'studied_years', 'worker_type', 'work_segment', 
            'occupation_group', 'tax_payer', 'hours_range', 'hours_value'];
        for (var i = 0; i < inputsToCheck.length; i++) {
            var value = parseInt(document.getElementById(inputsToCheck[i]).value);
            if (!Number.isInteger(value)) {
                showError(inputsToCheck[i].charAt(0).toUpperCase() + inputsToCheck[i].slice(1) + " must be an integer.");
                return false;
            }
        }

        // Checking if there is aninvalid race
        var race = parseInt(document.getElementById('race').value)
        if (!validRaces.includes(race)){
            showError("Race must be a valid integer representing a race.")
            return false;
        }

        return true;
    }

    if (validateInputs()) {
        // If all input is valid, save it
        var formData = new FormData(this);

        // Send a request to Flask API
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Render response on the html page
            document.getElementById('result').innerHTML = `
                <p>Predicted Income in 2023: R$ ${data.prediction_2023.toFixed(2)}</p>
                <p>Predicted Income Adjusted to current date: R$ ${data.prediction_adjusted.toFixed(2)}</p>
                <p>Predicted Income in 2023 (USD): $ ${data.prediction_2023_usd.toFixed(2)}</p>
                <p>Predicted Income Adjusted to current date(USD): $ ${data.prediction_adjusted_usd.toFixed(2)}</p>
            `;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('result').innerHTML = 'An error occurred. Please try again.';
        });
    }
});
