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

// Keep track of the sorting direction for each column
let sortDirections = [];

function sortTable(columnIndex) {
    const table = document.getElementById("sortableTable");
    const tbody = document.getElementById("tableBody");
    const rows = Array.from(tbody.querySelectorAll("tr"));
    
    // Determine sort direction: 'asc' for first click, 'desc' for second, then toggle
    const currentDirection = sortDirections[columnIndex] === 'asc' ? 'desc' : 'asc';
    sortDirections = []; // Reset directions for other columns
    sortDirections[columnIndex] = currentDirection;

    // Sort the rows
    const sortedRows = rows.sort((rowA, rowB) => {
        const cellA = rowA.cells[columnIndex].textContent.trim();
        const cellB = rowB.cells[columnIndex].textContent.trim();

        // Basic data type detection (can be expanded for more types like dates)
        const isNumeric = !isNaN(parseFloat(cellA)) && isFinite(cellA) && !isNaN(parseFloat(cellB)) && isFinite(cellB);

        if (isNumeric) {
            // Sort numerically
            return currentDirection === 'asc' ? cellA - cellB : cellB - cellA;
        } else {
            // Sort alphabetically (case-insensitive)
            return currentDirection === 'asc' 
                ? cellA.localeCompare(cellB, undefined, { numeric: true, sensitivity: 'base' })
                : cellB.localeCompare(cellA, undefined, { numeric: true, sensitivity: 'base' });
        }
    });
    // Re-append the sorted rows to the tbody
    while (tbody.firstChild) {
        tbody.removeChild(tbody.firstChild);
    }
    sortedRows.forEach(row => tbody.appendChild(row));
}