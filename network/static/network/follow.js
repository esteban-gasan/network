const followBtn = document.querySelector("#follow-btn");
const userId = document.querySelector("h1").dataset.userId;

const classes = { Follow: "btn-secondary", Unfollow: "btn-outline-secondary" };

if (followBtn) {
  followBtn.addEventListener("click", (e) => {
    const btn = e.target;
    btn.textContent = btn.textContent === "Follow" ? "Unfollow" : "Follow";
    btn.classList.replace(btn.classList[1], classes[btn.textContent]);

    fetch(`/api/follow/${userId}/`, { method: "POST" })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) alert(data.error);
        console.info(data["message"]);
      })
      .catch((error) => console.log(error));
  });
}
