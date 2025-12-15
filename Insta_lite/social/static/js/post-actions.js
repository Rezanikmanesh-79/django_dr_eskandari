// ===========================================================
//  post-actions.js  — نسخه نهایی
//  مدیریت لایک و ذخیره پست‌ها با AJAX + CSRF + Error Handling
// ===========================================================


// دریافت CSRF token از meta tag
function getCSRFToken() {
    const tokenMeta = document.querySelector('meta[name="csrf-token"]');
    return tokenMeta ? tokenMeta.getAttribute("content") : "";
}


// تبدیل پاسخ به JSON همراه با دیباگ
async function parseJSON(response) {
    const text = await response.text();

    try {
        return JSON.parse(text);
    } catch (err) {
        console.error("❌ سرور JSON نداد! پاسخ دریافتی:", text);
        throw new Error("Server did not return valid JSON");
    }
}


// ===========================================================
//  LIKE / UNLIKE
// ===========================================================

document.addEventListener("click", function (event) {

    if (event.target.classList.contains("like-btn")) {

        const btn = event.target;
        const postId = btn.dataset.postId;

        fetch("/social/ajax/like/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `post_id=${postId}`
        })
        .then(parseJSON)
        .then(data => {

            if (data.error) {
                alert("عملیات لایک انجام نشد.");
                return;
            }

            btn.innerHTML = `👍 لایک (${data.post_like_count})`;

            if (data.liked) {
                btn.classList.add("btn-primary");
                btn.classList.remove("btn-outline-primary");
            } else {
                btn.classList.remove("btn-primary");
                btn.classList.add("btn-outline-primary");
            }
        })
        .catch(err => console.error("LIKE ERROR:", err));
    }
});


// ===========================================================
//  SAVE / UNSAVE POST
// ===========================================================

document.addEventListener("click", function (event) {

    if (event.target.classList.contains("save-btn")) {

        const btn = event.target;
        const postId = btn.dataset.postId;

        fetch("/social/ajax/save_post/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `post_id=${postId}`
        })
        .then(parseJSON)
        .then(data => {

            if (data.error) {
                alert("عملیات ذخیره انجام نشد.");
                return;
            }

            if (data.saved) {
                btn.innerHTML = "💾 ذخیره شد";
                btn.classList.add("btn-success");
                btn.classList.remove("btn-outline-success");
            } else {
                btn.innerHTML = "💾 ذخیره";
                btn.classList.remove("btn-success");
                btn.classList.add("btn-outline-success");
            }
        })
        .catch(err => console.error("SAVE ERROR:", err));
    }
});
