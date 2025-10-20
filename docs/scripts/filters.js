document.addEventListener("DOMContentLoaded", function () {
  const table = document.querySelector("table");
  if (!table) return;

  const headers = table.querySelectorAll("th");
  const rows = Array.from(table.querySelectorAll("tr")).slice(1);

  const filterableColumns = [1, 2];
  const activeFilters = {};

  filterableColumns.forEach((colIndex) => {
    const values = [
      ...new Set(rows.map((r) => r.cells[colIndex].textContent.trim())),
    ].sort();
    values.unshift("All");

    const select = document.createElement("select");
    select.innerHTML = values
      .map((v) => `<option value="${v}">${v}</option>`)
      .join("");
    headers[colIndex].appendChild(select);

    activeFilters[colIndex] = "All";

    select.addEventListener("change", function () {
      activeFilters[colIndex] = this.value;
      applyFilters();
    });
  });

  function applyFilters() {
    rows.forEach((row) => {
      let visible = true;
      for (const [colIndex, selected] of Object.entries(activeFilters)) {
        const cellText = row.cells[colIndex].textContent.trim();
        if (selected !== "All" && cellText !== selected) {
          visible = false;
          break;
        }
      }
      row.style.display = visible ? "" : "none";
    });
  }
});
