const task =
    document.getElementById("task");

const dynamicFields =
    document.getElementById("dynamicFields");

const submitBtn =
    document.getElementById("submitBtn");

const result =
    document.getElementById("result");

const statusBadge =
    document.getElementById("statusBadge");

const copyBtn =
    document.getElementById("copyBtn");


// ======================================================
// CREATE FORM FIELD
// ======================================================

function field(
    label,
    id,
    type = "textarea",
    placeholder = ""
) {

    const wrapper =
        document.createElement("div");

    wrapper.className = "field";


    const labelElement =
        document.createElement("label");

    labelElement.htmlFor = id;

    labelElement.textContent = label;


    const input =
        document.createElement(
            type === "textarea"
                ? "textarea"
                : "input"
        );


    input.id = id;

    input.placeholder = placeholder;


    wrapper.append(
        labelElement,
        input
    );


    return wrapper;
}


// ======================================================
// CREATE SELECT FIELD
// ======================================================

function selectField(
    label,
    id,
    options
) {

    const wrapper =
        document.createElement("div");

    wrapper.className = "field";


    const labelElement =
        document.createElement("label");

    labelElement.htmlFor = id;

    labelElement.textContent = label;


    const select =
        document.createElement("select");

    select.id = id;


    options.forEach(
        ([value, text]) => {

            const option =
                document.createElement(
                    "option"
                );

            option.value = value;

            option.textContent = text;

            select.appendChild(
                option
            );
        }
    );


    wrapper.append(
        labelElement,
        select
    );


    return wrapper;
}


// ======================================================
// RENDER TASK FIELDS
// ======================================================

function renderFields() {

    dynamicFields.innerHTML = "";


    // --------------------------------------------------
    // Q&A
    // --------------------------------------------------

    if (task.value === "qa") {

        dynamicFields.append(

            field(
                "Question",
                "inputText",
                "textarea",
                "e.g. Why is the sky blue?"
            ),

            field(
                "Optional context",
                "context",
                "textarea",
                "Paste notes or context if useful."
            )

        );

    }


    // --------------------------------------------------
    // EXPLANATION
    // --------------------------------------------------

    if (task.value === "explain") {

        dynamicFields.append(

            field(
                "Topic",
                "inputText",
                "textarea",
                "e.g. Pythagoras theorem"
            ),

            selectField(
                "Learner level",
                "level",
                [
                    [
                        "beginner",
                        "Beginner"
                    ],
                    [
                        "intermediate",
                        "Intermediate"
                    ],
                    [
                        "advanced",
                        "Advanced"
                    ]
                ]
            )

        );

    }


    // --------------------------------------------------
    // QUIZ
    // --------------------------------------------------

    if (task.value === "quiz") {

        dynamicFields.append(

            field(
                "Educational text",
                "inputText",
                "textarea",
                "Paste a passage or study notes..."
            ),

            selectField(
                "Difficulty",
                "level",
                [
                    [
                        "beginner",
                        "Beginner"
                    ],
                    [
                        "mixed",
                        "Mixed"
                    ],
                    [
                        "intermediate",
                        "Intermediate"
                    ]
                ]
            )

        );

    }


    // --------------------------------------------------
    // SUMMARY
    // --------------------------------------------------

    if (task.value === "summarize") {

        dynamicFields.append(

            field(
                "Text to summarize",
                "inputText",
                "textarea",
                "Paste the passage here..."
            ),

            selectField(
                "Summary length",
                "length",
                [
                    [
                        "short",
                        "Short"
                    ],
                    [
                        "medium",
                        "Medium"
                    ],
                    [
                        "long",
                        "Long"
                    ]
                ]
            )

        );

    }


    // --------------------------------------------------
    // LEARNING PATH
    // --------------------------------------------------

    if (task.value === "learn") {

        dynamicFields.append(

            field(
                "Topic",
                "inputText",
                "textarea",
                "e.g. SQL"
            ),

            selectField(
                "Current level",
                "level",
                [
                    [
                        "beginner",
                        "Beginner"
                    ],
                    [
                        "intermediate",
                        "Intermediate"
                    ],
                    [
                        "advanced",
                        "Advanced"
                    ]
                ]
            ),

            field(
                "Weeks",
                "weeks",
                "number",
                "6"
            )

        );


        const weeks =
            document.getElementById(
                "weeks"
            );


        weeks.value = 6;

        weeks.min = 1;

        weeks.max = 52;

    }

}


// ======================================================
// DISPLAY RESULT
// ======================================================

function renderResult(data) {


    // --------------------------------------------------
    // QUIZ
    // --------------------------------------------------

    if (
        task.value === "quiz"
        &&
        Array.isArray(data.questions)
    ) {

        result.innerHTML = "";


        data.questions.forEach(
            (question, index) => {

                const box =
                    document.createElement(
                        "div"
                    );

                box.className =
                    "quiz-question";


                const title =
                    document.createElement(
                        "h3"
                    );

                title.textContent =
                    `${index + 1}. ${question.question}`;


                box.appendChild(title);


                question.options.forEach(
                    option => {

                        const optionElement =
                            document.createElement(
                                "div"
                            );

                        optionElement.className =
                            "quiz-option";

                        optionElement.textContent =
                            `• ${option}`;

                        box.appendChild(
                            optionElement
                        );

                    }
                );


                const answer =
                    document.createElement(
                        "p"
                    );

                answer.className =
                    "muted";


                answer.textContent =
                    `Answer: ${question.correct_answer}` +
                    (
                        question.explanation
                            ? ` — ${question.explanation}`
                            : ""
                    );


                box.appendChild(
                    answer
                );


                result.appendChild(
                    box
                );

            }
        );


        return;
    }


    // --------------------------------------------------
    // NORMAL RESPONSE
    // --------------------------------------------------

    const text =
        data.answer
        ??
        data.explanation
        ??
        data.summary
        ??
        data.recommendations;


    result.textContent =
        text ||
        "No result returned.";

}


// ======================================================
// ERROR DISPLAY
// ======================================================

function showError(message) {

    result.innerHTML = "";


    const box =
        document.createElement(
            "div"
        );


    box.className =
        "error";


    box.textContent =
        message;


    result.appendChild(
        box
    );


    statusBadge.textContent =
        "Error";
}


// ======================================================
// LOADING STATE
// ======================================================

function setBusy(busy) {

    submitBtn.disabled =
        busy;


    submitBtn.textContent =
        busy
            ? "Generating..."
            : "Generate";


    if (busy) {

        statusBadge.textContent =
            "Working...";

    }

}


// ======================================================
// SUBMIT REQUEST
// ======================================================

async function submit() {

    const selected =
        task.value;


    const inputTextElement =
        document.getElementById(
            "inputText"
        );


    const inputText =
        inputTextElement
            ?.value
            .trim();


    let endpoint;

    let payload;


    // --------------------------------------------------
    // Q&A
    // --------------------------------------------------

    if (selected === "qa") {

        if (!inputText) {

            showError(
                "Please enter a question."
            );

            return;
        }


        endpoint = "/qa";


        payload = {

            question:
                inputText,

            context:
                document
                    .getElementById(
                        "context"
                    )
                    ?.value
                    .trim()
                    ||
                    null

        };

    }


    // --------------------------------------------------
    // EXPLAIN
    // --------------------------------------------------

    if (selected === "explain") {

        if (!inputText) {

            showError(
                "Please enter a topic."
            );

            return;
        }


        endpoint =
            "/explain";


        payload = {

            topic:
                inputText,

            level:
                document
                    .getElementById(
                        "level"
                    )
                    .value

        };

    }


    // --------------------------------------------------
    // QUIZ
    // --------------------------------------------------

    if (selected === "quiz") {

        if (!inputText) {

            showError(
                "Please paste some educational text."
            );

            return;
        }


        endpoint =
            "/quiz";


        payload = {

            text:
                inputText,

            level:
                document
                    .getElementById(
                        "level"
                    )
                    .value

        };

    }


    // --------------------------------------------------
    // SUMMARY
    // --------------------------------------------------

    if (selected === "summarize") {

        if (!inputText) {

            showError(
                "Please enter text to summarize."
            );

            return;
        }


        endpoint =
            "/summarize";


        payload = {

            text:
                inputText,

            length:
                document
                    .getElementById(
                        "length"
                    )
                    .value

        };

    }


    // --------------------------------------------------
    // LEARNING PATH
    // --------------------------------------------------

    if (selected === "learn") {

        if (!inputText) {

            showError(
                "Please enter a topic."
            );

            return;
        }


        endpoint =
            "/learn/recommendations";


        payload = {

            topic:
                inputText,

            level:
                document
                    .getElementById(
                        "level"
                    )
                    .value,

            weeks:
                Number(
                    document
                        .getElementById(
                            "weeks"
                        )
                        .value
                )

        };

    }


    setBusy(true);


    try {

        const response =
            await fetch(
                endpoint,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            payload
                        )
                }
            );


        const contentType =
            response.headers.get("content-type") || "";

        const data =
            contentType.includes("application/json")
                ? await response.json()
                : {
                    detail: await response.text()
                };


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Request failed."
            );

        }


        renderResult(data);


        statusBadge.textContent =
            "Completed";

    }

    catch (error) {

        showError(
            error.message
        );

    }

    finally {

        setBusy(false);

    }

}


// ======================================================
// COPY RESULT
// ======================================================

copyBtn.addEventListener(
    "click",
    async () => {

        try {

            await navigator.clipboard.writeText(
                result.innerText
            );


            statusBadge.textContent =
                "Copied";

        }

        catch {

            statusBadge.textContent =
                "Copy failed";

        }

    }
);


// ======================================================
// EVENT LISTENERS
// ======================================================

task.addEventListener(
    "change",
    renderFields
);


submitBtn.addEventListener(
    "click",
    submit
);


// Initial UI

renderFields();