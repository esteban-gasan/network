const likeBtns = document.querySelectorAll(".like-btn");
const likeClasses = { like: "btn-danger", unlike: "btn-outline-secondary" };

likeBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    newClass = btn.classList.contains(likeClasses["like"])
      ? likeClasses["unlike"]
      : likeClasses["like"];
    btn.classList.replace(btn.classList[0], newClass);
    const likeCountDiv = btn.firstElementChild;
    counter = parseInt(likeCountDiv.textContent);
    likeCountDiv.textContent = parseInt(
      newClass === likeClasses["like"] ? counter + 1 : counter - 1
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
