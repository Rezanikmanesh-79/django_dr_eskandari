// ===========================================================
//  user-actions.js — نسخه نهایی
//  مدیریت فالو / بلاک / گزارش با AJAX + CSRF + Error Handling
// ===========================================================


function getCSRFToken() {
    const m = document.querySelector('meta[name="csrf-token"]');
    return m ? m.getAttribute("content") : "";
}

async function parseJSON(response) {
    const text = await response.text();
    try {
        return JSON.parse(text);
    } catch (err) {
        console.error("❌ JSON معتبر نیست. پاسخ:", text);
        throw err;
    }
}


// ===========================================================
//  FOLLOW / UNFOLLOW
// ===========================================================

document.addEventListener("click", function (event) {

    if (event.target.classList.contains("follow-btn")) {

        const btn = event.target;
        const userId = btn.dataset.userId;

        fetch("/social/ajax/follow/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `id=${userId}`
        })
        .then(parseJSON)
        .then(data => {

            if (data.error) return;

            if (data.follow) {
                btn.innerText = "✔ دنبال شد";
                btn.classList.add("btn-success");
                btn.classList.remove("btn-primary");
            } else {
                btn.innerText = "دنبال کردن";
                btn.classList.remove("btn-success");
                btn.classList.add("btn-primary");
            }
        })
        .catch(err => console.error("FOLLOW ERROR:", err));
    }
});


// ===========================================================
//  BLOCK / UNBLOCK USER
// ===========================================================

document.addEventListener("click", function (event) {

    if (event.target.classList.contains("block-btn")) {

        const btn = event.target;
        const userId = btn.dataset.userId;

        fetch("/social/ajax/toggle-block/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `user_id=${userId}`
        })
        .then(parseJSON)
        .then(data => {

            if (data.status === "error") {
                alert(data.message);
                return;
            }

            if (data.action === "blocked") {
                btn.innerText = "🚫 مسدود شد";
                btn.classList.add("btn-danger");
                btn.classList.remove("btn-outline-danger");
            } else {
                btn.innerText = "مسدود / آزادسازی";
                btn.classList.remove("btn-danger");
                btn.classList.add("btn-outline-danger");
            }
        })
        .catch(err => console.error("BLOCK ERROR:", err));
    }
});


// ===========================================================
//  REPORT USER
// ===========================================================

document.addEventListener("click", function (event) {

    if (event.target.classList.contains("report-btn")) {

        const btn = event.target;
        const userId = btn.dataset.userId;

        const reason = prompt("لطفاً دلیل گزارش را وارد کنید:");
        if (!reason) return;

        fetch("/social/ajax/report/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `user_id=${userId}&reason=${encodeURIComponent(reason)}`
        })
        .then(parseJSON)
        .then(data => {

            if (data.status === "ok") {
                btn.innerText = "✔ گزارش شد";
                btn.disabled = true;
                btn.classList.remove("btn-warning");
                btn.classList.add("btn-secondary");
            } else {
                alert(data.message);
            }
        })
        .catch(err => console.error("REPORT ERROR:", err));
    }
});
