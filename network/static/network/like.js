const likeBtns = document.querySelectorAll(".like-btn");
const classes = { Like: "btn-danger", Unlike: "btn-outline-danger" };

likeBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    btn.textContent = btn.textContent === "Like" ? "Unlike" : "Like";
    btn.classList.replace(btn.classList[2], classes[btn.textContent]);
    const likeCountDiv = btn.previousElementSibling;
    counter = likeCountDiv.textContent;
    likeCountDiv.textContent = parseInt(
      btn.textContent === "Unlike" ? counter + 1 : counter - 1
    );

    const postId = btn.closest("article").dataset.postId;
    fetch(`/api/like/${postId}/`, { method: "POST" })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) alert(data.error);
        console.info(data["message"]);
      })
      .catch((error) => console.log(error));
  });
});
