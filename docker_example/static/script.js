const form =
    document.getElementById("predictionForm");

const button =
    document.getElementById("predictBtn");

const buttonText =
    document.getElementById("btnText");

const placeholder =
    document.getElementById("placeholder");

const resultValue =
    document.getElementById("resultValue");

const price =
    document.getElementById("price");

const errorBox =
    document.getElementById("errorBox");


form.addEventListener("submit", async (event) => {

    event.preventDefault();

    button.disabled = true;

    buttonText.textContent =
        "Analyzing property...";

    placeholder.classList.add("hidden");

    resultValue.classList.add("hidden");

    errorBox.classList.add("hidden");


    const formData =
        new FormData(form);

    const data =
        Object.fromEntries(
            formData.entries()
        );


    try {

        const response =
            await fetch("/predict", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify(data)
            });


        const result =
            await response.json();


        if (!response.ok ||
            !result.success) {

            throw new Error(
                result.error ||
                "Prediction failed."
            );
        }


        const value =
            Number(result.prediction);


        price.textContent =
            value.toLocaleString(
                "en-US",
                {
                    style: "currency",
                    currency: "USD",
                    maximumFractionDigits: 0
                }
            );


        resultValue.classList.remove(
            "hidden"
        );


    } catch (error) {

        errorBox.textContent =
            "⚠ " + error.message;

        errorBox.classList.remove(
            "hidden"
        );

    } finally {

        button.disabled = false;

        buttonText.textContent =
            "Generate Prediction";
    }

});