const slider = document.getElementById("stress");
const output = document.getElementById("stressValue");
output.innerHTML = slider.value;

let breathInterval;  // Store reference to interval

function startBreathingAnimation() {
    let breathText = document.getElementById("breathText");
    let states = ["Inhale", "Hold", "Exhale", "Hold"];
    let index = 0;

    breathInterval = setInterval(() => {
        if (breathText) {
            breathText.innerText = states[index];
            index = (index + 1) % states.length;
        }
    }, 4000);
}



slider.oninput = function () {
    output.innerHTML = this.value;
}

function startSession() {
    const feedback = document.getElementById("feedback").value;

    fetch("http://127.0.0.1:5000/get_tip", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            stress: slider.value,
            feedback: feedback
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("responseBox").innerHTML = `<p>${data.tip}</p>`;

        // Showing animation only for breathing category
        const breathingSection = document.querySelector(".breathing-container");

        if (data.category === "Breathing Exercise") {
            breathingSection.style.display = "block";
            startBreathingAnimation(); //Start animation only now
        } else {
            breathingSection.style.display = "none";
        }
    });
}

function endSession() {
    const stress = slider.value;
    const feedback = document.getElementById("feedback").value;

    fetch("http://127.0.0.1:5000/end_session", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            stress: stress,
            feedback: feedback
        })
    })
    .then(response => response.json())
    .then(data => {
        clearInterval(breathInterval); //Stop animation
        // Replacing entire page content with final thank-you message
        document.body.innerHTML = `
            <div style="text-align: center; margin-top: 100px;">
                <h2>Thanks for your feedback!</h2>
                <p style="font-size: 20px;">Take care and come back any time 💙</p>
            </div>
        `;
    });
}

