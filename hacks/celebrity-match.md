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
    <div class="control-group">
        <label for="mbti">MBTI Type:</label>
        <select id="mbti">
            <option value="">-- Select your MBTI type --</option>
            <option value="INTJ">INTJ</option><option value="INTP">INTP</option>
            <option value="ENTJ">ENTJ</option><option value="ENTP">ENTP</option>
            <option value="INFJ">INFJ</option><option value="INFP">INFP</option>
            <option value="ENFJ">ENFJ</option><option value="ENFP">ENFP</option>
            <option value="ISTJ">ISTJ</option><option value="ISFJ">ISFJ</option>
            <option value="ESTJ">ESTJ</option><option value="ESFJ">ESFJ</option>
            <option value="ISTP">ISTP</option><option value="ISFP">ISFP</option>
            <option value="ESTP">ESTP</option><option value="ESFP">ESFP</option>
        </select>
    </div>
    <button id="matchBtn">Find Your Celebrity/User Match</button>
</section>

<!-- 🧠 Personality Quiz Section -->
<section>
    <h2>Quick Personality Quiz</h2>
    <p>Answer these 5 short questions to estimate your MBTI type.</p>

    <div id="quiz">
        <div class="control-group">
            <label>1. At a party, you usually...</label>
            <select class="quiz-q" data-dimension="E-I">
                <option value="">-- Choose an answer --</option>
                <option value="E">Talk to lots of people, even strangers</option>
                <option value="I">Stick with people you know well</option>
            </select>
        </div>

        <div class="control-group">
            <label>2. When solving problems, you rely more on...</label>
            <select class="quiz-q" data-dimension="S-N">
                <option value="">-- Choose an answer --</option>
                <option value="S">Practical facts and past experiences</option>
                <option value="N">Ideas, theories, and imagination</option>
            </select>
        </div>

        <div class="control-group">
            <label>3. In decision making, you value...</label>
            <select class="quiz-q" data-dimension="T-F">
                <option value="">-- Choose an answer --</option>
                <option value="T">Logic and consistency</option>
                <option value="F">Feelings and harmony</option>
            </select>
        </div>

        <div class="control-group">
            <label>4. Your workspace is usually...</label>
            <select class="quiz-q" data-dimension="J-P">
                <option value="">-- Choose an answer --</option>
                <option value="J">Organized and planned</option>
                <option value="P">Flexible and spontaneous</option>
            </select>
        </div>

        <div class="control-group">
            <label>5. You gain energy by...</label>
            <select class="quiz-q" data-dimension="E-I">
                <option value="">-- Choose an answer --</option>
                <option value="E">Being around people</option>
                <option value="I">Having time alone</option>
            </select>
        </div>

        <button id="getMbtiBtn">Get My Personality Type</button>
        <div id="mbtiResult" style="margin-top:10px;font-weight:bold;"></div>
    </div>
</section>

<!-- 🎬 Celebrity Compatibility Section -->
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

// --- Load previous users ---
function populateUserDropdown() {
    fetch("http://localhost:5000/api/previous-users")
        .then(resp => resp.json())
        .then(res => {
            if (!res.success) return;
            userDropdown.innerHTML = '<option value="">-- Select a previous user --</option>';
            res.users.forEach(u => {
                const opt = document.createElement("option");
                opt.value = u.name;
                opt.textContent = `${u.name} (${u.age} yrs, ${u.interest}, ${u.mbti || 'No MBTI'})`;
                userDropdown.appendChild(opt);
            });
        })
        .catch(e => console.log("Error loading previous users:", e));
}
populateUserDropdown();


// 🧩 Personality Quiz Logic
document.getElementById("getMbtiBtn").onclick = function() {
    const answers = document.querySelectorAll(".quiz-q");
    let scores = { E: 0, I: 0, S: 0, N: 0, T: 0, F: 0, J: 0, P: 0 };

    let allAnswered = true;
    for (const q of answers) {
        const val = q.value;
        if (!val) allAnswered = false;
        else scores[val]++;
    }

    const resultDiv = document.getElementById("mbtiResult");

    if (!allAnswered) {
        resultDiv.textContent = "⚠️ Please answer all 5 questions before getting your result.";
        resultDiv.style.color = "red";
        return;
    }

    const mbti =
        (scores.E >= scores.I ? "E" : "I") +
        (scores.S >= scores.N ? "S" : "N") +
        (scores.T >= scores.F ? "T" : "F") +
        (scores.J >= scores.P ? "J" : "P");

    resultDiv.style.color = "#fbf4f4ff";
    resultDiv.innerHTML = `Your estimated MBTI type: <b>${mbti}</b>`;
    document.getElementById("mbti").value = mbti;
    localStorage.setItem("userMBTI", mbti);
};


// 🧭 Find Best Celebrity & User Match
document.getElementById("matchBtn").onclick = function() {
    const name = document.getElementById("name").value.trim();
    const age = document.getElementById("age").value;
    const interest = document.getElementById("interest").value.trim();
    const mbti = document.getElementById("mbti").value.trim() || localStorage.getItem("userMBTI") || "";
    const outputDiv = document.getElementById("output");

    if (!name || !age || !interest || !mbti) {
        outputDiv.textContent = "⚠️ Please enter name, age, interest, and MBTI (or take the quiz).";
        return;
    }

    outputDiv.textContent = "⏳ Finding your best celebrity and previous user match...";

    fetch("http://localhost:5000/api/match-user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, age, interest, mbti })
    })
    .then(resp => resp.json())
    .then(result => {
        if (!result.success) {
            outputDiv.textContent = "⚠️ " + (result.error || "Unknown error");
            return;
        }

        let html = `<h3> Your MBTI: ${mbti}</h3><br>`;
        html += "<h3> Best Previous User Match:</h3>";
        if (result.best_user_match) {
            html += `<b>Name:</b> ${result.best_user_match.name}<br>`;
            html += `<b>Age:</b> ${result.best_user_match.age}<br>`;
            html += `<b>Interest:</b> ${result.best_user_match.interest}<br>`;
            html += `<b>MBTI:</b> ${result.best_user_match.mbti || 'N/A'}<br>`;
            html += `<b>Compatibility score:</b> ${result.user_score}/100<br><br>`;
        } else {
            html += "No previous users found.<br><br>";
        }

        html += "<h3> Best Celebrity Match:</h3>";
        if (result.best_celebrity_match) {
            html += `<b>Name:</b> ${result.best_celebrity_match.name}<br>`;
            html += `<b>Profession:</b> ${result.best_celebrity_match.profession}<br>`;
            html += `<b>Interest:</b> ${result.best_celebrity_match.interest}<br>`;
            html += `<b>MBTI:</b> ${result.best_celebrity_match.mbti || 'N/A'}<br>`;
            html += `<b>Compatibility score:</b> ${result.celebrity_score}/100<br>`;
        } else {
            html += "No celebrity match found.<br>";
        }

        outputDiv.innerHTML = html;
        populateUserDropdown();
    })
    .catch(e => { outputDiv.textContent = "⚠️ Error: " + e; });
};


// ⭐ Celebrity Compatibility
document.getElementById("compatCelebrityBtn").onclick = function() {
    const name = document.getElementById("name").value.trim();
    const age = document.getElementById("age").value;
    const interest = document.getElementById("interest").value.trim();
    const mbti = document.getElementById("mbti").value.trim() || localStorage.getItem("userMBTI") || "";
    const celebrity = document.getElementById("celebrityInput").value.trim();
    const outputDiv = document.getElementById("output");

    if (!name || !age || !interest || !mbti || !celebrity) {
        outputDiv.textContent = "⚠️ Please fill all fields or take the quiz.";
        return;
    }

    outputDiv.textContent = "🤖 Checking compatibility with celebrity...";

    fetch("http://localhost:5000/api/compatibility", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name1: name, name2: celebrity, interest1: interest, mbti1: mbti })
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


// 👥 Compatibility with previous user
document.getElementById("compatUserBtn").onclick = function() {
    const name = document.getElementById("name").value.trim();
    const age = document.getElementById("age").value;
    const interest = document.getElementById("interest").value.trim();
    const mbti = document.getElementById("mbti").value.trim() || localStorage.getItem("userMBTI") || "";
    const selectedUser = userDropdown.value;
    const outputDiv = document.getElementById("output");

    if (!name || !age || !interest || !mbti || !selectedUser) {
        outputDiv.textContent = "⚠️ Please fill all fields.";
        return;
    }

    outputDiv.textContent = "🤖 Checking compatibility with previous user...";

    fetch("http://localhost:5000/api/compatibility", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name1: name, name2: selectedUser, interest1: interest, mbti1: mbti })
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
