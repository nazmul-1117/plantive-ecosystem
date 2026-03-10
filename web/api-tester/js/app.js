// screen navigation

function showScreen(screenId, element) {

    const screens = document.querySelectorAll(".screen");

    screens.forEach(screen => {
        screen.classList.remove("active");
    });

    document.getElementById(screenId).classList.add("active");


    const navItems = document.querySelectorAll(".nav-item");

    navItems.forEach(item => {
        item.classList.remove("active");
    });

    element.classList.add("active");

}


// chat prototype

function sendChat() {

    const input = document.getElementById("chatInput");
    const chatBox = document.getElementById("chatBox");

    const message = input.value;

    if (message === "") return;

    chatBox.innerHTML += `
<p><strong>You:</strong> ${message}</p>
<p><strong>AI:</strong> Water plants regularly 🌱</p>
`;

    input.value = "";

    chatBox.scrollTop = chatBox.scrollHeight;

}