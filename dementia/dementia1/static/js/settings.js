document.addEventListener(

    "DOMContentLoaded",

    () => {

        initializeSettings();

    }

);

function initializeSettings(){

    const saveBtn =

    document.querySelector(
        ".save-btn"
    );

    if(saveBtn){

        saveBtn.addEventListener(

            "click",

            () => {

                alert(

                    "Settings Saved Successfully"

                );

            }

        );

    }

}