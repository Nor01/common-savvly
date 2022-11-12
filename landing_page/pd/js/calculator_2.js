const inflation_rate = 2 / 100;
const newaverage_return = 6 / 100;
const default_value = 5.5 / 100;
const Annual_withdrawal_percentage_without = 4 / 100;

let Annual_withdrawal_target = 0;
let Initial_retirement_balance = 0;
let SAVVLY_initial_retirement_balance = 0;

let Monthly_withdrawal_with_SAVVLY = 0;
let Monthly_withdrawal_without_SAVVLY = 0;


let current_gender_selected = document.getElementById('current_gender_selected');
Value_current_gender_selected = document.getElementById('current_gender_selected').value;
// sessionStorage.setItem("Value_current_gender_selected$", Value_current_gender_selected);

let current_retired_status = document.getElementById('current_retired_status');
Value_current_retired_status = document.getElementById('current_retired_status').value;
// sessionStorage.setItem("Value_current_retired_status$", Value_current_retired_status);

let current_age_selected = document.getElementById('current_age_selected');
Value_current_age_selected = document.getElementById('current_age_selected').value;
// sessionStorage.setItem("Value_current_age_selected$", Value_current_age_selected);

let current_age_selected2 = document.getElementById('current_age_selected2');
Value_current_age_selected2 = document.getElementById('current_age_selected2').value;

let current_withdrawal_selected = document.getElementById('current_withdrawal_selected');
Value_current_withdrawal_selected = document.getElementById('current_withdrawal_selected').value;
// sessionStorage.setItem("Value_current_withdrawal_selected$", Value_current_withdrawal_selected);

let current_spending_selected = document.getElementById('current_spending_selected');
Value_current_spending_selected = document.getElementById('current_spending_selected').value;
// sessionStorage.setItem("Value_current_spending_selected$", Value_current_spending_selected);

// if the user is NOT RETIRED
let current_age_retire_selected = document.getElementById('current_age_retire_selected');
Value_current_age_retire_selected = document.getElementById('current_age_retire_selected').value;
// sessionStorage.setItem("Value_current_age_retire_selected$", Value_current_age_retire_selected);

let current_needed_selected = document.getElementById('current_needed_selected');
Value_current_needed_selected = document.getElementById('current_needed_selected').value;
// sessionStorage.setItem("Value_current_needed_selected$", Value_current_needed_selected);

let current_saved_selected = document.getElementById('current_saved_selected');
Value_current_saved_selected = document.getElementById('current_saved_selected').value;
// sessionStorage.setItem("Value_current_saved_selected$", Value_current_saved_selected);


let Montly_installment_XX = 0;
let Montly_installment_YY = 0;
let money_saved_already = 0;
let Montly_installment_YY_Percent = 0;

document.addEventListener('DOMContentLoaded', () => {
    // Montly_installment_XX = (without_savvly_value - Money_saved_already) * default_average_return / [ ( (1+default_average_return) ^ 12(retirement_age - current_age)) - 1 ]
    // Montly_installment_YY = (with_savvly_value - Money_saved_already) * default_average_return/ [ ( (1+default_average_return) ^ 12(retirement_age - current_age)) - 1 ]

    document.getElementById('montly_installment_XX').innerHTML = parseInt(0).toLocaleString('en-US');
    document.getElementById('montly_installment_YY').innerHTML = parseInt(0).toLocaleString('en-US');

    //Labels With and Without Savvly
    document.getElementById('withsavvly').innerHTML = parseInt(0).toLocaleString('en-US');
    document.getElementById('withoutsavvly').innerHTML = parseInt(0).toLocaleString('en-US');

    document.getElementById('withsavvly2').innerHTML = parseInt(0).toLocaleString('en-US');
    document.getElementById('withoutsavvly2').innerHTML = parseInt(0).toLocaleString('en-US');

    Value_current_gender_selected = 'Choose...';
    Value_current_retired_status = sessionStorage.getItem("Value_current_retired_status$");

    $('#ageIfRetiredY').hide();

    // sessionStorage.getItem("Value_current_retired_status$");

    if (sessionStorage.getItem("Value_current_age_selected$") != null && sessionStorage.getItem("Value_current_retired_status$") == "No") {
        $('#current_age_selected').val(sessionStorage.getItem('Value_current_age_selected$'));
        Value_current_age_selected = sessionStorage.getItem('Value_current_age_selected$');
        document.getElementById('ageLabel').innerHTML = sessionStorage.getItem("Value_current_age_selected$");
        // document.getElementById('warningAge').innerHTML = sessionStorage.getItem("Value_current_age_selected$");
        let valueAgeSelected = (current_age_selected.value - current_age_selected.min) / (current_age_selected.max - current_age_selected.min) * 100;
        current_age_selected.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79  ' + valueAgeSelected + '%, #fff ' + valueAgeSelected + '%, white 100%)';
    } else {
        document.getElementById('ageLabel').innerHTML = Value_current_age_selected;
        // document.getElementById('warningAge').innerHTML = Value_current_age_selected;
    }

    //If Retired = Y the Age will have this values

    if (sessionStorage.getItem("Value_current_age_selected2$") != null && sessionStorage.getItem("Value_current_retired_status$") == "Yes") {
        $('#current_age_selected2').val(sessionStorage.getItem('Value_current_age_selected2$'));
        Value_current_age_selected2 = sessionStorage.getItem('Value_current_age_selected2$');
        document.getElementById('ageLabelIfRetireY').innerHTML = sessionStorage.getItem("Value_current_age_selected2$");
        // document.getElementById('warningAge').innerHTML = sessionStorage.getItem("Value_current_age_selected2$");
        let valueAgeSelected2 = (current_age_selected2.value - current_age_selected2.min) / (current_age_selected2.max - current_age_selected2.min) * 100;
        current_age_selected2.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79  ' + valueAgeSelected2 + '%, #fff ' + valueAgeSelected2 + '%, white 100%)';
    } else {
        document.getElementById('ageLabelIfRetireY').innerHTML = Value_current_age_selected2;
        // document.getElementById('warningAge').innerHTML = Value_current_age_selected2;
    }

    if (sessionStorage.getItem("Value_current_withdrawal_selected$") != null) {
        $('#current_withdrawal_selected').val(sessionStorage.getItem("Value_current_withdrawal_selected$"));
        Value_current_withdrawal_selected = sessionStorage.getItem("Value_current_withdrawal_selected$");

        console.log('sessionStorage:' + Value_current_withdrawal_selected);
        document.getElementById('withdrawalLabel').innerHTML = parseInt(sessionStorage.getItem("Value_current_withdrawal_selected$")).toLocaleString('en-US');
        let valueWithdrawal = (current_withdrawal_selected.value - current_withdrawal_selected.min) / (current_withdrawal_selected.max - current_withdrawal_selected.min) * 100;
        current_withdrawal_selected.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79  ' + valueWithdrawal + '%, #fff ' + valueWithdrawal + '%, white 100%)';
    } else {
        document.getElementById('withdrawalLabel').innerHTML = parseInt(Value_current_withdrawal_selected).toLocaleString('en-US');
        Value_current_withdrawal_selected = document.getElementById('current_withdrawal_selected').value;
        console.log('default input:' + Value_current_withdrawal_selected);

    }

    if (sessionStorage.getItem('Value_current_spending_selected$') != null) {
        $('#current_spending_selected').val(sessionStorage.getItem('Value_current_spending_selected$'));
        Value_current_spending_selected = sessionStorage.getItem('Value_current_spending_selected$');
        document.getElementById('spendingLabel').innerHTML = parseInt(sessionStorage.getItem("Value_current_spending_selected$")).toLocaleString('en-US');
        let valueSpending = (current_spending_selected.value - current_spending_selected.min) / (current_spending_selected.max - current_spending_selected.min) * 100;
        current_spending_selected.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79  ' + valueSpending + '%, #fff ' + valueSpending + '%, white 100%)';
    } else {
        document.getElementById('spendingLabel').innerHTML = parseInt(Value_current_spending_selected).toLocaleString('en-US');
    }

    // if the user is not retired

    document.getElementById('ageRetireLabel').innerHTML = Value_current_age_retire_selected;
    if (sessionStorage.getItem("Value_current_age_retire_selected$") != null) {
        document.getElementById('ageRetireLabel').innerHTML = parseInt(sessionStorage.getItem("Value_current_age_retire_selected$")).toLocaleString('en-US');
        let valueAgeRetire = (current_age_retire_selected.value - current_age_retire_selected.min) / (current_age_retire_selected.max - current_age_retire_selected.min) * 100;
        current_age_retire_selected.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79  ' + valueAgeRetire + '%, #fff ' + valueAgeRetire + '%, white 100%)';
    }

    document.getElementById('neededLabel').innerHTML = parseInt(Value_current_needed_selected).toLocaleString('en-US');
    if (sessionStorage.getItem("Value_current_needed_selected$") != null) {
        document.getElementById('neededLabel').innerHTML = parseInt(sessionStorage.getItem("Value_current_needed_selected$")).toLocaleString('en-US');
        let valueNeeded = (current_needed_selected.value - current_needed_selected.min) / (current_needed_selected.max - current_needed_selected.min) * 100;
        current_needed_selected.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79  ' + valueNeeded + '%, #fff ' + valueNeeded + '%, white 100%)';
    }

    document.getElementById('savedLabel').innerHTML = parseInt(Value_current_saved_selected).toLocaleString('en-US');
    if (sessionStorage.getItem("Value_current_saved_selected$") != null) {
        document.getElementById('savedLabel').innerHTML = parseInt(sessionStorage.getItem("Value_current_saved_selected$")).toLocaleString('en-US');
        let valueSaved = (current_saved_selected.value - current_saved_selected.min) / (current_saved_selected.max - current_saved_selected.min) * 100;
        current_saved_selected.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79  ' + valueSaved + '%, #fff ' + valueSaved + '%, white 100%)';

    }

    //Load values by default

    $(function() {


        $('#fieldsRetired').hide();
        $('#fieldsNoRetired').hide();
        $('#buttonsForm1').hide();
        $('#buttonsForm2').hide();

        document.getElementById('nextGraph2').style.display = "none";

    });

    cargar();


});

let ctx_calculator2 = document.getElementById('myChart_calculator2');
let myChart_calculator2 = null;

// valores por defecto en la grafica
createGraph2(0, 0);

function cargar() {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 & this.status == 200) {
            let obj = JSON.parse(xhttp.responseText);

            // Gender as first condition then Retire Status
            Value_current_spending_selected = parseInt(current_spending_selected.value);
            // Load values from sessionStorage to be used in graph
            Value_current_gender_selected = sessionStorage.getItem('Value_current_gender_selected$');
            Value_current_retired_status = sessionStorage.getItem('Value_current_retired_status$');

            const default_average_return = 5 / 100;
            money_saved_already = sessionStorage.getItem('Value_current_saved_selected$');


            if (sessionStorage.getItem('Value_current_withdrawal_selected$') != null) {
                Value_current_withdrawal_selected = sessionStorage.getItem('Value_current_withdrawal_selected$');
            } else {
                Value_current_withdrawal_selected = document.getElementById('current_withdrawal_selected').value;
            }

            if (Value_current_gender_selected == "Male") {
                if (Value_current_retired_status == "Yes") {
                    Monthly_withdrawal_with_SAVVLY = Value_current_withdrawal_selected * newaverage_return / 12;

                    Monthly_withdrawal_without_SAVVLY = Value_current_withdrawal_selected * Annual_withdrawal_percentage_without / 12;

                    let withoutRounded = Math.round(Monthly_withdrawal_without_SAVVLY);
                    let withRounded = Math.round(Monthly_withdrawal_with_SAVVLY);

                    document.getElementById('withsavvly').innerHTML = parseInt(withRounded).toLocaleString('en-US');
                    document.getElementById('withoutsavvly').innerHTML = parseInt(withoutRounded).toLocaleString('en-US');

                    // document.getElementById('withsavvly2').innerHTML = parseInt(withRounded).toLocaleString('en-US');
                    // document.getElementById('withoutsavvly2').innerHTML = parseInt(withoutRounded).toLocaleString('en-US');
                    document.getElementById('withoutsavvly2').innerHTML = parseInt(sessionStorage.getItem('Montly_installment_XX$')).toLocaleString('en-US');
                    document.getElementById('withsavvly2').innerHTML = parseInt(sessionStorage.getItem('Montly_installment_YY$')).toLocaleString('en-US');

                    sessionStorage.setItem("prueba", parseInt(withRounded).toLocaleString('en-US'));

                    let newValue = parseInt(withoutRounded);
                    if (parseInt(Value_current_spending_selected) > newValue) {
                        // document.getElementById('myWarning').style.display = "block";
                        document.getElementById('myWarning').style.visibility = "visible";
                        document.getElementById('warningLabel').innerHTML = "You are at risk of running out money";
                    } else {
                        // document.getElementById('myWarning').style.display = "none";
                        document.getElementById('myWarning').style.visibility = "hidden";

                    }

                    if (sessionStorage.getItem("Value_current_retired_status$") == "No") {
                        document.getElementById('myWarning2').style.visibility = "hidden";
                        let differenceWithWithout = parseInt(withoutRounded - withRounded).toLocaleString('en-US');

                        // document.getElementById('withoutSavv2').innerHTML =
                        //     "Without Savvly you will need to save <br><b style='color:#0b6e79'> $" + differenceWithWithout + "</b> more to achieve your retirement goals";
                        document.getElementById('withoutSavv2').innerHTML =
                            "Without Savvly you will need to save more to achieve your retirement goals";
                    } else {
                        document.getElementById('myWarning2').style.visibility = "hidden";
                    }

                    createGraph2(withRounded, withoutRounded);
                } else {

                    let currentAge = parseInt(Value_current_age_selected);
                    let retireAge = parseInt(Value_current_age_retire_selected);

                    Annual_withdrawal_target = Value_current_needed_selected * 12;

                    //This value is the Without Savvly
                    Initial_retirement_balance = Math.pow((1 + inflation_rate), (retireAge - currentAge)) * Annual_withdrawal_target / Annual_withdrawal_percentage_without;

                    //This value is the With Savvly
                    SAVVLY_initial_retirement_balance = Initial_retirement_balance * 0.79;

                    let withoutRounded = Math.round(Initial_retirement_balance);
                    let withRounded = Math.round(SAVVLY_initial_retirement_balance);

                    document.getElementById('withsavvly').innerHTML = parseInt(withRounded).toLocaleString('en-US');
                    document.getElementById('withoutsavvly').innerHTML = parseInt(withoutRounded).toLocaleString('en-US');

                    // document.getElementById('withsavvly2').innerHTML = parseInt(withRounded).toLocaleString('en-US');
                    // document.getElementById('withoutsavvly2').innerHTML = parseInt(withoutRounded).toLocaleString('en-US');
                    document.getElementById('withoutsavvly2').innerHTML = parseInt(sessionStorage.getItem('Montly_installment_XX$')).toLocaleString('en-US');
                    document.getElementById('withsavvly2').innerHTML = parseInt(sessionStorage.getItem('Montly_installment_YY$')).toLocaleString('en-US');

                    // sessionStorage.setItem("withoutSavvlyVal", parseInt(withoutRounded));
                    // sessionStorage.setItem("withoutSavvlyValMain", parseInt(Value_current_spending_selected));

                    let newValue = parseInt(withoutRounded);
                    if (parseInt(Value_current_spending_selected) > newValue) {
                        // document.getElementById('myWarning').style.display = "block";
                        document.getElementById('myWarning').style.visibility = "visible";
                        document.getElementById('withSavvY').innerHTML = "This is how much you can safely spend with <b>SAVVLY</b>";
                        document.getElementById('withoutSavvY').innerHTML = "This is the most you should be spending a month to avoid running out.";

                        // document.getElementById('withSavv2').innerHTML = "This is how much you can safely spend with <b>SAVVLY</b>";
                        // document.getElementById('withoutSavv2').innerHTML = "This is the most you should be spending a month to avoid running out.";

                    } else {
                        // document.getElementById('myWarning').style.display = "none";
                        document.getElementById('myWarning').style.visibility = "hidden";
                        document.getElementById('withSavvY').innerHTML = "This is how much you can safely spend with <b>SAVVLY</b>";
                        document.getElementById('withoutSavvY').innerHTML = "This is the most you should be spending a month to avoid running out.";

                        // document.getElementById('withSavv2').innerHTML = "This is how much you can safely spend with <b>SAVVLY</b>";
                        // document.getElementById('withoutSavv2').innerHTML = "This is the most you should be spending a month to avoid running out.";
                    }

                    if (sessionStorage.getItem("Value_current_retired_status$") == "No") {
                        document.getElementById('myWarning2').style.visibility = "hidden";
                        let differenceWithWithout = parseInt(withoutRounded - withRounded).toLocaleString('en-US');

                        // document.getElementById('withoutSavv2').innerHTML =
                        //     "Without Savvly you will need to save <br><b style='color:#0b6e79'> $" + differenceWithWithout + "</b> more to achieve your retirement goals";

                        document.getElementById('withoutSavv2').innerHTML =
                            "Without Savvly you will need to save more to achieve your retirement goals";


                        document.getElementById('withSavv2').innerHTML = "With <b>SAVVLY</b> you will need only this";

                    } else {
                        document.getElementById('myWarning2').style.visibility = "hidden";
                    }

                    // Comentarios sobre la formula:
                    // (withoutRounded - money_saved_already) * 0.05 = 98,946.05
                    //[Math.pow((1 + 0.05), (12 * (retireAge - currentAge))) - 1] = 121,738.57
                    // (withoutRounded - money_saved_already) * 0.05% = 989.4605
                    //[Math.pow((1 + 0.05%), (12 * (retireAge - currentAge))) - 1] = 0.1274630

                    let myAgeCalculator = 12 * (retireAge - currentAge);

                    Montly_installment_XX = (withoutRounded - money_saved_already) * (newaverage_return / 12) / (Math.pow((1 + (newaverage_return / 12)), myAgeCalculator) - 1);
                    Montly_installment_YY = (withRounded - money_saved_already) * (newaverage_return / 12) / (Math.pow((1 + (newaverage_return / 12)), myAgeCalculator) - 1);

                    sessionStorage.setItem('Montly_installment_XX$', Montly_installment_XX);
                    sessionStorage.setItem('Montly_installment_YY$', Montly_installment_YY);

                    document.getElementById('montly_installment_XX').innerHTML = parseInt(Montly_installment_XX).toLocaleString('en-US');
                    document.getElementById('montly_installment_YY').innerHTML = parseInt(Montly_installment_YY).toLocaleString('en-US');

                    Montly_installment_YY_Percent = Math.round(Montly_installment_YY * 10 / 100);
                    sessionStorage.setItem("monthly_percent$", Montly_installment_YY_Percent);
                    console.log(Montly_installment_YY_Percent);

                    createGraph2(withRounded, withoutRounded);
                }

            } else if (Value_current_gender_selected == "Female") {
                if (Value_current_retired_status == "Yes") {
                    Monthly_withdrawal_with_SAVVLY = Value_current_withdrawal_selected * default_value / 12;

                    Monthly_withdrawal_without_SAVVLY = Value_current_withdrawal_selected * Annual_withdrawal_percentage_without / 12;

                    let withoutRounded = Math.round(Monthly_withdrawal_without_SAVVLY);
                    let withRounded = Math.round(Monthly_withdrawal_with_SAVVLY);

                    document.getElementById('withsavvly').innerHTML = parseInt(withRounded).toLocaleString('en-US');
                    document.getElementById('withoutsavvly').innerHTML = parseInt(withoutRounded).toLocaleString('en-US');

                    // document.getElementById('withsavvly2').innerHTML = parseInt(withRounded).toLocaleString('en-US');
                    // document.getElementById('withoutsavvly2').innerHTML = parseInt(withoutRounded).toLocaleString('en-US');
                    document.getElementById('withoutsavvly2').innerHTML = parseInt(sessionStorage.getItem('Montly_installment_XX$')).toLocaleString('en-US');
                    document.getElementById('withsavvly2').innerHTML = parseInt(sessionStorage.getItem('Montly_installment_YY$')).toLocaleString('en-US');


                    // sessionStorage.setItem("withoutSavvlyVal", parseInt(withoutRounded));
                    // sessionStorage.setItem("withoutSavvlyValMain", parseInt(Value_current_spending_selected));

                    let newValue = parseInt(withoutRounded);
                    if (parseInt(Value_current_spending_selected) > newValue) {
                        // document.getElementById('myWarning').style.display = "block";
                        document.getElementById('myWarning').style.visibility = "visible";
                        document.getElementById('warningLabel').innerHTML = "You are at risk of running out money";

                    } else {
                        // document.getElementById('myWarning').style.display = "none";
                        document.getElementById('myWarning').style.visibility = "hidden";
                    }

                    if (sessionStorage.getItem("Value_current_retired_status$") == "No") {
                        document.getElementById('myWarning2').style.visibility = "hidden";
                        let differenceWithWithout = parseInt(withoutRounded - withRounded).toLocaleString('en-US');

                        // document.getElementById('withoutSavv2').innerHTML =
                        //     "Without Savvly you will need to save <br><b style='color:#0b6e79'> $" + differenceWithWithout + "</b> more to achieve your retirement goals";

                        document.getElementById('withoutSavv2').innerHTML =
                            "Without Savvly you will need to save more to achieve your retirement goals";
                        document.getElementById('withSavv2').innerHTML = "With <b>SAVVLY</b> you will need only this";
                    } else {
                        document.getElementById('myWarning2').style.visibility = "hidden";
                    }

                    createGraph2(withRounded, withoutRounded);
                } else {

                    let currentAge = parseInt(Value_current_age_selected);
                    let retireAge = parseInt(Value_current_age_retire_selected);

                    Annual_withdrawal_target = Value_current_needed_selected * 12;

                    //This value is the Without Savvly
                    Initial_retirement_balance = Math.pow((1 + inflation_rate), (retireAge - currentAge)) * Annual_withdrawal_target / Annual_withdrawal_percentage_without;

                    //This value is the With Savvly
                    SAVVLY_initial_retirement_balance = Initial_retirement_balance * 0.85;

                    console.log({ Initial_retirement_balance, SAVVLY_initial_retirement_balance });

                    let withoutRounded = Math.round(Initial_retirement_balance);
                    let withRounded = Math.round(SAVVLY_initial_retirement_balance);

                    document.getElementById('withsavvly').innerHTML = parseInt(withRounded).toLocaleString('en-US');
                    document.getElementById('withoutsavvly').innerHTML = parseInt(withoutRounded).toLocaleString('en-US');

                    // document.getElementById('withsavvly2').innerHTML = parseInt(withRounded).toLocaleString('en-US');
                    // document.getElementById('withoutsavvly2').innerHTML = parseInt(withoutRounded).toLocaleString('en-US');
                    document.getElementById('withoutsavvly2').innerHTML = parseInt(sessionStorage.getItem('Montly_installment_XX$')).toLocaleString('en-US');
                    document.getElementById('withsavvly2').innerHTML = parseInt(sessionStorage.getItem('Montly_installment_YY$')).toLocaleString('en-US');


                    let newValue = parseInt(withoutRounded);
                    if (parseInt(Value_current_spending_selected) > newValue) {
                        // document.getElementById('myWarning').style.display = "block";
                        document.getElementById('myWarning').style.visibility = "visible";
                        document.getElementById('warningLabel').innerHTML = "You are at risk of running out money";
                    } else {
                        // document.getElementById('myWarning').style.display = "none";
                        document.getElementById('myWarning').style.visibility = "hidden";
                    }

                    if (sessionStorage.getItem("Value_current_retired_status$") == "No") {
                        document.getElementById('myWarning2').style.visibility = "hidden";
                        let differenceWithWithout = parseInt(withoutRounded - withRounded).toLocaleString('en-US');

                        // document.getElementById('withoutSavv2').innerHTML =
                        //     "Without Savvly you will need to save <br><b style='color:#0b6e79'> $" + differenceWithWithout + "</b> more to achieve your retirement goals";
                        document.getElementById('withoutSavv2').innerHTML =
                            "Without Savvly you will need to save more to achieve your retirement goals";

                        document.getElementById('withSavv2').innerHTML = "With <b>SAVVLY</b> you will need only this";
                    } else {
                        document.getElementById('myWarning2').style.visibility = "hidden";
                    }

                    // Montly_installment_XX = (withoutRounded - money_saved_already) * default_average_return;
                    // console.log("Antes del exponente" + Montly_installment_XX);

                    // Montly_installment_XX = Math.pow((1 + default_average_return), (12 * (retireAge - currentAge))) - 1;
                    // console.log("Valor del exponente" + Montly_installment_XX);
                    let myAgeCalculator = 12 * (retireAge - currentAge);

                    Montly_installment_XX = (withoutRounded - money_saved_already) * (newaverage_return / 12) / (Math.pow((1 + (newaverage_return / 12)), myAgeCalculator) - 1);
                    Montly_installment_YY = (withRounded - money_saved_already) * (newaverage_return / 12) / (Math.pow((1 + (newaverage_return / 12)), myAgeCalculator) - 1);

                    sessionStorage.setItem('Montly_installment_XX$', Montly_installment_XX);
                    sessionStorage.setItem('Montly_installment_YY$', Montly_installment_YY);

                    console.log(Montly_installment_XX);
                    console.log(Montly_installment_YY);

                    document.getElementById('montly_installment_XX').innerHTML = parseInt(Montly_installment_XX).toLocaleString('en-US');
                    document.getElementById('montly_installment_YY').innerHTML = parseInt(Montly_installment_YY).toLocaleString('en-US');

                    Montly_installment_YY_Percent = Math.round(Montly_installment_YY * 10 / 100);
                    sessionStorage.setItem("monthly_percent$", Montly_installment_YY_Percent);
                    console.log(Montly_installment_YY_Percent);

                    createGraph2(withRounded, withoutRounded);
                }

            } else {
                createGraph2(0, 0);
            }
        }
    };

    xhttp.open("GET", "livenumbers.json", true);
    xhttp.send();
}

function nextPrincipalRanges() {

    if ((Value_current_gender_selected == "Male" || Value_current_gender_selected == "Female") && Value_current_retired_status == "Yes") {

        if (Value_current_age_selected2 >= 60) {
            console.log('Input Ranges estan siendo mostrados');

            $('#nextPrincipal').hide();
            $('#fieldsRetired').show();
            $('#buttonsForm1').show();

            // Save Age in sessionStorage to be displayed in next window

            Value_current_age_selected2 = current_age_selected2.value;
            sessionStorage.setItem("Value_current_age_selected2$", Value_current_age_selected2);
            $('#current_age_selected2').val(sessionStorage.getItem("Value_current_age_selected2$"));
            Value_current_age_selected2 = sessionStorage.getItem("Value_current_age_selected2$");
            document.getElementById('ageLabelIfRetireY').innerHTML = sessionStorage.getItem("Value_current_age_selected2$");
            let valueAgeSelected2 = (current_age_selected2.value - current_age_selected2.min) / (current_age_selected2.max - current_age_selected2.min) * 100;
            current_age_selected2.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79  ' + valueAgeSelected2 + '%, #fff ' + valueAgeSelected2 + '%, white 100%)';

            document.getElementById('current_retired_status').disabled = true;
            document.getElementById('current_gender_selected').disabled = true;

            //Set Age in sessionStorage to load in the next page
            // sessionStorage.setItem("Value_current_age_selected$", Value_current_age_selected);
        }
    } else if ((Value_current_gender_selected == "Male" || Value_current_gender_selected == "Female") && Value_current_retired_status == "No") {

        if (Value_current_age_selected != 18) {
            console.log('Input Ranges estan siendo mostrados');

            $('#fieldsNoRetired').show();
            $('#buttonsForm2').show();
            $('#buttonsForm1').hide();
            $('#nextPrincipal').hide();



            // Save Age in sessionStorage to be displayed in next window
            Value_current_age_selected = current_age_selected.value;
            sessionStorage.setItem("Value_current_age_selected$", Value_current_age_selected);
            $('#current_age_selected').val(sessionStorage.getItem("Value_current_age_selected$"));
            Value_current_age_selected = sessionStorage.getItem("Value_current_age_selected$");
            document.getElementById('ageLabel').innerHTML = sessionStorage.getItem("Value_current_age_selected$");
            let valueAgeSelected = (current_age_selected.value - current_age_selected.min) / (current_age_selected.max - current_age_selected.min) * 100;
            current_age_selected.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79  ' + valueAgeSelected + '%, #fff ' + valueAgeSelected + '%, white 100%)';

            document.getElementById('current_retired_status').disabled = true;
            document.getElementById('current_gender_selected').disabled = true;
        }

    } else {
        $('#fieldsRetired').hide();
        $('#fieldsNoRetired').hide();
        $('#buttonsForm1').hide();
        $('#buttonsForm2').hide();
    }
}

function resetValues() {
    $('#current_gender_selected').val('Choose...');
    sessionStorage.setItem("Value_current_retired_status$", 'Choose...');
    sessionStorage.setItem("Value_current_age_selected$", 18);
    sessionStorage.setItem("Value_current_age_selected2$", 60);
    sessionStorage.setItem("Value_current_spending_selected$", 0);
    sessionStorage.setItem("Value_current_age_retire_selected$", 60);
    sessionStorage.setItem("Value_current_needed_selected$", 0);
    sessionStorage.setItem("Value_current_saved_selected$", 0);

    // ifRetiredY clean Ranges
    sessionStorage.setItem("Value_current_withdrawal_selected$", 100000);
    window.location.reload();
}

function showGraph_RetiredY() {
    document.getElementById('graph1').style.display = "block";
    document.getElementById('next1').style.display = "none";
    document.getElementById('withSavvY').innerHTML = "This is how much you can safely spend with <b>SAVVLY</b>";
    document.getElementById('withoutSavvY').innerHTML = "This is the most you should be spending a month to avoid running out.";

    // document.getElementById('withSavv2').innerHTML = "This is how much you can safely spend with <b>SAVVLY</b>";
    // document.getElementById('withoutSavv2').innerHTML = "This is the most you should be spending a month to avoid running out.";
    // document.getElementById('withSavv').style.display = "block";
    // document.getElementById('withoutSavv').style.display = "block";

    // labels inside the graph1
    // document.getElementById('myWarning')

}

function showGraph_RetiredN() {
    document.getElementById('graph1').style.display = "block";
    document.getElementById('next2').style.display = "none";
    document.getElementById('nextGraph2').style.display = "block";
    // document.getElementById('withSavv2').innerHTML = "This is how much you can safely spend with <b>SAVVLY</b>";
    // document.getElementById('withoutSavv2').innerHTML = "This is the most you should be spending a month to avoid running out.";

    let differenceWithWithout = parseInt(withoutRounded - withRounded).toLocaleString('en-US');

    // document.getElementById('withoutSavv2').innerHTML = "Without Savvly you will need to save <br><b style='color:#0b6e79'> $" + differenceWithWithout + "</b> more to achieve your retirement goals";
    document.getElementById('withoutSavv2').innerHTML = "Without Savvly you will need to save more to achieve your retirement goals";

    document.getElementById('withSavv2').innerHTML = "With <b>SAVVLY</b> you will need only this";
}



current_gender_selected.oninput = function() {
    Value_current_gender_selected = current_gender_selected.value;
    sessionStorage.setItem("Value_current_gender_selected$", Value_current_gender_selected);

    // if (sessionStorage.getItem("Value_current_gender_selected$") == "Male") {
    //     Value_current_gender_selected = "Male";
    //     $('#current_gender_selected').val(sessionStorage.getItem("Value_current_gender_selected$"));
    // } else if (sessionStorage.getItem("Value_current_gender_selected$") == "Female") {
    //     Value_current_gender_selected = "Female";
    //     $('#current_gender_selected').val(sessionStorage.getItem("Value_current_gender_selected$"));
    // } else {
    //     Value_current_gender_selected = "Choose...";
    //     $('#current_gender_selected').val('Choose...');
    // }
}
current_gender_selected.addEventListener("change", cargar);

current_retired_status.oninput = function() {
    Value_current_retired_status = current_retired_status.value;
    sessionStorage.setItem("Value_current_retired_status$", Value_current_retired_status);

    // ageIfRetiredY, ageIfRetiredN
    if (sessionStorage.getItem("Value_current_retired_status$") == "Yes") {
        $('#ageIfRetiredY').show();
        $('#ageIfRetiredN').hide();
    } else {
        $('#ageIfRetiredY').hide();
        $('#ageIfRetiredN').show();
    }


    // if (sessionStorage.getItem('Value_current_age_selected$') != 18) {
    //     if (sessionStorage.getItem("Value_current_retired_status$") == "Yes") {
    //         $('#fieldsRetired').show();
    //         $('#buttonsForm1').show();
    //         document.getElementById('warningLabel').innerHTML =
    //             "You are at risk of running out money";
    //         document.getElementById('withSavv').innerHTML =
    //             "This is how much you can safely spend with <b>SAVVLY</b>";
    //         document.getElementById('withoutSavv').innerHTML =
    //             "This is the most you should be spending a month to avoid running out.";
    //         $('#fieldsNoRetired').hide();
    //         $('#buttonsForm2').hide();
    //         $('#current_retired_status').val(sessionStorage.getItem("Value_current_retired_status$"));
    //     }
    // }
    // if (sessionStorage.getItem("Value_current_retired_status$") == "Yes") {
    //         $('#fieldsRetired').show();
    //         $('#buttonsForm1').show();
    //         document.getElementById('warningLabel').innerHTML =
    //             "You are at risk of running out money";
    //         document.getElementById('withSavv').innerHTML =
    //             "This is how much you can safely spend with <b>SAVVLY</b>";
    //         document.getElementById('withoutSavv').innerHTML =
    //             "This is the most you should be spending a month to avoid running out.";
    //         $('#fieldsNoRetired').hide();
    //         $('#buttonsForm2').hide();
    //         $('#current_retired_status').val(sessionStorage.getItem("Value_current_retired_status$"));
    // } 
    // else if (sessionStorage.getItem("Value_current_retired_status$") == 'No') {
    //     $('#fieldsNoRetired').show();
    //     $('#buttonsForm2').show();
    //     $('#buttonsForm1').hide();
    //     document.getElementById('warningLabel').innerHTML =
    //         "Without Savvly you will need to save much more to retire.";
    //     document.getElementById('withSavv').innerHTML =
    //         "With <b>SAVVLY</b> you need only this.";
    //     document.getElementById('withoutSavv').innerHTML =
    //         "Without Savvly you will need to save " + "xxx" + " more to achieve your retirement goals";


    //     $('#fieldsRetired').hide();

    //     $('#current_retired_status').val(sessionStorage.getItem("Value_current_retired_status$"));
    // } else {
    //     $('#fieldsRetired').hide();
    //     $('#fieldsNoRetired').hide();
    //     $('#buttonsForm1').hide();
    //     $('#buttonsForm2').hide();

    //     Value_current_retired_status = "Choose...";
    //     $('#current_retired_status').val('Choose...');
    // }
}
current_retired_status.addEventListener("change", cargar);

function compareAgeWithRetirement() {
    if (Value_current_age_selected >= Value_current_age_retire_selected) {
        current_age_retire_selected.value = parseInt(Value_current_age_selected) + 1;
        var value = (current_age_retire_selected.value - current_age_retire_selected.min) / (current_age_retire_selected.max - current_age_retire_selected.min) * 100;
        current_age_retire_selected.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79  ' + value + '%, #fff ' + value + '%, white 100%)';
        document.getElementById('ageRetireLabel').innerHTML = parseInt(Value_current_age_selected) + 1;
    }
}

current_age_selected.oninput = function() {
    Value_current_age_selected = current_age_selected.value;
    sessionStorage.setItem("Value_current_age_selected$", Value_current_age_selected);
    document.getElementById('ageLabel').innerHTML = Value_current_age_selected;
    var valueAgeSelected = (this.value - this.min) / (this.max - this.min) * 100;
    this.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79  ' + valueAgeSelected + '%, #fff ' + valueAgeSelected + '%, white 100%)';

    if (Value_current_age_selected > Value_current_age_retire_selected) {
        alert('Your retire age should be greater than current age');
        compareAgeWithRetirement();
    }
}
current_age_selected.addEventListener("change", cargar);

current_age_selected2.oninput = function() {
    Value_current_age_selected2 = current_age_selected2.value;
    sessionStorage.setItem("Value_current_age_selected2$", Value_current_age_selected2);
    document.getElementById('ageLabelIfRetireY').innerHTML = Value_current_age_selected2;
    // document.getElementById('warningAge').innerHTML = Value_current_age_selected2;

    var valueAgeSelected2 = (this.value - this.min) / (this.max - this.min) * 100;
    this.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79  ' + valueAgeSelected2 + '%, #fff ' + valueAgeSelected2 + '%, white 100%)';
}
current_age_selected2.addEventListener("change", cargar);

current_withdrawal_selected.oninput = function() {
    Value_current_withdrawal_selected = parseInt(current_withdrawal_selected.value);
    document.getElementById('withdrawalLabel').innerHTML = parseInt(Value_current_withdrawal_selected).toLocaleString('en-US');
    sessionStorage.setItem("Value_current_withdrawal_selected$", Value_current_withdrawal_selected);

    var valueWithdrawalSelected = (this.value - this.min) / (this.max - this.min) * 100;
    this.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79 ' + valueWithdrawalSelected + '%, #fff ' + valueWithdrawalSelected + '%, white 100%)';
}
current_withdrawal_selected.addEventListener("change", cargar);

current_spending_selected.oninput = function() {
    Value_current_spending_selected = parseInt(current_spending_selected.value);
    document.getElementById('spendingLabel').innerHTML = parseInt(Value_current_spending_selected).toLocaleString('en-US');
    sessionStorage.setItem("Value_current_spending_selected$", Value_current_spending_selected);

    var valueSpendingSelected = (this.value - this.min) / (this.max - this.min) * 100;
    this.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79 ' + valueSpendingSelected + '%, #fff ' + valueSpendingSelected + '%, white 100%)';
}
current_spending_selected.addEventListener("change", cargar);

// If the user is NOT RETIRED

current_age_retire_selected.oninput = function() {
    Value_current_age_retire_selected = current_age_retire_selected.value;
    document.getElementById('ageRetireLabel').innerHTML = Value_current_age_retire_selected;
    sessionStorage.setItem("Value_current_age_retire_selected$", Value_current_age_retire_selected);

    // document.getElementById('warningAge').innerHTML = Value_current_age_retire_selected;

    var valueAgeRetireSelected = (this.value - this.min) / (this.max - this.min) * 100;
    this.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79  ' + valueAgeRetireSelected + '%, #fff ' + valueAgeRetireSelected + '%, white 100%)';
}
current_age_retire_selected.addEventListener("change", cargar);

current_needed_selected.oninput = function() {
    Value_current_needed_selected = parseInt(current_needed_selected.value);
    document.getElementById('neededLabel').innerHTML = parseInt(Value_current_needed_selected).toLocaleString('en-US');
    sessionStorage.setItem("Value_current_needed_selected$", Value_current_needed_selected);

    var valueNeededSelected = (this.value - this.min) / (this.max - this.min) * 100;
    this.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79 ' + valueNeededSelected + '%, #fff ' + valueNeededSelected + '%, white 100%)';
}
current_needed_selected.addEventListener("change", cargar);

current_saved_selected.oninput = function() {
    Value_current_saved_selected = parseInt(current_saved_selected.value);
    document.getElementById('savedLabel').innerHTML = parseInt(Value_current_saved_selected).toLocaleString('en-US');
    sessionStorage.setItem("Value_current_saved_selected$", Value_current_saved_selected);

    var valueSavedSelected = (this.value - this.min) / (this.max - this.min) * 100;
    this.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79 ' + valueSavedSelected + '%, #fff ' + valueSavedSelected + '%, white 100%)';
}
current_saved_selected.addEventListener("change", cargar);

function createGraph2(valor1, valor2) {
    if (myChart_calculator2 !== null) {
        myChart_calculator2.destroy();
    }
    myChart_calculator2 = new Chart(ctx_calculator2, {
        type: 'bar',
        data: {
            labels: ['With Savvly', 'Without Savvly'],
            datasets: [{
                label: '',
                data: [valor1, valor2],
                minBarLength: 10,
                barThickness: 100,
                backgroundColor: [
                    '#FFAD78',
                    '#0B6E79'
                ],
                datalabels: {
                    color: '#000',
                    font: {
                        weight: 'bold',
                        size: 13,
                        family: 'Roboto'
                    },
                    formatter: (value, context) => {
                        return '$ ' + parseInt(value).toLocaleString('en-US');
                    },
                    anchor: 'end',
                    align: 'top',
                    offset: 0,
                    display: true
                }

            }]
        },
        options: {
            layout: {
                padding: {
                    top: 32
                }
            },
            legend: {
                display: false,
                labels: {
                    color: '#fff'
                }

            },

            tooltips: {
                callbacks: {
                    label: function(tooltipItem) {
                        return tooltipItem.yLabel;
                    }
                }
            },
            scales: {
                yAxes: [{
                    gridLines: {
                        drawBorder: false,
                        display: false
                    },
                    ticks: {
                        display: false,
                        beginAtZero: true,

                    }
                }],

                xAxes: [{
                    gridLines: {
                        drawBorder: false,
                        display: false
                    },
                    ticks: {
                        fontSize: 16

                    }
                }]
            }
        },
    });
}