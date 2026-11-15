document.addEventListener(

    "DOMContentLoaded",

    () => {

        animateProfileCards();

    }

);

function animateProfileCards(){

    const cards =

    document.querySelectorAll(

        ".profile-card,.stat-box,.detail-card"

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

                index * 120

            );

        }

    );

}