document.addEventListener(

    "DOMContentLoaded",

    () => {

        initializeAssessment();

    }

);


/* ========================= */
/* Main */
/* ========================= */

function initializeAssessment(){

    setupFormValidation();

    setupPredictionLoading();

    animateResultCards();

    animateFeatureTable();

}


/* ========================= */
/* Validation */
/* ========================= */

function setupFormValidation(){

    const form =

    document.getElementById(
        "assessmentForm"
    );

    if(!form){

        return;
    }

    form.addEventListener(

        "submit",

        function(e){

            const validations = [

                validateRange(
                    "age",
                    40,
                    100
                ),

                validateRange(
                    "mmse",
                    0,
                    30
                ),

                validateRange(
                    "bmi",
                    10,
                    60
                ),

                validateRange(
                    "adl",
                    0,
                    10
                ),

                validateRange(
                    "sleepquality",
                    0,
                    10
                ),

                validateRange(
                    "functionalassessment",
                    0,
                    10
                )

            ];

            const isValid =

            validations.every(
                v => v
            );

            if(!isValid){

                e.preventDefault();

                alert(

                    "Please correct invalid values."

                );

            }

        }

    );

}


function validateRange(

    fieldName,

    min,

    max

){

    const input =

    document.querySelector(

        `[name="${fieldName}"]`

    );

    if(!input){

        return true;
    }

    const value =

    parseFloat(
        input.value
    );

    removeError(
        input
    );

    if(

        isNaN(value)

    ){

        showError(

            input,

            "Value required"

        );

        return false;
    }

    if(

        value < min ||

        value > max

    ){

        showError(

            input,

            `Scale exceeded (${min}-${max})`

        );

        input.style.border =
        "2px solid red";

        return false;
    }

    input.style.border =
    "2px solid #10b981";

    return true;

}


function showError(

    input,

    message

){

    const error =

    document.createElement(
        "small"
    );

    error.className =
    "error-message";

    error.innerText =
    message;

    input.parentNode.appendChild(
        error
    );

}


function removeError(

    input

){

    const error =

    input.parentNode.querySelector(

        ".error-message"

    );

    if(error){

        error.remove();
    }

}


/* ========================= */
/* Loading Animation */
/* ========================= */

function setupPredictionLoading(){

    const form =

    document.getElementById(
        "assessmentForm"
    );

    if(!form){

        return;
    }

    form.addEventListener(

        "submit",

        () => {

            showLoading();

        }

    );

}


function showLoading(){

    const overlay =

    document.createElement(
        "div"
    );

    overlay.id =
    "loadingOverlay";

    overlay.innerHTML =

    `

    <div class="loading-box">

        <div class="spinner"></div>

        <h3>

            Running AI Analysis

        </h3>

        <p>

            Please wait...

        </p>

    </div>

    `;

    document.body.appendChild(
        overlay
    );

}


/* ========================= */
/* Result Cards */
/* ========================= */

function animateResultCards(){

    const cards =

    document.querySelectorAll(

        ".result-card"

    );

    cards.forEach(

        (
            card,
            index
        ) => {

            card.style.opacity =
            "0";

            card.style.transform =
            "translateY(40px)";

            setTimeout(

                () => {

                    card.style.transition =
                    "all 0.6s ease";

                    card.style.opacity =
                    "1";

                    card.style.transform =
                    "translateY(0px)";

                },

                index * 150

            );

        }

    );

}


/* ========================= */
/* Feature Table */
/* ========================= */

function animateFeatureTable(){

    const rows =

    document.querySelectorAll(

        ".feature-table tbody tr"

    );

    rows.forEach(

        (
            row,
            index
        ) => {

            row.style.opacity =
            "0";

            row.style.transform =
            "translateX(-40px)";

            setTimeout(

                () => {

                    row.style.transition =
                    "all 0.5s ease";

                    row.style.opacity =
                    "1";

                    row.style.transform =
                    "translateX(0px)";

                },

                index * 100

            );

        }

    );

}


/* ========================= */
/* Confidence Animation */
/* ========================= */

function animateConfidenceScore(

    elementId,

    target

){

    const element =

    document.getElementById(
        elementId
    );

    if(!element){

        return;
    }

    let value = 0;

    const interval =

    setInterval(

        () => {

            if(

                value >= target

            ){

                clearInterval(
                    interval
                );
            }

            else{

                value++;

                element.innerText =

                value + "%";

            }

        },

        20

    );

}


/* ========================= */
/* Scroll To Result */
/* ========================= */

function scrollToResult(){

    const section =

    document.querySelector(

        ".result-section"

    );

    if(section){

        section.scrollIntoView(

            {

                behavior:
                "smooth"

            }

        );

    }

}