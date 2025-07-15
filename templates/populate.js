function renderBarChart(containerId, data) {
  const container = document.getElementById(containerId);
  container.innerHTML = ""; // Clear existing content

  for (const [label, value] of Object.entries(data)) {
    const row = document.createElement("div");
    row.className = "bar-row";

    const labelEl = document.createElement("div");
    labelEl.className = "bar-label";
    labelEl.textContent = label.charAt(0).toUpperCase() + label.slice(1);

    const track = document.createElement("div");
    track.className = "bar-track";

    const fill = document.createElement("div");
    fill.className = "bar-fill";
    fill.style.width = `${value}%`;

    track.appendChild(fill);
    row.appendChild(labelEl);
    row.appendChild(track);
    container.appendChild(row);
  }
}

fetch('/api/persona')
  .then(res => res.json())
  .then(data => {
    // Fill static text
    document.getElementById("name").textContent = data.username || "-";
    document.getElementById("quote").textContent = `"${data.quote || "-"}"`;
    document.getElementById("age").textContent = data.age || "-";
    document.getElementById("occupation").textContent = data.occupation || "-";
    document.getElementById("status").textContent = data.status || "-";
    document.getElementById("location").textContent = data.location || "-";
    document.getElementById("tier").textContent = data.tier || "-";
    document.getElementById("archetype").textContent = data.archetype || "-";

    ["habits", "frustrations", "goals"].forEach(section => {
      const container = document.getElementById(section);
      (data[section] || []).forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        container.appendChild(li);
      });
    });

    // Render bar graphs
    renderBarChart("motivations-graph", data.motivations || {});
    renderBarChart("personality-graph", data.personality || {});
  });
