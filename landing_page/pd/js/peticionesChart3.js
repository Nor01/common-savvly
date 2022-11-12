let valueCurrent_ageI = 0;
let default_ageI = 0;
let default_genderI = 0;
let default_fundingI = 0;
let valueCurrent_genderI = 0;
let without_multiplier = 0;
let valueCurrent_payoutI = 0;
let withRounded = 0;
let withoutRounded = 0;
let multiplierRound = 0;
let male_multiplier = 0;
let installment_without = 0;
let final_without_multiplier = 0;

const average_return = 6 / 100;

let valueCurrent_averageReturnI = 0;
let default_minstallmentI = 0;
let default_retirementAgeI = 0;

let current_ageI = document.getElementById("current_ageI");
let current_genderI = document.getElementById("current_genderI");
let current_fundingamountI = document.getElementById("current_fundingamountI");

let current_averageReturnI = document.getElementById("current_averageReturnI");

let current_payoutI = document.getElementById("current_payoutI");
let current_minstallmentI = document.getElementById("current_minstallmentI");
let current_retirementAgeI = document.getElementById("current_retirementAgeI");

let newPercent = 0;

valueCurrent_ageI = current_ageI.value;

document.addEventListener('DOMContentLoaded', () => {
    // valueCurrent_ageI = current_ageI.value;
    // valueCurrent_genderI = current_genderI.value;

    newPercent = parseInt(sessionStorage.getItem('Value_current_saved_selected$')) * 10 / 100;
    console.log(newPercent);

    document.getElementById('current_genderI').disabled = true;
    document.getElementById('current_ageI').disabled = true;



    valueCurrent_fundingamountI = current_fundingamountI.value;
    valueCurrent_averageReturnI = current_averageReturnI.value / 100;

    valueCurrent_payoutI = parseInt(current_payoutI.value);
    valueCurrent_minstallmentI = parseInt(current_minstallmentI.value);
    valueCurrent_retirementAgeI = parseInt(current_retirementAgeI.value);

    // document.getElementById('demo').innerHTML = parseInt(valueCurrent_fundingamountI).toLocaleString('en-US');
    // document.getElementById('demoAge').innerHTML = valueCurrent_ageI;
    document.getElementById('demo2').innerHTML = valueCurrent_payoutI;

    if (sessionStorage.getItem('monthly_percent$') != null) {
        document.getElementById('demo3').innerHTML = sessionStorage.getItem('monthly_percent$');
        $('#current_minstallmentI').val(sessionStorage.getItem('monthly_percent$'));
        let installPercent = (current_minstallmentI.value - current_minstallmentI.min) / (current_minstallmentI.max - current_minstallmentI.min) * 100;
        current_minstallmentI.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79  ' + installPercent + '%, #fff ' + installPercent + '%, white 100%)';
    } else {
        document.getElementById('demo3').innerHTML = valueCurrent_minstallmentI;
        $('#current_minstallmentI').val(valueCurrent_minstallmentI);
    }


    // document.getElementById('labelPercent').innerHTML = valueCurrent_fundingamountI;


    $('#current_genderI').val(sessionStorage.getItem("Value_current_gender_selected$"));
    valueCurrent_genderI = sessionStorage.getItem("Value_current_gender_selected$");


    if (sessionStorage.getItem("Value_current_age_selected$") != null) {
        $('#current_ageI').val(sessionStorage.getItem("Value_current_age_selected$"));
        valueCurrent_ageI = sessionStorage.getItem("Value_current_age_selected$");
        document.getElementById('demoAge').innerHTML = sessionStorage.getItem("Value_current_age_selected$");
        let valueCurrentAge = (current_ageI.value - current_ageI.min) / (current_ageI.max - current_ageI.min) * 100;
        current_ageI.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79  ' + valueCurrentAge + '%, #fff ' + valueCurrentAge + '%, white 100%)';
    } else {
        document.getElementById('demoAge').innerHTML = valueCurrent_ageI;
    }

    // document.getElementById('demo').innerHTML = parseInt(valueCurrent_fundingamountI).toLocaleString('en-US');
    // if (sessionStorage.getItem('valueCurrent_fundingamountI$') != null) {
    //     document.getElementById('demo').innerHTML = parseInt(sessionStorage.getItem("valueCurrent_fundingamountI$")).toLocaleString('en-US');
    //     let valueFundingAmount = (current_fundingamountI.value - current_fundingamountI.min) / (current_fundingamountI.max - current_fundingamountI.min) * 100;
    //     current_fundingamountI.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79  ' + valueFundingAmount + '%, #fff ' + valueFundingAmount + '%, white 100%)';
    // }

    if (sessionStorage.getItem('valueCurrent_fundingamountI$') != null) {
        document.getElementById('demo').innerHTML = 10 + "% ( $" + parseInt(newPercent).toLocaleString('en-US') + ")";
        document.getElementById('labelPercent').innerHTML = '10';
        let valueFundingAmount = (current_fundingamountI.value - current_fundingamountI.min) / (current_fundingamountI.max - current_fundingamountI.min) * 100;
        current_fundingamountI.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79  ' + valueFundingAmount + '%, #fff ' + valueFundingAmount + '%, white 100%)';
    } else {
        document.getElementById('demo').innerHTML = 10 + "% ( $" + parseInt(newPercent).toLocaleString('en-US') + ")";
        document.getElementById('labelPercent').innerHTML = 10;
    }

    // document.getElementById('multiValue').innerHTML = '2.77x';
    document.getElementById('currentAgeSelected').innerHTML = '85';
    document.getElementById('ageFinal').innerHTML = '85';
    document.getElementById("current_ageI").addEventListener('change', cargar);
    document.getElementById("current_retirementAgeI").addEventListener('change', cargar);

    cargar();
    document.getElementById('withsavvlyRetire').innerHTML = parseInt(withRounded).toLocaleString('en-US');
    document.getElementById('lumpsumFinal').innerHTML = parseInt(withRounded).toLocaleString('en-US');
    document.getElementById('withoutsavvlyRetire').innerHTML = parseInt(withoutRounded).toLocaleString('en-US');
    document.getElementById('withsavvlyRetire2').innerHTML = parseInt(withRounded).toLocaleString('en-US');

});

let ctx = document.getElementById('myChart2');
let myChart = null;

// valores por defecto en la grafica
crearGrafica(457822, 151280);

function compareAge() {
    if (valueCurrent_ageI >= valueCurrent_payoutI) {
        current_payoutI.value = parseInt(valueCurrent_ageI) + 1;
        // console.log(current_payoutI.value);
        var value = (current_payoutI.value - current_payoutI.min) / (current_payoutI.max - current_payoutI.min) * 100;
        current_payoutI.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79  ' + value + '%, #fff ' + value + '%, white 100%)';
        document.getElementById('demo2').innerHTML = parseInt(valueCurrent_ageI) + 1;
    }
}

function cargar() {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 & this.status == 200) {
            let obj = JSON.parse(xhttp.responseText);

            if (valueCurrent_minstallmentI == 0) {
                if (valueCurrent_fundingamountI == 0) {
                    withoutRounded = 0;
                    withRounded = 0;
                    multiplierRound = 0;

                    document.getElementById('currentAgeSelected').innerHTML = valueCurrent_payoutI;
                    document.getElementById('ageFinal').innerHTML = valueCurrent_payoutI;

                    document.getElementById('withsavvlyRetire').innerHTML = parseInt(withRounded).toLocaleString('en-US');
                    document.getElementById('lumpsumFinal').innerHTML = parseInt(withRounded).toLocaleString('en-US');
                    document.getElementById('withoutsavvlyRetire').innerHTML = parseInt(withoutRounded).toLocaleString('en-US');

                    document.getElementById('withsavvlyRetire2').innerHTML = parseInt(withRounded).toLocaleString('en-US');

                    // document.getElementById('multiValue').innerHTML = multiplierRound + 'x';
                    crearGrafica(withRounded, withoutRounded);
                } else {

                    without_multiplier = newPercent * Math.pow(1 + valueCurrent_averageReturnI, valueCurrent_payoutI - valueCurrent_ageI);

                    console.log('valueCurrent_minstallmentI : ', valueCurrent_averageReturnI);
                    let liveNumbersCurrAge = obj.find(item => item.age == valueCurrent_ageI);
                    let liveNumbersPoAge = obj.find(item => item.age == valueCurrent_payoutI);

                    let liveNumberMaleCur = (liveNumbersCurrAge) ? parseInt(liveNumbersCurrAge.liveMale) : 0;
                    let liveNumberFemaleCur = (liveNumbersCurrAge) ? parseInt(liveNumbersCurrAge.liveFemale) : 0;

                    let liveNumberMalePo = (liveNumbersPoAge) ? parseInt(liveNumbersPoAge.liveMale) : 0;
                    let liveNumberFemalePo = (liveNumbersPoAge) ? parseInt(liveNumbersPoAge.liveFemale) : 0;

                    let multiplier = 0;
                    let withMultiplier = 0;
                    if (valueCurrent_genderI == "Male") {
                        multiplier = (liveNumberMaleCur - liveNumberMalePo) / liveNumberMalePo + 1;
                        withMultiplier = without_multiplier * multiplier;
                        multiplier = withMultiplier / without_multiplier;

                    } else {
                        multiplier = (liveNumberFemaleCur - liveNumberFemalePo) / liveNumberFemalePo + 1;
                        withMultiplier = without_multiplier * multiplier;
                    }

                    withMultiplier = without_multiplier * multiplier;

                    let multiplierRound = multiplier.toFixed(2);
                    let withoutRounded = Math.round(without_multiplier);
                    let withRounded = Math.round(withMultiplier);

                    document.getElementById('currentAgeSelected').innerHTML = valueCurrent_payoutI;
                    document.getElementById('ageFinal').innerHTML = valueCurrent_payoutI;

                    document.getElementById('withsavvlyRetire').innerHTML = parseInt(withRounded).toLocaleString('en-US');
                    document.getElementById('lumpsumFinal').innerHTML = parseInt(withRounded).toLocaleString('en-US');
                    document.getElementById('withoutsavvlyRetire').innerHTML = parseInt(withoutRounded).toLocaleString('en-US');

                    document.getElementById('withsavvlyRetire2').innerHTML = parseInt(withRounded).toLocaleString('en-US');

                    // document.getElementById('multiValue').innerHTML = multiplierRound + 'x';
                    crearGrafica(withRounded, withoutRounded);
                }

            } else if (valueCurrent_minstallmentI != 0) {



                currAge = parseInt(valueCurrent_ageI);
                retirAge = parseInt(valueCurrent_retirementAgeI);
                currPayo = parseInt(valueCurrent_payoutI);
                valueMonthlyInstall = parseInt(valueCurrent_minstallmentI);
                // valueAverageReturn = parseInt(valueCurrent_averageReturnI) / 100;

                // console.log('valueAverageReturnParseInt : ', valueAverageReturn);

                without_multiplier = newPercent * Math.pow(1 + valueCurrent_averageReturnI, currPayo - currAge);
                console.log('valueCurrent_minstallmentI != 0 : ', valueCurrent_averageReturnI);
                installment_without = (valueCurrent_minstallmentI * 12) * (1 + (valueCurrent_averageReturnI / 2));

                if (valueCurrent_fundingamountI == 0) {

                    for ($x = currAge + 2; $x <= 65; $x++) {
                        installment_without = (installment_without * (1 + valueCurrent_averageReturnI)) + (valueCurrent_minstallmentI * 12) * (1 + (valueCurrent_averageReturnI / 2));
                    }

                    installment_without = installment_without * Math.pow(1 + valueCurrent_averageReturnI, (currPayo - retirAge));

                    if (valueCurrent_genderI == "Male") {

                        let liveNumberAtCurrentAge = obj.find(item => item.age == valueCurrent_ageI);
                        let valueLiveNumberAtCurrentAge = (liveNumberAtCurrentAge) ? parseInt(liveNumberAtCurrentAge.liveMale) : 0;
                        let liveNumberAtPayoutAge = obj.find(item => item.age == valueCurrent_payoutI);
                        let valueLiveNumberAtPayoutAge = (liveNumberAtPayoutAge) ? parseInt(liveNumberAtPayoutAge.liveMale) : 0;

                        male_multiplier = ((valueLiveNumberAtCurrentAge - valueLiveNumberAtPayoutAge) / valueLiveNumberAtPayoutAge + 1).toFixed(8);
                        withMultiplier = male_multiplier * without_multiplier;

                        let life_coeff_male = 0;

                        let liveNumberAtCurrentAgeN = obj.find(item => item.age == currAge);
                        let valueLiveNumberAtCurrentAgeN = (liveNumberAtCurrentAgeN) ? parseInt(liveNumberAtCurrentAgeN.liveMale) : 0;
                        let liveNumberAtCurrentAgeN1 = obj.find(item => item.age == (currAge + 1));
                        let valueLiveNumberAtCurrentAgeN1 = (liveNumberAtCurrentAgeN1) ? parseInt(liveNumberAtCurrentAgeN1.liveMale) : 0;

                        life_coeff_male = ((valueLiveNumberAtCurrentAgeN - valueLiveNumberAtCurrentAgeN1) / valueLiveNumberAtCurrentAgeN1);
                        installment_with = (valueMonthlyInstall * 12) * (1 + valueCurrent_averageReturnI / 2) * (1 + life_coeff_male / 2);

                        for ($i = currAge + 2; $i <= 65; $i++) {

                            let tmpliveNumberAtCurrentN1 = obj.find(item => item.age == ($i - 1));
                            let valueTmpliveNumberAtCurrentN1 = (tmpliveNumberAtCurrentN1) ? parseInt(tmpliveNumberAtCurrentN1.liveMale) : 0;
                            let tmpliveNumberAtCurrentN2 = obj.find(item => item.age == ($i));
                            let valueTmpliveNumberAtCurrentN2 = (tmpliveNumberAtCurrentN2) ? parseInt(tmpliveNumberAtCurrentN2.liveMale) : 0;

                            life_coeff_male = (valueTmpliveNumberAtCurrentN1 - valueTmpliveNumberAtCurrentN2) / valueTmpliveNumberAtCurrentN2;
                            installment_with = installment_with * (1 + valueCurrent_averageReturnI) * (1 + life_coeff_male) + (valueMonthlyInstall * 12) * (1 + (valueCurrent_averageReturnI / 2)) * (1 + (life_coeff_male / 2));
                        }

                        let multiplier_coeff = 0;
                        let liveNumberAtRetirementAge = obj.find(item => item.age == 65);
                        let valueLiveNumberAtRetirementAge = (liveNumberAtRetirementAge) ? parseInt(liveNumberAtRetirementAge.liveMale) : 0;
                        let liveNumberAtPayoutAgex = obj.find(item => item.age == valueCurrent_payoutI);
                        let valueLiveNumberAtPayoutAgex = (liveNumberAtPayoutAgex) ? parseInt(liveNumberAtPayoutAgex.liveMale) : 0;

                        multiplier_coeff = (valueLiveNumberAtRetirementAge - valueLiveNumberAtPayoutAgex) / valueLiveNumberAtPayoutAgex + 1;
                        installment_with = multiplier_coeff * installment_with * Math.pow(1 + valueCurrent_averageReturnI, (valueCurrent_payoutI - 65));

                    } else if ((valueCurrent_genderI == "Female")) {

                        let liveNumberAtCurrentAge = obj.find(item => item.age == valueCurrent_ageI);
                        let valueLiveNumberAtCurrentAge = (liveNumberAtCurrentAge) ? parseInt(liveNumberAtCurrentAge.liveFemale) : 0;
                        let liveNumberAtPayoutAge = obj.find(item => item.age == valueCurrent_payoutI);
                        let valueLiveNumberAtPayoutAge = (liveNumberAtPayoutAge) ? parseInt(liveNumberAtPayoutAge.liveFemale) : 0;

                        female_multiplier = ((valueLiveNumberAtCurrentAge - valueLiveNumberAtPayoutAge) / valueLiveNumberAtPayoutAge + 1).toFixed(8);
                        withMultiplier = female_multiplier * without_multiplier;

                        let life_coeff_female = 0;

                        let liveNumberAtCurrentAgeN = obj.find(item => item.age == currAge);
                        let valueLiveNumberAtCurrentAgeN = (liveNumberAtCurrentAgeN) ? parseInt(liveNumberAtCurrentAgeN.liveFemale) : 0;
                        let liveNumberAtCurrentAgeN1 = obj.find(item => item.age == (currAge + 1));
                        let valueLiveNumberAtCurrentAgeN1 = (liveNumberAtCurrentAgeN1) ? parseInt(liveNumberAtCurrentAgeN1.liveFemale) : 0;

                        life_coeff_female = ((valueLiveNumberAtCurrentAgeN - valueLiveNumberAtCurrentAgeN1) / valueLiveNumberAtCurrentAgeN1);
                        installment_with = (valueMonthlyInstall * 12) * (1 + valueCurrent_averageReturnI / 2) * (1 + life_coeff_female / 2);

                        for ($i = currAge + 2; $i <= 65; $i++) {

                            let tmpliveNumberAtCurrentN1 = obj.find(item => item.age == ($i - 1));
                            let valueTmpliveNumberAtCurrentN1 = (tmpliveNumberAtCurrentN1) ? parseInt(tmpliveNumberAtCurrentN1.liveFemale) : 0;
                            let tmpliveNumberAtCurrentN2 = obj.find(item => item.age == ($i));
                            let valueTmpliveNumberAtCurrentN2 = (tmpliveNumberAtCurrentN2) ? parseInt(tmpliveNumberAtCurrentN2.liveFemale) : 0;

                            life_coeff_female = (valueTmpliveNumberAtCurrentN1 - valueTmpliveNumberAtCurrentN2) / valueTmpliveNumberAtCurrentN2;
                            installment_with = installment_with * (1 + valueCurrent_averageReturnI) * (1 + life_coeff_female) + (valueMonthlyInstall * 12) * (1 + (valueCurrent_averageReturnI / 2)) * (1 + (life_coeff_female / 2));
                        }

                        let multiplier_coeff = 0;
                        let liveNumberAtRetirementAge = obj.find(item => item.age == 65);
                        let valueLiveNumberAtRetirementAge = (liveNumberAtRetirementAge) ? parseInt(liveNumberAtRetirementAge.liveFemale) : 0;
                        let liveNumberAtPayoutAgex = obj.find(item => item.age == valueCurrent_payoutI);
                        let valueLiveNumberAtPayoutAgex = (liveNumberAtPayoutAgex) ? parseInt(liveNumberAtPayoutAgex.liveFemale) : 0;

                        multiplier_coeff = (valueLiveNumberAtRetirementAge - valueLiveNumberAtPayoutAgex) / valueLiveNumberAtPayoutAgex + 1;
                        installment_with = multiplier_coeff * installment_with * Math.pow(1 + valueCurrent_averageReturnI, (valueCurrent_payoutI - 65));
                    }

                    myMultiplier = installment_with / installment_without;

                    let mymultiplierRound = myMultiplier.toFixed(2);
                    let mywithoutRounded = Math.round(installment_without);
                    let mywithRounded = Math.round(installment_with);

                    document.getElementById('currentAgeSelected').innerHTML = valueCurrent_payoutI;
                    document.getElementById('ageFinal').innerHTML = valueCurrent_payoutI;

                    document.getElementById('withsavvlyRetire').innerHTML = parseInt(withRounded).toLocaleString('en-US');
                    document.getElementById('lumpsumFinal').innerHTML = parseInt(withRounded).toLocaleString('en-US');
                    document.getElementById('withoutsavvlyRetire').innerHTML = parseInt(withoutRounded).toLocaleString('en-US');

                    document.getElementById('withsavvlyRetire2').innerHTML = parseInt(withRounded).toLocaleString('en-US');

                    // document.getElementById('multiValue').innerHTML = mymultiplierRound + 'x';
                    crearGrafica(mywithRounded, mywithoutRounded);
                } else {

                    for ($x = currAge + 2; $x <= 65; $x++) {
                        installment_without = (installment_without * (1 + valueCurrent_averageReturnI)) + (valueCurrent_minstallmentI * 12) * (1 + (valueCurrent_averageReturnI / 2));
                    }

                    installment_without = installment_without * Math.pow(1 + valueCurrent_averageReturnI, (currPayo - retirAge));
                    final_without_multiplier = without_multiplier + installment_without;

                    if (valueCurrent_genderI == "Male") {

                        let liveNumberAtCurrentAge = obj.find(item => item.age == valueCurrent_ageI);
                        let valueLiveNumberAtCurrentAge = (liveNumberAtCurrentAge) ? parseInt(liveNumberAtCurrentAge.liveMale) : 0;
                        let liveNumberAtPayoutAge = obj.find(item => item.age == valueCurrent_payoutI);
                        let valueLiveNumberAtPayoutAge = (liveNumberAtPayoutAge) ? parseInt(liveNumberAtPayoutAge.liveMale) : 0;

                        male_multiplier = ((valueLiveNumberAtCurrentAge - valueLiveNumberAtPayoutAge) / valueLiveNumberAtPayoutAge + 1).toFixed(8);
                        withMultiplier = male_multiplier * without_multiplier;

                        let life_coeff_male = 0;

                        let liveNumberAtCurrentAgeN = obj.find(item => item.age == currAge);
                        let valueLiveNumberAtCurrentAgeN = (liveNumberAtCurrentAgeN) ? parseInt(liveNumberAtCurrentAgeN.liveMale) : 0;
                        let liveNumberAtCurrentAgeN1 = obj.find(item => item.age == (currAge + 1));
                        let valueLiveNumberAtCurrentAgeN1 = (liveNumberAtCurrentAgeN1) ? parseInt(liveNumberAtCurrentAgeN1.liveMale) : 0;

                        life_coeff_male = ((valueLiveNumberAtCurrentAgeN - valueLiveNumberAtCurrentAgeN1) / valueLiveNumberAtCurrentAgeN1);
                        installment_with = (valueMonthlyInstall * 12) * (1 + valueCurrent_averageReturnI / 2) * (1 + life_coeff_male / 2);

                        for ($i = currAge + 2; $i <= 65; $i++) {

                            let tmpliveNumberAtCurrentN1 = obj.find(item => item.age == ($i - 1));
                            let valueTmpliveNumberAtCurrentN1 = (tmpliveNumberAtCurrentN1) ? parseInt(tmpliveNumberAtCurrentN1.liveMale) : 0;
                            let tmpliveNumberAtCurrentN2 = obj.find(item => item.age == ($i));
                            let valueTmpliveNumberAtCurrentN2 = (tmpliveNumberAtCurrentN2) ? parseInt(tmpliveNumberAtCurrentN2.liveMale) : 0;

                            life_coeff_male = (valueTmpliveNumberAtCurrentN1 - valueTmpliveNumberAtCurrentN2) / valueTmpliveNumberAtCurrentN2;
                            installment_with = installment_with * (1 + valueCurrent_averageReturnI) * (1 + life_coeff_male) + (valueMonthlyInstall * 12) * (1 + (valueCurrent_averageReturnI / 2)) * (1 + (life_coeff_male / 2));
                        }

                        let multiplier_coeff = 0;
                        let final_withMultiplier = 0;
                        let liveNumberAtRetirementAge = obj.find(item => item.age == 65);
                        let valueLiveNumberAtRetirementAge = (liveNumberAtRetirementAge) ? parseInt(liveNumberAtRetirementAge.liveMale) : 0;
                        let liveNumberAtPayoutAgex = obj.find(item => item.age == valueCurrent_payoutI);
                        let valueLiveNumberAtPayoutAgex = (liveNumberAtPayoutAgex) ? parseInt(liveNumberAtPayoutAgex.liveMale) : 0;

                        multiplier_coeff = (valueLiveNumberAtRetirementAge - valueLiveNumberAtPayoutAgex) / valueLiveNumberAtPayoutAgex + 1;
                        installment_with = multiplier_coeff * installment_with * Math.pow(1 + valueCurrent_averageReturnI, (valueCurrent_payoutI - 65));
                        final_withMultiplier = withMultiplier + installment_with;
                        multiplier = final_withMultiplier / final_without_multiplier;

                        let multiplierRound = multiplier.toFixed(2);
                        let withoutRounded = Math.round(final_without_multiplier);
                        let withRounded = Math.round(final_withMultiplier);

                        document.getElementById('currentAgeSelected').innerHTML = valueCurrent_payoutI + '';
                        document.getElementById('ageFinal').innerHTML = valueCurrent_payoutI + '';

                        document.getElementById('withsavvlyRetire').innerHTML = parseInt(withRounded).toLocaleString('en-US');
                        document.getElementById('lumpsumFinal').innerHTML = parseInt(withRounded).toLocaleString('en-US');
                        document.getElementById('withoutsavvlyRetire').innerHTML = parseInt(withoutRounded).toLocaleString('en-US');

                        document.getElementById('withsavvlyRetire2').innerHTML = parseInt(withRounded).toLocaleString('en-US');

                        // document.getElementById('multiValue').innerHTML = multiplierRound + 'x';
                        crearGrafica(withRounded, withoutRounded);

                    } else if (valueCurrent_genderI == "Female") {

                        let liveNumberAtCurrentAge = obj.find(item => item.age == valueCurrent_ageI);
                        let valueLiveNumberAtCurrentAge = (liveNumberAtCurrentAge) ? parseInt(liveNumberAtCurrentAge.liveFemale) : 0;
                        let liveNumberAtPayoutAge = obj.find(item => item.age == valueCurrent_payoutI);
                        let valueLiveNumberAtPayoutAge = (liveNumberAtPayoutAge) ? parseInt(liveNumberAtPayoutAge.liveFemale) : 0;

                        female_multiplier = ((valueLiveNumberAtCurrentAge - valueLiveNumberAtPayoutAge) / valueLiveNumberAtPayoutAge + 1).toFixed(8);
                        withMultiplier = female_multiplier * without_multiplier;

                        let life_coeff_male = 0;

                        let liveNumberAtCurrentAgeN = obj.find(item => item.age == currAge);
                        let valueLiveNumberAtCurrentAgeN = (liveNumberAtCurrentAgeN) ? parseInt(liveNumberAtCurrentAgeN.liveFemale) : 0;
                        let liveNumberAtCurrentAgeN1 = obj.find(item => item.age == (currAge + 1));
                        let valueLiveNumberAtCurrentAgeN1 = (liveNumberAtCurrentAgeN1) ? parseInt(liveNumberAtCurrentAgeN1.liveFemale) : 0;

                        life_coeff_female = ((valueLiveNumberAtCurrentAgeN - valueLiveNumberAtCurrentAgeN1) / valueLiveNumberAtCurrentAgeN1);
                        installment_with = (valueMonthlyInstall * 12) * (1 + valueCurrent_averageReturnI / 2) * (1 + life_coeff_female / 2);

                        for ($i = currAge + 2; $i <= 65; $i++) {

                            let tmpliveNumberAtCurrentN1 = obj.find(item => item.age == ($i - 1));
                            let valueTmpliveNumberAtCurrentN1 = (tmpliveNumberAtCurrentN1) ? parseInt(tmpliveNumberAtCurrentN1.liveFemale) : 0;
                            let tmpliveNumberAtCurrentN2 = obj.find(item => item.age == ($i));
                            let valueTmpliveNumberAtCurrentN2 = (tmpliveNumberAtCurrentN2) ? parseInt(tmpliveNumberAtCurrentN2.liveFemale) : 0;

                            life_coeff_female = (valueTmpliveNumberAtCurrentN1 - valueTmpliveNumberAtCurrentN2) / valueTmpliveNumberAtCurrentN2;
                            installment_with = installment_with * (1 + valueCurrent_averageReturnI) * (1 + life_coeff_female) + (valueMonthlyInstall * 12) * (1 + (valueCurrent_averageReturnI / 2)) * (1 + (life_coeff_female / 2));
                        }

                        let multiplier_coeff = 0;
                        let final_withMultiplier = 0;
                        let liveNumberAtRetirementAge = obj.find(item => item.age == 65);
                        let valueLiveNumberAtRetirementAge = (liveNumberAtRetirementAge) ? parseInt(liveNumberAtRetirementAge.liveFemale) : 0;
                        let liveNumberAtPayoutAgex = obj.find(item => item.age == valueCurrent_payoutI);
                        let valueLiveNumberAtPayoutAgex = (liveNumberAtPayoutAgex) ? parseInt(liveNumberAtPayoutAgex.liveFemale) : 0;

                        multiplier_coeff = (valueLiveNumberAtRetirementAge - valueLiveNumberAtPayoutAgex) / valueLiveNumberAtPayoutAgex + 1;
                        installment_with = multiplier_coeff * installment_with * Math.pow(1 + valueCurrent_averageReturnI, (valueCurrent_payoutI - 65));
                        final_withMultiplier = withMultiplier + installment_with;
                        multiplier = final_withMultiplier / final_without_multiplier;

                        let multiplierRound = multiplier.toFixed(2);
                        let withoutRounded = Math.round(final_without_multiplier);
                        let withRounded = Math.round(final_withMultiplier);

                        document.getElementById('currentAgeSelected').innerHTML = valueCurrent_payoutI + '';
                        document.getElementById('ageFinal').innerHTML = valueCurrent_payoutI + '';

                        document.getElementById('withsavvlyRetire').innerHTML = parseInt(withRounded).toLocaleString('en-US');
                        document.getElementById('lumsumFinal').innerHTML = parseInt(withRounded).toLocaleString('en-US');
                        document.getElementById('withoutsavvlyRetire').innerHTML = parseInt(withoutRounded).toLocaleString('en-US');

                        document.getElementById('withsavvlyRetire2').innerHTML = parseInt(withRounded).toLocaleString('en-US');

                        // document.getElementById('multiValue').innerHTML = multiplierRound + 'x';
                        crearGrafica(withRounded, withoutRounded);
                    }

                }
            }
        }
    };

    xhttp.open("GET", "livenumbers.json", true);
    xhttp.send();
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


current_ageI.oninput = function() {
    valueCurrent_ageI = current_ageI.value;
    document.getElementById('demoAge').innerHTML = valueCurrent_ageI;
    sessionStorage.setItem('Value_current_age_selected$', valueCurrent_ageI);
    var value = (this.value - this.min) / (this.max - this.min) * 100;
    this.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79  ' + value + '%, #fff ' + value + '%, white 100%)';

    compareAge();

}
current_ageI.addEventListener("change", cargar);

current_averageReturnI.oninput = function() {
    valueCurrent_averageReturnI = current_averageReturnI.value / 100;
}
current_averageReturnI.addEventListener("change", cargar);

current_genderI.oninput = function() {
    valueCurrent_genderI = current_genderI.value;
}
current_genderI.addEventListener("change", cargar);

// current_fundingamountI.oninput = function() {
//     valueCurrent_fundingamountI = parseInt(current_fundingamountI.value);
//     document.getElementById('demo').innerHTML = parseInt(valueCurrent_fundingamountI).toLocaleString('en-US');

//     var value = (this.value - this.min) / (this.max - this.min) * 100;
//     this.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79  ' + value + '%, #fff ' + value + '%, white 100%)';
// }
// current_fundingamountI.addEventListener("change", cargar);

current_fundingamountI.oninput = function() {
    valueCurrent_fundingamountI = parseInt(current_fundingamountI.value);
    newPercent = parseInt(sessionStorage.getItem('Value_current_saved_selected$')) * valueCurrent_fundingamountI / 100;
    document.getElementById('demo').innerHTML = valueCurrent_fundingamountI + "% ( $" + parseInt(newPercent).toLocaleString('en-US') + ")";
    document.getElementById('labelPercent').innerHTML = valueCurrent_fundingamountI;
    // document.getElementById('demo').innerHTML = parseInt(valueCurrent_fundingamountI).toLocaleString('en-US');
    sessionStorage.setItem("valueCurrent_fundingamountI$", valueCurrent_fundingamountI);

    var value = (this.value - this.min) / (this.max - this.min) * 100;
    this.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79  ' + value + '%, #fff ' + value + '%, white 100%)';
}
current_fundingamountI.addEventListener("change", cargar);

current_payoutI.oninput = function() {
    valueCurrent_payoutI = parseInt(current_payoutI.value);
    document.getElementById('demo2').innerHTML = valueCurrent_payoutI;

    var value = (this.value - this.min) / (this.max - this.min) * 100;
    this.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79  ' + value + '%, #fff ' + value + '%, white 100%)';
}
current_payoutI.addEventListener("change", cargar);

current_minstallmentI.oninput = function() {
    valueCurrent_minstallmentI = parseInt(current_minstallmentI.value);
    document.getElementById('demo3').innerHTML = valueCurrent_minstallmentI;

    var value = (this.value - this.min) / (this.max - this.min) * 100;
    this.style.background = 'linear-gradient(to right, #0b6e79  0%, #0b6e79  ' + value + '%, #fff ' + value + '%, white 100%)';
}
current_minstallmentI.addEventListener("change", cargar);


current_retirementAgeI.oninput = function() {
    valueCurrent_retirementAgeI = parseInt(current_retirementAgeI.value);
}
current_retirementAgeI.addEventListener("change", cargar);


function crearGrafica(valor1, valor2) {
    if (myChart !== null) {
        myChart.destroy();
    }
    myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['With Savvly', 'Without Savvly'],
            datasets: [{
                label: '',
                data: [valor1, valor2],
                minBarLength: 10,
                barThickness: 100,
                backgroundColor: [
                    '#fed67e',
                    '#0b6e79 '

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