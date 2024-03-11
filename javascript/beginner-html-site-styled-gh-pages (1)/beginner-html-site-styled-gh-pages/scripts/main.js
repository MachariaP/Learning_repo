/* Adding an image changer */

// Select the <img> element from the HTML document and store it in the variable myImage
const myImage = document.querySelector("img");

// Add an onclick event listener to the selected element
myImage.onclick = () => {
    // Get the value of the src attribute of the clicked image and store it in the variable
    const mySrc = myImage.getAttribute("src");

    // Check if the src attribute value is "images/firefox-icon.png"
    if (mySrc === "images/firefox-icon.png") {
        // if the src attribute value is not "images/firefox-icon.png" (i.e., it is "images/firefox2.png" )
        myImage.setAttribute("src", "images/firefox2.png");
    } else {
        // If the src attribute value is not "images/firefox-icon.png" (i.e., it is "image/firefox2.png"),
        // change it back to "images/firefox-icon.png"
        myImage.setAttribute("src", "images/firefox-icon.png");
    }

};

/* Adding a personalized welcome message */
let myButton = document.querySelector("button");
let myHeading = document.querySelector("h1");

// Function to set the personalized greeting
function setUserName() {
    const myName = prompt("Please enter your name.");
    if (!myName) {
        setUserName();
    } else {
        localStorage.setItem("name", myName);
        myHeading.textContent = `Mozilla is cool, ${myName}`;
    }
}

// Check if the user's name is stored in the local storage
if (!localStorage.getItem("name")) {
    // If the user's name is not stored, call the setUserName() function to prompt the enter their name
    setUserName();
} else {
    // If the user's name is stored, retrieve it from the local storage
    const storedName = localStorage.getItem("name");

    // Set the text content of the heading to include the user's stored name
    myHeading.textContent = `Mozilla is cool. ${storedName}`;
}

// Add an onclick event handler to the button element
myButton.onclick = () => {
    // When the button is clicked, call the setUserName() function to prompt the user to enter their name
    setUserName();
};