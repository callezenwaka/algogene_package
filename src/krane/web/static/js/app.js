document.addEventListener("DOMContentLoaded", () => {
    const subscribeInput = document.getElementById("subscribe");
    const subscribeButton = document.getElementById("subscribeButton");
    const buttonText = document.getElementById("buttonText");

    subscribeInput.addEventListener("input", () => {
        if (subscribeInput.value.trim() !== "") {
            subscribeButton.disabled = false;
            subscribeButton.classList.add("isValid");
        } else {
            subscribeButton.disabled = true;
            subscribeButton.classList.remove("isValid");
        }
    });

    document.getElementById("subscribeForm").addEventListener("submit", async (event) => {
        event.preventDefault();
        subscribeButton.disabled = true;
        buttonText.innerHTML = '<svg class="spinner" viewBox="0 0 50 50"><circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle></svg>';

        setTimeout(() => {
            alert("Subscription successful!");
            subscribeInput.value = "";
            buttonText.textContent = "Subscribe";
            subscribeButton.disabled = true;
            subscribeButton.classList.remove("isValid");
        }, 2000); // Simulating API call
    });
});
