// Показ/скрытие дополнительной информации о визите
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".toggle-details").forEach(function (button) {
    button.addEventListener("click", function () {
      var block = document.getElementById(button.dataset.target);
      var isHidden = block.hasAttribute("hidden");
      if (isHidden) {
        block.removeAttribute("hidden");
        button.textContent = "Скрыть";
      } else {
        block.setAttribute("hidden", "");
        button.textContent = "Подробнее";
      }
    });
  });
});
