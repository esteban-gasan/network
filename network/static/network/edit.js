const editBtns = document.querySelectorAll(".edit-btn");
const template = document.querySelector("template");
var c = undefined;

editBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    const postElement = btn.parentElement;
    const postContent = postElement.querySelector(":scope>p");
    const postArticle = postElement.closest("article");
    const postId = postArticle.dataset.postId;

    const clone = template.content.cloneNode(true);
    const form = clone.querySelector(":scope>form");
    const textArea = clone.querySelector(":scope textarea");
    const cancelBtn = clone.querySelector(":scope .cancel-btn");

    textArea.value = postContent.textContent;
    postElement.style.display = "none";
    postArticle.append(clone);

    cancelBtn.onclick = () => {
      postArticle.lastElementChild.remove();
      postElement.style.display = "block";
    };

    form.onsubmit = (e) => {
      e.preventDefault();
      text = textArea.value;
      postContent.textContent = text;
      postArticle.lastElementChild.remove();
      postElement.style.display = "block";
      sendChanges(postId, text);
    };
  });
});

function sendChanges(postId, text) {
  fetch(`/api/edit/${postId}/`, {
    method: "POST",
    body: JSON.stringify({ text: text }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) alert(data.error);
      console.info(data["message"]);
    })
    .catch((error) => console.log(error));
}
