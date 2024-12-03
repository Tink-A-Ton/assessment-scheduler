const searchInput = document.getElementById("search_box");
const searchDropdown = document.getElementById("search-dropdown");
const selectedCourses = document.getElementById("selected_courses");
const searchTerm = searchInput.value.toLowerCase();
const tableBody = document.getElementById("courseTableBody");
const tableRows = tableBody.querySelectorAll("tr.course-row");

searchInput.addEventListener("focus", () => {
  let count = 0;
  tableRows.forEach((row) => {
    if (count < 5) {
      row.style.display = "";
      count++;
    } else {
      row.style.display = "none";
    }
  });
  searchDropdown.style.display = "block";
});


tableRows.forEach((row) => {
  row.addEventListener("click", (event) => {
    event.stopPropagation(); // Stop event bubbling
    const courseCode = row.querySelector("td").textContent;
    addCourse(courseCode);
  });
});

function handleSearch(e) {
  e.preventDefault(); // Prevent form submission
  const searchTerm = searchInput.value.toLowerCase();

  tableRows.forEach((row) => {
    const courseCode = row.querySelector("td").textContent;

    if (courseCode.toLowerCase().includes(searchTerm)) {
      row.style.display = ""; // Show row if it matches search term
    } else {
      row.style.display = "none"; // Hide row if it doesn't match
    }
  });

}

function addCourse(course) {
  if (!myCourses.includes(course)) {
    myCourses.push(course);
    const courseElement = document.createElement("p");
    courseElement.textContent = course;
    courseElement.classList.add("selected-course");
    selectedCourses.appendChild(courseElement);
    const courseCodesInput = document.getElementById("courseCodesInput");
    courseCodesInput.value = JSON.stringify(myCourses);
  }
  // resetSearch()
}

function resetSearch() {
  searchInput.value = "";
  tableRows.forEach((row) => {
    row.style.display = "none";
  });
}
document.addEventListener("click", (event) => {
  if (!event.target.closest(".search-container")) {
    resetSearch();
  }
});

function setExistingCourses() {
  myCourses.forEach(course => {
    const courseElement = document.createElement("p");
    courseElement.textContent = course;
    courseElement.classList.add("selected-course");
    selectedCourses.appendChild(courseElement);
    const courseCodesInput = document.getElementById("courseCodesInput");
    courseCodesInput.value = JSON.stringify(myCourses);
  })
}

setExistingCourses()

resetSearch()

searchInput.addEventListener("keyup", handleSearch);

