document.addEventListener(

    "DOMContentLoaded",

    () => {

        animateCounters();

        animateCards();

        showWelcomeMessage();

    }

);


function animateCounters(){

    const counters =

    document.querySelectorAll(

        ".counter"

    );

    counters.forEach(

        counter => {

            const target =

            Number(

                counter.getAttribute(

                    "data-target"

                )

            );

            let count = 0;

            const speed =

            target / 50;

            const updateCounter = () => {

                if(

                    count < target

                ){

                    count += speed;

                    counter.innerText =

                    Math.ceil(
                        count
                    );

                    requestAnimationFrame(

                        updateCounter

                    );

                }

                else{

                    counter.innerText =
                    target;
                }

            };

            updateCounter();

        }

    );

}


function animateCards(){

    const cards =

    document.querySelectorAll(

        ".stat-card,.action-card,.info-card"

    );

    cards.forEach(

        (
            card,
            index
        ) => {

            card.style.opacity = "0";

            card.style.transform =
            "translateY(40px)";

            setTimeout(

                () => {

                    card.style.transition =
                    "all 0.6s ease";

                    card.style.opacity = "1";

                    card.style.transform =
                    "translateY(0px)";

                },

                index * 150

            );

        }

    );

}


function showWelcomeMessage(){

    const banner =

    document.querySelector(

        ".welcome-section"
    );

    if(!banner){

        return;
    }

    banner.style.opacity = "0";

    banner.style.transform =
    "translateX(-50px)";

    setTimeout(

        () => {

            banner.style.transition =
            "all 0.8s ease";

            banner.style.opacity =
            "1";

            banner.style.transform =
            "translateX(0px)";

        },

        300

    );

}


/* ========================= */
/* Risk Progress Animation */
/* ========================= */

function animateRiskBar(

    elementId,

    percentage

){

    const bar =

    document.getElementById(
        elementId
    );

    if(!bar){

        return;
    }

    let width = 0;

    const interval = setInterval(

        () => {

            if(

                width >= percentage

            ){

                clearInterval(
                    interval
                );
            }

            else{

                width++;

                bar.style.width =
                width + "%";
            }

        },

        10

    );

}


/* ========================= */
/* Dashboard Notification */
/* ========================= */

function showNotification(

    message

){

    const notification =

    document.createElement(
        "div"
    );

    notification.className =
    "dashboard-notification";

    notification.innerText =
    message;

    document.body.appendChild(
        notification
    );

    setTimeout(

        () => {

            notification.classList.add(
                "show"
            );

        },

        100

    );

    setTimeout(

        () => {

            notification.remove();

        },

        4000

    );

}