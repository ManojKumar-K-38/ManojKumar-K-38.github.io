document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".child");
  const display = document.getElementById("display");

  let currentInput = "";

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const value = button.dataset.value || button.textContent.trim();

      switch (value) {
        case "AC":
          currentInput = "";
          break;
        case "DEL":
          currentInput = currentInput.slice(0, -1);
          break;
        case "=":
          try {
            currentInput = eval(currentInput).toString();
          } catch {
            currentInput = "Error";
          }
          break;
        default:
          currentInput += value;
      }

      display.value = currentInput;
    });
  });
});
