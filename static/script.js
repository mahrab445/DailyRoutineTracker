const checkboxes = document.querySelectorAll(".taskCheck");
const progressBar = document.getElementById("progressBar");
const progressText = document.getElementById("progressText");
const dateInput = document.getElementById("routineDate");
const todayDate = document.getElementById("todayDate");

// Live Date
function updateDate() {

    const d = new Date(dateInput.value);

    const options = {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric"
    };

    todayDate.innerHTML = d.toLocaleDateString("en-US", options);

}

updateDate();


// Progress
function updateProgress() {

    let checked = 0;

    checkboxes.forEach(box => {

        if (box.checked)
            checked++;

    });

    let percent = Math.round((checked / checkboxes.length) * 100);

    progressBar.style.width = percent + "%";
    progressText.innerHTML = percent + "%";

}

updateProgress();


// Save Task
checkboxes.forEach(box => {

    box.addEventListener("change", () => {

        updateProgress();

        fetch("/save", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                task_id: parseInt(box.dataset.id),

                status: box.checked,

                date: dateInput.value

            })

        })

        .then(res => res.json())

        .then(data => {

            showToast("✔ Saved Successfully");

        })

        .catch(() => {

            showToast("❌ Save Failed");

        });

    });

});


// Change Date
dateInput.addEventListener("change", () => {

    updateDate();

    window.location.href = "/?date=" + dateInput.value;

});


// Toast
function showToast(message) {

    let toast = document.createElement("div");

    toast.className = "toast-box";

    toast.innerHTML = message;

    document.body.appendChild(toast);

    setTimeout(() => {

        toast.classList.add("show");

    }, 50);

    setTimeout(() => {

        toast.classList.remove("show");

    }, 2500);

    setTimeout(() => {

        toast.remove();

    }, 3000);

}


function updateClock(){

    let now = new Date();

    let time = now.toLocaleTimeString("en-US", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
    });

    document.getElementById("liveTime").innerHTML =
     "🕒 " + time;

}

setInterval(updateClock,1000);

updateClock();
