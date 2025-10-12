---
layout: post
title: Celebrity Matchmaker
permalink: /celebrity-match
---

<style>
#output {
    padding: 15px;
    word-wrap: break-word;
    overflow-wrap: break-word;
    background-color: #f9f9f9;
    border-radius: 8px;
    margin-top: 10px;
}
.controls {
    margin: 10px 0;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    align-items: center;
}
.control-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
    min-width: 200px;
}
label {
    font-weight: bold;
    font-size: 14px;
}
input, select {
    padding: 8px 12px;
    border-radius: 4px;
    border: 1px solid #ccc;
    color: #333;
    background-color: #fff;
}
button {
    padding: 8px 12px;
    border-radius: 4px;
    border: none;
    background-color: #007bff;
    color: white;
    cursor: pointer;
}
button:hover {
    background-color: #0056b3;
}
section {
    margin-bottom: 20px;
}
</style>

<section>
    <h2>Your Info</h2>
    <div class="control-group">
        <label for="name">Name:</label>
        <input type="text" id="name" placeholder="Enter your name">
    </div>
    <div class="control-group">
        <label for="age">Age:</label>
        <input type="number" id="age" min="10" max="99" placeholder="Enter your age">
    </div>
    <div class="control-group">
        <label for="interest">Interest:</label>
        <select id="interest">
            <option value="music">Music</option>
            <option value="sports">Sports</option>
            <option value="reading">Reading</option>
            <option value="travel">Travel</option>
            <option value="gaming">Gaming</option>
        </select>
    </div>
    <button id="matchBtn">Find Your Celebrity/User Match</button>
</section>

<section>
    <h2>Check Compatibility with Celebrity</h2>
    <div class="control-group">
        <label for="celebrityInput">Celebrity Name:</label>
        <input type="text" id="celebrityInput" placeholder="Type a celebrity name">
    </div>
    <button id="compatCelebrityBtn">Check Compatibility</button>
</section>

<section>
    <h2>Check Compatibility with Previous User</h2>
    <div class="control-group">
        <label for="userDropdown">Select Previous User:</label>
        <select id="userDropdown">
            <option value="">-- Select a previous user --</option>
        </select>
    </div>
    <button id="compatUserBtn">Check Compatibility</button>
</section>

<div id="output"></div>

<script>
const userDropdown = document.getElementById("userDropdown");

// --- Populate previous users dropdown dynamically ---
function populateUserDropdown() {
    fetch("http://localhost:5000/api/previous-users")
        .then(resp => resp.json())
        .then(res => {
            if (!res.success) return;
            userDropdown.innerHTML = '<option value="">-- Select a previous user --</option>';
            res.users.forEach(u => {
                const opt = document.createElement("option");
                opt.value = u.name;
                opt.textContent = `${u.name} (${u.age} yrs, ${u.interest})`;
                userDropdown.appendChild(opt);
            });
        })
        .catch(e => console.log("Error loading previous users:", e));
}

// Initial load
populateUserDropdown();

// --- Find best celebrity and user match ---
document.getElementById("matchBtn").onclick = function() {
    const name = document.getElementById("name").value.trim();
    const age = document.getElementById("age").value;
    const interest = document.getElementById("interest").value.trim();
    const outputDiv = document.getElementById("output");

    if (!name || !age || !interest) {
        outputDiv.textContent = "⚠️ Please enter name, age, and interest.";
        return;
    }

    outputDiv.textContent = "⏳ Finding your best celebrity and previous user match...";

    fetch("http://localhost:5000/api/match-user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, age, interest })
    })
    .then(resp => resp.json())
    .then(result => {
        if (!result.success) {
            outputDiv.textContent = "⚠️ " + (result.error || "Unknown error");
            return;
        }

        let html = "<h3>🎯 Best Previous User Match:</h3>";
        if (result.best_user_match) {
            html += `<b>Name:</b> ${result.best_user_match.name}<br>`;
            html += `<b>Age:</b> ${result.best_user_match.age}<br>`;
            html += `<b>Interest:</b> ${result.best_user_match.interest}<br>`;
            html += `<b>Compatibility score:</b> ${result.user_score}/100<br><br>`;
        } else {
            html += "No previous users found.<br><br>";
        }

        html += "<h3>🎉 Best Celebrity Match:</h3>";
        if (result.best_celebrity_match) {
            html += `<b>Name:</b> ${result.best_celebrity_match.name}<br>`;
            html += `<b>Profession:</b> ${result.best_celebrity_match.profession}<br>`;
            html += `<b>Interest:</b> ${result.best_celebrity_match.interest}<br>`;
            html += `<b>Compatibility score:</b> ${result.celebrity_score}/100<br>`;
        } else {
            html += "No celebrity match found.<br>";
        }

        outputDiv.innerHTML = html;

        // Refresh previous user dropdown
        populateUserDropdown();
    })
    .catch(e => { outputDiv.textContent = "⚠️ Error: " + e; });
};

// --- Compatibility with typed celebrity ---
document.getElementById("compatCelebrityBtn").onclick = function() {
    const name = document.getElementById("name").value.trim();
    const age = document.getElementById("age").value;
    const interest = document.getElementById("interest").value.trim();
    const celebrity = document.getElementById("celebrityInput").value.trim();
    const outputDiv = document.getElementById("output");

    if (!name || !age || !interest || !celebrity) {
        outputDiv.textContent = "⚠️ Please enter name, age, interest, and celebrity name.";
        return;
    }

    outputDiv.textContent = "🤖 Checking compatibility with celebrity...";

    fetch("http://localhost:5000/api/compatibility", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name1: name, name2: celebrity, interest1: interest })
    })
    .then(resp => resp.json())
    .then(res => {
        if (!res.success) {
            outputDiv.textContent = "⚠️ " + (res.error || "Unknown error");
            return;
        }
        outputDiv.innerHTML = `<b>Compatibility with ${celebrity}:</b> ${res.score}/100<br><b>Summary:</b> ${res.explanation}`;
    })
    .catch(e => { outputDiv.textContent = "⚠️ Error: " + e; });
};

// --- Compatibility with selected previous user ---
document.getElementById("compatUserBtn").onclick = function() {
    const name = document.getElementById("name").value.trim();
    const age = document.getElementById("age").value;
    const interest = document.getElementById("interest").value.trim();
    const selectedUser = userDropdown.value;
    const outputDiv = document.getElementById("output");

    if (!name || !age || !interest || !selectedUser) {
        outputDiv.textContent = "⚠️ Please enter name, age, interest, and select a previous user.";
        return;
    }

    outputDiv.textContent = "🤖 Checking compatibility with previous user...";

    fetch("http://localhost:5000/api/compatibility", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name1: name, name2: selectedUser, interest1: interest })
    })
    .then(resp => resp.json())
    .then(res => {
        if (!res.success) {
            outputDiv.textContent = "⚠️ " + (res.error || "Unknown error");
            return;
        }
        outputDiv.innerHTML = `<b>Compatibility with ${selectedUser}:</b> ${res.score}/100<br><b>Summary:</b> ${res.explanation}`;
    })
    .catch(e => { outputDiv.textContent = "⚠️ Error: " + e; });
};
</script>
