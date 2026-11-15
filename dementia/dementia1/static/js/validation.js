document.addEventListener(

    "DOMContentLoaded",

    () => {

        const form = document.querySelector(
            "#assessmentForm"
        );

        if(!form){

            return;
        }

        const rules = {

            age: {

                min:40,

                max:100
            },

            mmse: {

                min:0,

                max:30
            },

            bmi: {

                min:10,

                max:60
            },

            adl: {

                min:0,

                max:10
            },

            sleepquality: {

                min:0,

                max:10
            },

            functionalassessment: {

                min:0,

                max:10
            }

        };

        Object.keys(
            rules
        ).forEach(

            field => {

                const input =
                document.querySelector(

                    `[name="${field}"]`

                );

                if(!input){

                    return;
                }

                input.addEventListener(

                    "input",

                    () => {

                        validateField(

                            input,

                            rules[field]

                        );

                    }

                );

            }

        );

        form.addEventListener(

            "submit",

            e => {

                let valid = true;

                Object.keys(
                    rules
                ).forEach(

                    field => {

                        const input =
                        document.querySelector(

                            `[name="${field}"]`

                        );

                        if(

                            !validateField(

                                input,

                                rules[field]

                            )

                        ){

                            valid = false;
                        }

                    }

                );

                if(!valid){

                    e.preventDefault();

                    alert(

                        "Please correct invalid values before submission."

                    );
                }

            }

        );

    }

);


function validateField(

    input,

    rule

){

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

        value < rule.min ||

        value > rule.max

    ){

        showError(

            input,

            `Scale exceeded. Allowed range ${rule.min} - ${rule.max}`

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