document.addEventListener(

    "DOMContentLoaded",

    () => {

        loadChartData();

        animateSummaryCards();

        animateComparisonTable();

        animateTrendCards();

    }

);


/* ========================= */
/* Load Chart Data */
/* ========================= */

function loadChartData(){

    const chartData =

    document.getElementById(
        "chartData"
    );

    if(!chartData){

        return;
    }

    const previousRisk =

    parseFloat(

        chartData.dataset
        .previousRisk

    );

    const currentRisk =

    parseFloat(

        chartData.dataset
        .currentRisk

    );

    const previousConfidence =

    parseFloat(

        chartData.dataset
        .previousConfidence

    );

    const currentConfidence =

    parseFloat(

        chartData.dataset
        .currentConfidence

    );

    createRiskChart(

        previousRisk,

        currentRisk

    );

    createConfidenceChart(

        previousConfidence,

        currentConfidence

    );

}


/* ========================= */
/* Risk Chart */
/* ========================= */

function createRiskChart(

    previousRisk,

    currentRisk

){

    const canvas =

    document.getElementById(
        "riskChart"
    );

    if(!canvas){

        return;
    }

    new Chart(

        canvas,

        {

            type:"line",

            data:{

                labels:[

                    "Previous",

                    "Current"

                ],

                datasets:[{

                    label:
                    "Risk Score",

                    data:[

                        previousRisk,

                        currentRisk

                    ],

                    borderWidth:4,

                    tension:0.4,

                    fill:false

                }]

            },

            options:{

                responsive:true,

                maintainAspectRatio:false,

                plugins:{

                    legend:{

                        display:true
                    }

                },

                scales:{

                    y:{

                        beginAtZero:true,

                        max:1

                    }

                }

            }

        }

    );

}


/* ========================= */
/* Confidence Chart */
/* ========================= */

function createConfidenceChart(

    previousConfidence,

    currentConfidence

){

    const canvas =

    document.getElementById(
        "confidenceChart"
    );

    if(!canvas){

        return;
    }

    new Chart(

        canvas,

        {

            type:"bar",

            data:{

                labels:[

                    "Previous",

                    "Current"

                ],

                datasets:[{

                    label:
                    "Confidence %",

                    data:[

                        previousConfidence,

                        currentConfidence

                    ]

                }]

            },

            options:{

                responsive:true,

                maintainAspectRatio:false,

                scales:{

                    y:{

                        beginAtZero:true,

                        max:100

                    }

                }

            }

        }

    );

}


/* ========================= */
/* Summary Cards Animation */
/* ========================= */

function animateSummaryCards(){

    const cards =

    document.querySelectorAll(

        ".summary-card,.analytics-card"

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
/* Table Animation */
/* ========================= */

function animateComparisonTable(){

    const rows =

    document.querySelectorAll(

        ".comparison-table tbody tr"

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

                index * 80

            );

        }

    );

}


/* ========================= */
/* Trend Cards Animation */
/* ========================= */

function animateTrendCards(){

    const cards =

    document.querySelectorAll(

        ".trend-card,.ai-card,.chart-card"

    );

    cards.forEach(

        (
            card,
            index
        ) => {

            card.style.opacity =
            "0";

            card.style.transform =
            "translateY(50px)";

            setTimeout(

                () => {

                    card.style.transition =
                    "all 0.8s ease";

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
/* Risk Change Badge */
/* ========================= */

function calculateRiskChange(

    previousRisk,

    currentRisk

){

    const difference =

    currentRisk -
    previousRisk;

    if(

        difference > 0

    ){

        return "Risk Increased";

    }

    if(

        difference < 0

    ){

        return "Risk Reduced";

    }

    return "No Change";

}


/* ========================= */
/* Scroll Animation */
/* ========================= */

window.addEventListener(

    "scroll",

    () => {

        const elements =

        document.querySelectorAll(

            ".chart-card,.trend-card,.ai-card"

        );

        elements.forEach(

            element => {

                const position =

                element
                .getBoundingClientRect()
                .top;

                if(

                    position <

                    window.innerHeight - 100

                ){

                    element.classList.add(
                        "visible"
                    );
                }

            }

        );

    }

);