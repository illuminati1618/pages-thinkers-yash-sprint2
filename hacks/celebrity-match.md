---
layout: post
title: Celebrity Matchmaker
permalink: /celebrity-match
---

<style>
#output {
    padding: 10px;
    word-wrap: break-word;
    overflow-wrap: break-word;
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
    border: 1px solid #ccc;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
}
button:hover {
    background-color: #0056b3;
}
</style>

<details style="padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #007bff;">
  <summary style="cursor: pointer; font-weight: bold; color: #007bff; font-size: 18px;">How does it work?</summary>
  <div style="margin-top: 10px;">
    <p>Enter your info and get matched with a celebrity based on your interests!</p>
  </div>
</details>

<div class="controls">
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
</div>

<button id="matchBtn">Find Your Celebrity Match</button>
<div id="output"></div>

<script>
document.getElementById("matchBtn").onclick = function() {
    const name = document.getElementById("name").value;
    const age = document.getElementById("age").value;
    const interest = document.getElementById("interest").value;
    const outputDiv = document.getElementById("output");
    outputDiv.textContent = "⏳ Matching you with a celebrity...";

    fetch("http://localhost:5000/api/match-celebrity", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            name: name,
            age: age,
            interest: interest
        })
    })
    .then(resp => {
        if (!resp.ok) return resp.text().then(text => { throw new Error(text); });
        return resp.json();
    })
    .then(result => {
        if (result.success && result.celebrity) {
            outputDiv.innerHTML = `<b>🎉 Your Celebrity Match:</b><br>Name: ${result.celebrity.name}<br>Profession: ${result.celebrity.profession}<br>Interest: ${result.celebrity.interest}`;
        } else {
            outputDiv.textContent = "✅ No match found. Try another interest.";
        }
    })
    .catch(e => {
        outputDiv.textContent = "⚠️ Fetch Error: " + e;
    });
};
</script>
