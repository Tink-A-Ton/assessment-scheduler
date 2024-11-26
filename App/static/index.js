var weekCounter = 0;

document.addEventListener("DOMContentLoaded", function () {
  const colors = {
    Assignment: "#3397b9",
    Quiz: "#499373",
    Project: "#006064",
    Exam: "#CC4E4E",
    Presentation: "#cc7a50",
    Other: "#C29203",
    Pending: "#999999",
  };

  const calendarEvents = [];
  renderCourses(myCourses, otherAssessments);
  const levelFilter = document.getElementById("level");
  const courseFilter = document.getElementById("courses");
  
  const calendarEl = document.getElementById("calendar");
  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: "dayGridMonth",
    headerToolbar: {
      left: "prev,next,today",
      center: "title",
      right: "semesterView,dayGridMonth,timeGridWeek,timeGridDay",
    },
    views: {
      semesterView: {
        type: "dayGridMonth",
        duration: { weeks: 13 },
        buttonText: "Semester",
        visibleRange: {
          start: semester.start,
          end: semester.end,
        },
      },
    },
    editable: true,
    selectable: true,
    droppable: true,
    events: calendarEvents,
    eventResize: handleEventEdit,
    eventDrop: handleEventEdit,
    drop: handleNewItem,
  });
  calendar.render();

  levelFilter.addEventListener("change", function () {
    const selectedLevel = levelFilter.value;
    const filteredEvents = filterEventsByLevel(selectedLevel, otherAssessments);
    updateCalendarEvents(calendar, filteredEvents);
  });

  courseFilter.addEventListener("change", function () {
    const selectedCourse = courseFilter.value;
    const filteredEvents = filterEventsByCourse(selectedCourse, otherAssessments);
    updateCalendarEvents(calendar, filteredEvents);
  });

  function renderCourses(courses, assessments) {
    const containerEl = document.getElementById("courses-list");
    courses.forEach((course) => {
      const courseCard = document.createElement("div");
      courseCard.classList.add("course-card");

      const title = document.createElement("h3");
      title.textContent = course.course_code;
      courseCard.appendChild(title);

      const eventsContainer = document.createElement("div");
      eventsContainer.classList.add("course-events");

      assessments
        .filter((a) => a.course_code === course.course_code)
        .forEach((a) => {
          const eventEl = createEventElement(a, course.course_code, colors);
          if (a.start_date && a.end_date) {
            console.log(a);
            const eventObj = createEventObject(a, colors);
            calendarEvents.push(eventObj);
          } else {
            eventsContainer.appendChild(eventEl);
          }
        });
      courseCard.appendChild(eventsContainer);
      containerEl.appendChild(courseCard);
    });

    new FullCalendar.Draggable(containerEl, {
      itemSelector: ".fc-event",
      eventData: (eventEl) => ({
        title: eventEl.innerText.trim(),
        backgroundColor: eventEl.dataset.color,
        id: eventEl.dataset.eventId,
      }),
    });
  }

  function createEventElement(assessment, course_code, colors) {
    const typeOfAssessment = getAssessmentType(assessment.assessment_type.id);
    const color = assessment.clash_detected ? colors.Pending : colors[typeOfAssessment];

    const eventEl = document.createElement("div");
    eventEl.classList.add(
      "fc-event",
      "fc-h-event",
      "fc-daygrid-event",
      "fc-daygrid-block-event"
    );
    eventEl.dataset.color = color;
    eventEl.style.backgroundColor = color;
    eventEl.setAttribute("data-event-id", assessment.id);
    eventEl.innerHTML = '<div class="fc-event-main">' + course_code + '-' + assessment.assessment_type.category + '</div>';
    return eventEl;
  }

  function createEventObject(assessment, colors) {
    const typeOfAssessment = getAssessmentType(assessment.assessment_type.id);
    const isFullDay =
      assessment.start_time === "00:00" &&
      (assessment.end_time === "23:59" || assessment.end_time === "00:00");
    
    return {
      id: assessment.id,
      title: `${assessment.course_code}-${typeOfAssessment}`,
      backgroundColor: colors[typeOfAssessment],
      start: `${assessment.start_date}T${assessment.start_time}`,
      end: `${assessment.end_date}T${assessment.end_time}`,
      allDay: isFullDay,
    };
  }

  function filterEventsByLevel(level, assessments) {
    return level === "0" ? assessments : assessments.filter((item) => item.course_code[4] === level);
  }

  function filterEventsByCourse(courseCode, assessments) {
    return courseCode == "all" ? assessments : assessments.filter((item) => item.course_code === courseCode);
  }

  function updateCalendarEvents(calendar, newEvents) {
    calendar.removeAllEvents();
    const updatedEvents = newEvents.map((a) => createEventObject(a, colors));
    calendar.setOption("events", updatedEvents);
    calendar.render();
    console.log(updatedEvents);
  }

  function handleEventEdit(info) {
    const event = info.event;
    const data = extractEventDetails(event);
    saveEvent(data);
  }

  function handleNewItem(arg) {
    const event = arg.draggedEl;
    const data = {
      id: event.dataset.eventId,
      startDate: formatDate(arg.date),
      endDate: formatDate(arg.date),
      startTime: "00:00",
      endTime: "23:59",
    };
    saveEvent(data);
    arg.draggedEl.parentNode.removeChild(arg.draggedEl);
  }

  function extractEventDetails(event) {
    const id = event.id;
    const startDate = formatDate(new Date(event.start));
    const endDate = event.end ? formatDate(new Date(event.end)) : startDate;
    const startTime = formatTime(new Date(event.start));
    const endTime = event.end ? formatTime(new Date(event.end)) : "23:59";

    return { id, startDate, endDate, startTime, endTime };
  }

  function saveEvent(data) {
    $.ajax({
      url: "/calendar",
      method: "POST",
      data,
      success: () => location.reload(),
      error: (xhr, status, error) => console.error("Error:", error),
    });
  }

  function getAssessmentType(typeId) {
    switch (typeId) {
      case 1:
        return "Exam";
      default:
        return "Exam";
    }
  }

  function formatDate(dateObj) {
    const year = dateObj.getFullYear();
    const month = (dateObj.getMonth() + 1).toString().padStart(2, "0");
    const day = dateObj.getDate().toString().padStart(2, "0");
    return `${year}-${month}-${day}`;
  }

  function formatTime(dateObj) {
    const hours = dateObj.getHours().toString().padStart(2, "0");
    const minutes = dateObj.getMinutes().toString().padStart(2, "0");
    return `${hours}:${minutes}`;
  }
});
