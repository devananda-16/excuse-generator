let selectedStyle = "funny";

const activityInput = document.getElementById("activity");
const generateBtn = document.getElementById("generateBtn");
const result = document.getElementById("result");
const excuseText = document.getElementById("excuseText");

const styleButtons = document.querySelectorAll(".style-btn");


// -----------------------------
// SELECT EXCUSE PERSONALITY
// -----------------------------

styleButtons.forEach(function (button) {

    button.addEventListener("click", function () {

        // Remove active from all buttons
        styleButtons.forEach(function (btn) {
            btn.classList.remove("active");
        });

        // Add active to clicked button
        button.classList.add("active");

        // Store selected personality
        selectedStyle = button.dataset.style;

        console.log("Selected style:", selectedStyle);
    });

});


// -----------------------------
// GENERATE EXCUSE
// -----------------------------

async function generateExcuse(style = selectedStyle) {

    const activity = activityInput.value.trim();

    if (activity === "") {
        alert("Brooo 😭 tell me what you're doing first!");
        activityInput.focus();
        return;
    }

    generateBtn.innerText = "GENERATING USELESSNESS... 💀";
    generateBtn.disabled = true;

    try {

        const response = await fetch("/generate", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                activity: activity,
                style: style
            })

        });

        const data = await response.json();

        console.log("Server response:", data);


        if (data.success) {

            excuseText.innerText = `"${data.excuse}"`;

            document.getElementById("believability").innerText =
                data.believability + "%";

            document.getElementById("ridiculousness").innerText =
                data.ridiculousness + "%";

            document.getElementById("caught").innerText =
                data.caught + "%";

            result.classList.remove("hidden");

        } else {

            excuseText.innerText = data.message;
            result.classList.remove("hidden");

        }

    } catch (error) {

        console.error("ERROR:", error);

        excuseText.innerText =
            "Oops. Even EXCUSE.exe needs an excuse right now. 💀";

        result.classList.remove("hidden");
    }

    generateBtn.innerText = "GENERATE MY EXCUSE 🎲";
    generateBtn.disabled = false;
}


// -----------------------------
// GENERATE BUTTON
// -----------------------------

generateBtn.addEventListener("click", function () {

    generateExcuse();

});


// -----------------------------
// GENERATE AGAIN
// -----------------------------

document.getElementById("againBtn").addEventListener("click", function () {

    generateExcuse();

});


// -----------------------------
// MAKE IT WORSE
// -----------------------------

document.getElementById("worseBtn").addEventListener("click", function () {

    selectedStyle = "ridiculous";

    styleButtons.forEach(function (btn) {
        btn.classList.remove("active");
    });

    document
        .querySelector('[data-style="ridiculous"]')
        .classList.add("active");

    generateExcuse("ridiculous");

});


// -----------------------------
// COPY EXCUSE
// -----------------------------

document.getElementById("copyBtn").addEventListener("click", async function () {

    const text = excuseText.innerText;

    try {

        await navigator.clipboard.writeText(text);

        this.innerText = "✅ Copied!";

        setTimeout(() => {
            this.innerText = "📋 Copy";
        }, 1500);

    } catch (error) {

        alert("Couldn't copy 😭");

    }

});


// -----------------------------
// PRESS ENTER TO GENERATE
// -----------------------------

activityInput.addEventListener("keydown", function (event) {

    if (event.key === "Enter") {
        generateExcuse();
    }

});