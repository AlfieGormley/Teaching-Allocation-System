// script.js



// Initialize global lookup arrays/objects for availability:
let availabilityDates = [];
let availabilityMap = {};

// Loop through availability_data 
if (typeof availability_data !== "undefined") {
    availability_data.forEach(slot => {
        // slot.date is already in YYYY-MM-DD format.
        let fullDate = slot.date;
        let timeRange = `${slot.start_time} - ${slot.end_time}`;

        if (!availabilityMap[fullDate]) {
            availabilityMap[fullDate] = [];
            availabilityDates.push(fullDate);
        }

        availabilityMap[fullDate].push(timeRange);

        //availabilityDates.push(fullDate);
        //availabilityMap[fullDate] = timeRange;
    });
}


// Define an array to store events
let events = [];

// letiables to store event input fields and reminder list
let eventDateInput =
	document.getElementById("eventDate");
let eventTitleInput =
	document.getElementById("eventTitle");
let eventDescriptionInput =
	document.getElementById("eventDescription");
let reminderList =
	document.getElementById("reminderList");

// Counter to generate unique event IDs
let eventIdCounter = 1;





// Function to generate a range of 
// years for the year select input
function generate_year_range(start, end) {
	let years = "";
	for (let year = start; year <= end; year++) {
		years += "<option value='" +
			year + "'>" + year + "</option>";
	}
	return years;
}

// Initialize date-related letiables
today = new Date();
currentMonth = today.getMonth();
currentYear = today.getFullYear();
selectYear = document.getElementById("year");
selectMonth = document.getElementById("month");

createYear = generate_year_range(1970, 2050);

document.getElementById("year").innerHTML = createYear;

let calendar = document.getElementById("calendar");

let months = [
	"January",
	"February",
	"March",
	"April",
	"May",
	"June",
	"July",
	"August",
	"September",
	"October",
	"November",
	"December"
];
let days = [
	"Sun", "Mon", "Tue", "Wed",
	"Thu", "Fri", "Sat"];

$dataHead = "<tr>";
for (dhead in days) {
	$dataHead += "<th data-days='" +
		days[dhead] + "'>" +
		days[dhead] + "</th>";
}
$dataHead += "</tr>";

document.getElementById("thead-month").innerHTML = $dataHead;

monthAndYear =
	document.getElementById("monthAndYear");
showCalendar(currentMonth, currentYear);




//Keep
// Function to navigate to the next month
function next() {
	currentYear = currentMonth === 11 ?
		currentYear + 1 : currentYear;
	currentMonth = (currentMonth + 1) % 12;
	showCalendar(currentMonth, currentYear);
}


//Keep
// Function to navigate to the previous month
function previous() {
	currentYear = currentMonth === 0 ?
		currentYear - 1 : currentYear;
	currentMonth = currentMonth === 0 ?
		11 : currentMonth - 1;
	showCalendar(currentMonth, currentYear);
}


//Keep
// Function to jump to a specific month and year
function jump() {
	currentYear = parseInt(selectYear.value);
	currentMonth = parseInt(selectMonth.value);
	showCalendar(currentMonth, currentYear);
}



// Function to display the calendar
function showCalendar(month, year) {
    //Creates a Date object representing the first day of the given month/year. getDay() returns the day of the week
	let firstDay = new Date(year, month, 1).getDay();

    //This selects the table body element and clears the previous calendar content
	tbl = document.getElementById("calendar-body");
	tbl.innerHTML = "";

    //Updates the display of the month and year
	monthAndYear.innerHTML = months[month] + " " + year;
	selectYear.value = year;
	selectMonth.value = month;

    //This is where we start generating the calendar table
	let date = 1;
    //This loop runs up to 6 times as this is the max rows needed for a month
	for (let i = 0; i < 6; i++) {

        //Creates a tr element stored to the variable row
		let row = document.createElement("tr");
        //This runs 7 times, once for each day of the week
		for (let j = 0; j < 7; j++) {
            
            //This adds empty cells before the first day of that month
			if (i === 0 && j < firstDay) {
				cell = document.createElement("td");
				cellText = document.createTextNode("");
				cell.appendChild(cellText);
				row.appendChild(cell);
                
                //Breaks the loop once all days in that month have been added 
			} else if (date > daysInMonth(month, year)) {
				break;
			} else {
                //Creates a td for the current date
				cell = document.createElement("td");
                
				cell.setAttribute("data-date", date); 
				cell.setAttribute("data-month", month + 1);
				cell.setAttribute("data-year", year);
				cell.setAttribute("data-month_name", months[month]);
				cell.className = "date-picker";
                //Sets the date number of the cell
				cell.innerHTML = "<span>" + date + "</span";

                

                //TESTING CODE FOR CALENDAR AVAILABILITY

                // Format full date as YYYY-MM-DD. Note that month is zero-indexed in JS Date, so add 1.
                let fullDate = `${year}-${String(month + 1).padStart(2, '0')}-${String(date).padStart(2, '0')}`;

                // Check if the date exists in our availabilityDates array
                if (availabilityDates.includes(fullDate)) {
                    cell.classList.add("available"); // Apply the available style (green highlight)

                    let tooltipText = "Available: " + availabilityMap[fullDate].join("; ");
                    cell.setAttribute("title", tooltipText);

                    //cell.setAttribute("title", `Available: ${availabilityMap[fullDate]}`);
                }
                

                //TESTING CODE FOR CALENDAR AVAILABILITY
                

                //This styles the current date differently to the others
				if (
					date === today.getDate() &&
					year === today.getFullYear() &&
					month === today.getMonth()
				) {
					cell.className = "date-picker selected";
				}

				// Check if there are events on this date and marks it if it i
				if (hasEventOnDate(date, month, year)) {
					cell.classList.add("event-marker");
					cell.appendChild(
						createEventTooltip(date, month, year)
				);
				}


                cell.addEventListener("click", function () {
                    open_form(fullDate);
                });
                
                //Adds the cell to the row and increments the date
				row.appendChild(cell);
				date++;
			}
		}
        //This appends the row to the table
		tbl.appendChild(row);
	}

	displayReminders();
}


// Function to create an event tooltip
function createEventTooltip(date, month, year) {
	let tooltip = document.createElement("div");
	tooltip.className = "event-tooltip";
	let eventsOnDate = getEventsOnDate(date, month, year);
	for (let i = 0; i < eventsOnDate.length; i++) {
		let event = eventsOnDate[i];
		let eventDate = new Date(event.date);
		let eventText = `<strong>${event.title}</strong> - 
			${event.description} on 
			${eventDate.toLocaleDateString()}`;
		let eventElement = document.createElement("p");
		eventElement.innerHTML = eventText;
		tooltip.appendChild(eventElement);
	}
	return tooltip;
}


// Function to get events on a specific date
function getEventsOnDate(date, month, year) {
	return events.filter(function (event) {
		let eventDate = new Date(event.date);
		return (
			eventDate.getDate() === date &&
			eventDate.getMonth() === month &&
			eventDate.getFullYear() === year
		);
	});
}


// Function to check if there are events on a specific date
function hasEventOnDate(date, month, year) {
	return getEventsOnDate(date, month, year).length > 0;
}


// Function to get the number of days in a month
function daysInMonth(iMonth, iYear) {
	return 32 - new Date(iYear, iMonth, 32).getDate();
}


// Call the showCalendar function initially to display the calendar
showCalendar(currentMonth, currentYear);



function open_form(date) {
    document.getElementById("availability_date").value = date;
    document.getElementById("availability_form").style.display = "block";
}

function close_form() {
    document.getElementById("availability_form").style.display = "none";
}