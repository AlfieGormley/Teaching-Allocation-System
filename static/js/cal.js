

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

    });
}

// Initialize global lookup arrays/objects for shifts:
let shiftDates = [];
let shiftMap = {};

console.log('Formatted Shifts:', formatted_shifts);

//CURRENTLY WORKING ON - CURRENTLY WORKING ON - CURRENTLY WORKING ON - CURRENTLY WORKING ON

// Loop through shift_data 
if (typeof formatted_shifts !== "undefined") {
    formatted_shifts.forEach(shift => {
        let fullDate = shift.date;
		let timeRange = `${shift.start_time} - ${shift.end_time}`; 

        let shiftInfo = {
			building: shift.building,
            timeRange: timeRange,
            room: shift.room,
			ta_id: shift.ta_id,
			ml_id: shift.ml_id,
            status: shift.status,
			description: shift.description
        };

        if (!shiftMap[fullDate]) {
            shiftMap[fullDate] = [];
            shiftDates.push(fullDate);
        }

        shiftMap[fullDate].push(shiftInfo);
    });
}

console.log('Shift Map:', shiftMap); // Log the entire shiftMap



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

            
                // Format full date as YYYY-MM-DD. Note that month is zero-indexed in JS Date, so add 1.
                let fullDate = `${year}-${String(month + 1).padStart(2, '0')}-${String(date).padStart(2, '0')}`;

                // Check if the date exists in our availabilityDates array
                if (availabilityDates.includes(fullDate)) {
                    cell.classList.add("available"); // Apply the available style (green highlight)

                    let tooltipText = "Available: " + availabilityMap[fullDate].join("; ");
                    cell.setAttribute("title", tooltipText);

                    //cell.setAttribute("title", `Available: ${availabilityMap[fullDate]}`);
                }

				// Check if the date exists in our shiftDates array
				if (shiftDates.includes(fullDate)) {
					console.log('Checking shifts for:', fullDate); // Log the fullDate to see if it's being checked

					//Loop through shifts for the current date
					shiftMap[fullDate].forEach(shift => {
						//Check the shift status
						let shiftStatus = shift.status; // approved, pending, or rejected

						// Apply color based on status
						if (shiftStatus === "approved") {
							cell.classList.add("approved"); // Green colour for approved
						} else if (shiftStatus === "pending") {
							cell.classList.add("pending"); // Yellow colour for pending
						} else if (shiftStatus === "rejected") {
							cell.classList.add("rejected"); // Red colour for rejected
						}

						// Set a tooltip for the shift
						let tooltipText = `Shift for Room ${shift.room}: ${shift.timeRange} - Status: ${shift.status}`;
						cell.setAttribute("title", tooltipText);
					});
				}
                
                
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

                //Left Click
                cell.addEventListener("click", function () {
                    open_form(fullDate);
                });

                //Right Click
                cell.addEventListener("contextmenu", function (event) {
                    event.preventDefault();
                    
                    showManageEventsButton(event, fullDate)
                })

                
                //Adds the cell to the row and increments the date
				row.appendChild(cell);
				date++;
			}
		}
        //This appends the row to the table
		tbl.appendChild(row);
	}

	
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

    var user_role = document.body.getAttribute("data-role").trim(); 

    console.log("User role:", user_role);


    document.getElementById("availability_date").value = date;

    console.log("User role:", user_role); 

    if (user_role == "Module Leader") {

        console.log("Opening request support form"); // Debugging
        // If the user is a Module Leader, open the request support form
        document.getElementById("request_support_form").style.display = "block";
    } else {
        console.log("Opening availability form");
        // If the user is not a Module Leader, open the availability form
        document.getElementById("availability_form").style.display = "block";
    }


    //document.getElementById("availability_date").value = date;
    //document.getElementById("availability_form").style.display = "block";
}


function close_form() {

    var user_role = document.body.getAttribute("data-role").trim(); 

    console.log("User role:", user_role);


    if (user_role == "Module Leader") {
        console.log("Closing request support form"); // Debugging
        // If the user is a Module Leader, close the request support form
        document.getElementById("request_support_form").style.display = "none";
    } else {
        console.log("Closing availability form");
        // If the user is not a Module Leader, close the availability form
        document.getElementById("availability_form").style.display = "none";
    }

}


// Function to show the "Manage Events" button on right-click
function showManageEventsButton(event, date) {
    let button = document.getElementById("manage-events-button");

    if (!button) {
        button = document.createElement("button");
        button.id = "manage-events-button";
        button.textContent = "View Events";
        button.style.position = "absolute";
        button.style.padding = "8px";
        button.style.background = "#007bff";
        button.style.color = "#fff";
        button.style.border = "none";
        button.style.cursor = "pointer";
        button.style.zIndex = "1000";
        document.body.appendChild(button);
    }

    button.style.left = `${event.pageX}px`;
    button.style.top = `${event.pageY}px`;
    button.style.display = "block";

    button.onclick = function () {

		//Uncomment to get ta working again
        //_manage_availability_form(date);
		view_schedule_form(date)

    };

    document.addEventListener("click", function () {
        button.style.display = "none";
    }, { once: true });
}


function view_schedule_form(date) {

	//Get the date
    document.getElementById("schedule_form_date").value = date;

	console.log("formatted_shifts", typeof(formatted_shifts));

	//Finds the container for the availaibility_list and Clears previous availability for when a new date is selected
	const schedule_list = document.getElementById("schedule_list");
    schedule_list.innerHTML = ""; 

	//Retrieves schedule for the given date
	const filtered_schedule = formatted_shifts.filter(slot => slot.date === date);
	
	

	if (filtered_schedule.length > 0) {

		//Iterates over each slot in the array
		filtered_schedule.forEach(slot => {

			//Creates a new paragraph element for each availability slot
            const slot_element = document.createElement("div");
			slot_element.classList.add("schedule-slot");

			const slot_text = document.createElement("p");
			slot_text.classList.add("schedule-text");


			//The text content inside the slot element
			slot_text.innerHTML = 
				`<strong>Time:</strong> ${slot.start_time} - ${slot.end_time} ` +
				`<strong>Floor:</strong> ${slot.floor} ` +
				`<strong>Room:</strong> ${slot.room} ` +
				`<strong>Building:</strong> ${slot.building_name} ` +
				`<strong>TA:</strong> ${slot.ta_name} ` +
				`<strong>Status:</strong> ${slot.status} `;


			//Button for cancelling the shift
			const drop_button = document.createElement("button");
			drop_button.classList.add("cancel-button");
			drop_button.textContent = "Cancel Shift";

			//Event listener for drop_button
			drop_button.addEventListener("click", () => {

				//This is logging the correct _id in the console
				console.log(slot.shift_id)

			})

			drop_button.setAttribute("data-id", slot.shift_id);
			slot_element.appendChild(slot_text);
			slot_element.appendChild(drop_button);

			//Adds the slot element to availability_list
            schedule_list.appendChild(slot_element);

        });
	} else {
		schedule_list.innerHTML = "<p>You have no availability set for this date.</p>";
	}

}



function _manage_availability_form(date) {
    document.getElementById("manage_availability_date").value = date;
	
	console.log("availability_data:", typeof(availability_data));

	//Finds the container for the availaibility_list and Clears previous availability for when a new date is selected
	const availability_list = document.getElementById("availability_list");
    availability_list.innerHTML = ""; 

	//Retrieves availability data for the given date
	const filtered_availability = availability_data.filter(slot => slot.date === date);

	//Debugging
	console.log("Filtered availability:", filtered_availability);

	if (filtered_availability.length > 0) {

		//Iterates over each slot in the array
		filtered_availability.forEach(slot => {

			//Creates a new paragraph element for each availability slot
            const slot_element = document.createElement("div");
			slot_element.classList.add("availability-slot");


			const slot_text = document.createElement("p");
			slot_text.classList.add("availability-text");

			//The text content inside the slot element
            slot_text.textContent = `${slot.start_time} - ${slot.end_time}`;

			//Button for dropping the availability
			const drop_button = document.createElement("button");
			drop_button.classList.add("drop-button");
			drop_button.textContent = "Drop Availability";


			//Event listener for drop_button
			drop_button.addEventListener("click", () => {

				//This is logging the correct _id in the console
				console.log(slot._id)

				//Send _id to the backend
				//Remove the slot_element from the front end

			})

			drop_button.setAttribute("data-id", slot._id);

			slot_element.appendChild(slot_text);
			slot_element.appendChild(drop_button);

			//Adds the slot element to availability_list
            availability_list.appendChild(slot_element);

        });
	} else {
		availability_list.innerHTML = "<p>You have no availability set for this date.</p>";
	}

	//Changes the display style making the form visible
    document.getElementById("manage_availability_form").style.display = "block";

}

function close_manage_availability_form() {
    document.getElementById("manage_availability_form").style.display = "none";
}


document.getElementById('buildings').addEventListener('change', function() {
    const selectedBuilding = this.options[this.selectedIndex];
    const numberOfFloors = selectedBuilding.getAttribute('data-floors');
    
    const floorsDropdown = document.getElementById('floors');
    floorsDropdown.innerHTML = ''; // Clear previous options

    // Add floor options (e.g., 'G', 1, 2, 3)
    for (let i = 0; i <= numberOfFloors; i++) {
        const option = document.createElement('option');
        option.value = i === 0 ? 'G' : i;  // 'G' for ground floor, otherwise the floor number
        option.textContent = i === 0 ? 'G' : i;
        floorsDropdown.appendChild(option);
    }
});

