

//Finds the form with name:register_form, when submitted it run this function
$("form[name='register_form']").submit(function(e) {
    
    //Prevents the page reloading
    e.preventDefault();

    //Stores the form object
    var $form = $(this);

    //Finds the error class to display error messages
    var $error = $form.find(".error");

    //Collects the data submitted from the form to be sent to the server as a POST request
    var data = $form.serialize();

    //AJAX requests are sent to the backend
    $.ajax({

        //Sends the request to the route which handles registration
        url: "/user/register",

        //POST request is used to create a new user 
        type: "POST",

        //Sends the form data
        data: data,

        //Expecting a json response
        dataType: "json",

        //If the response is succesfull
        success: function(resp) {

            //Logs the servers response in the console
            console.log(resp);
            
            $error.text("Registration successful!").removeClass("error--hidden").addClass("success");
        },
        error: function(resp) {

            //Logs the error response in the browser console
            console.log(resp);

            //This will look at our models.py file and return the appropriate error message
            $error.text(resp.responseJSON.error).removeClass("error--hidden"); 
        }
    });


});


//Java Script to handle the login form
$("form[name='login_form']").submit(function(e) {
    
    //Prevents the page reloading
    e.preventDefault();

    //Stores the form object
    var $form = $(this);

    //Finds the error class to display error messages
    var $error = $form.find(".error");

    //Collects the data submitted from the form to be sent to the server as a POST request
    var data = $form.serialize();

    //AJAX requests are sent to the backend
    $.ajax({

        //Sends the request to the route which handles login
        url: "/user/login",

        
        type: "POST",

        //Sends the form data
        data: data,

        //Expecting a json response
        dataType: "json",

        //If the response is succesfull
        success: function(resp) {

            //Logs the servers response in the console
            console.log(resp);

            // Redirect to appropriate page based on user role
                if (resp.role === "Teaching Associate") {
                    window.location.href = "/ta/";
                } else if (resp.role === "Admin") {
                    window.location.href = "/admin/";
                } else if (resp.role === "Module Leader") {
                    window.location.href = "/ml/";
                } else {
                    window.location.href = "/";  // Default redirect if no role matches
                }

        },
        
        error: function(resp) {

            //Logs the error response in the browser console
            console.log(resp);

            //This will look at our models.py file and return the appropriate error message
            $error.text(resp.responseJSON.error).removeClass("error--hidden"); 
        }
    });

    
});


//Finds the form with name:skills_form, when submitted it run this function
$("form[name='skills_form']").submit(function(e) {
    
    //Prevents the page reloading
    e.preventDefault();

    //Stores the form object
    var $form = $(this);

    //Finds the error class to display error messages
    var $error = $form.find(".error");

    //Collects the data submitted from the form to be sent to the server as a POST request
    var data = $form.serialize();

    //AJAX requests are sent to the backend
    $.ajax({

        //Sends the request to the route which handles skill updates
        url: "/user/update_skills",

        //POST request
        type: "POST",

        //Sends the form data
        data: data,

        //Expecting a json response
        dataType: "json",

        //If the response is succesfull
        success: function(resp) {

            //Logs the servers response in the console
            console.log(resp);
            
            $error.text("Successful Update!").removeClass("error--hidden").addClass("success");
        },

        error: function(resp) {

            //Logs the error response in the browser console
            console.log(resp);

            //This will look at our models.py file and return the appropriate error message
           // $error.text(resp.responseJSON.error).removeClass("error--hidden"); 
        }
    });

});


//Finds the form with name:remove_skills_form, when submitted it run this function
$("form[name='remove_skills_form']").submit(function(e) {
    
    //Prevents the page reloading
    e.preventDefault();

    //Stores the form object
    var $form = $(this);

    //Finds the error class to display error messages
    var $error = $form.find(".error");

    //Collects the data submitted from the form to be sent to the server as a POST request
    var data = $form.serialize();

    //AJAX requests are sent to the backend
    $.ajax({

        //Sends the request to the route which handles skill updates
        url: "/user/remove_skills",

        //POST request
        type: "POST",

        //Sends the form data
        data: data,

        //Expecting a json response
        dataType: "json",

        //If the response is succesfull
        success: function(resp) {

            //Logs the servers response in the console
            console.log(resp);
            
            $error.text("Successful Update!").removeClass("error--hidden").addClass("success");
        },

        error: function(resp) {

            //Logs the error response in the browser console
            console.log(resp);

            //This will look at our models.py file and return the appropriate error message
           // $error.text(resp.responseJSON.error).removeClass("error--hidden"); 
        }
    });

});


//Finds the form with name:remove_skills_form, when submitted it run this function
$("form[name='remove_user_form']").submit(function(e) {
    
    //Prevents the page reloading
    e.preventDefault();

    //Stores the form object
    var $form = $(this);

    //Finds the error class to display error messages
    var $error = $form.find(".error");

    //Collects the data submitted from the form to be sent to the server as a POST request
    var data = $form.serialize();

    //AJAX requests are sent to the backend
    $.ajax({

        //Sends the request to the route which handles skill updates
        url: "/user/delete_user",

        //POST request
        type: "POST",

        //Sends the form data
        data: data,

        //Expecting a json response
        dataType: "json",

        //If the response is succesfull
        success: function(resp) {

            //Logs the servers response in the console
            console.log(resp);
            
            $error.text("Successful Update!").removeClass("error--hidden").addClass("success");
        },

        error: function(resp) {

            //Logs the error response in the browser console
            console.log(resp);

            //This will look at our models.py file and return the appropriate error message
           // $error.text(resp.responseJSON.error).removeClass("error--hidden"); 
        }
    });

});


//Finds the form with name:register_form, when submitted it run this function
$("form[name='change_password_form']").submit(function(e) {
    
    //Prevents the page reloading
    e.preventDefault();

    //Stores the form object
    var $form = $(this);

    //Finds the error class to display error messages
    var $error = $form.find(".error");

    //Collects the data submitted from the form to be sent to the server as a POST request
    var data = $form.serialize();

    //AJAX requests are sent to the backend
    $.ajax({

        //Sends the request to the route which handles registration
        url: "/user/change_password",

        //POST request is used to create a new user 
        type: "POST",

        //Sends the form data
        data: data,

        //Expecting a json response
        dataType: "json",

        //If the response is succesfull
        success: function(resp) {

            //Logs the servers response in the console
            console.log(resp);
            
            $error.text("Password Change successful!").removeClass("error--hidden").addClass("success");
        },
        error: function(resp) {

            //Logs the error response in the browser console
            console.log(resp);

            //This will look at our models.py file and return the appropriate error message
            $error.text(resp.responseJSON.error).removeClass("error--hidden"); 
        }
    });


});


//Finds the form with name:remove_skills_form, when submitted it run this function
$("form[name='toggle_mobile_form']").submit(function(e) {
    
    //Prevents the page reloading
    e.preventDefault();

    //Stores the form object
    var $form = $(this);

    //Finds the error class to display error messages
    var $error = $form.find(".error");

    //Collects the data submitted from the form to be sent to the server as a POST request
    var data = $form.serialize();

    //AJAX requests are sent to the backend
    $.ajax({

        //Sends the request to the route which handles skill updates
        url: "/user/toggle_mobile",

        //POST request
        type: "POST",

        //Sends the form data
        data: data,

        //Expecting a json response
        dataType: "json",

        //If the response is succesfull
        success: function(resp) {

            //Logs the servers response in the console
            console.log(resp);
            
            $error.text("Successful Update!").removeClass("error--hidden").addClass("success");
        },

        error: function(resp) {

            //Logs the error response in the browser console
            console.log(resp);

            //This will look at our models.py file and return the appropriate error message
           // $error.text(resp.responseJSON.error).removeClass("error--hidden"); 
        }
    });

});


//Finds the form with name:register_form, when submitted it run this function
$("#availability_form_content").submit(function(e) {
    
    //Prevents the page reloading
    e.preventDefault();

    //Stores the form object
    var $form = $(this);

    //Finds the error class to display error messages
    var $error = $form.find(".error");

    //Collects the data submitted from the form to be sent to the server as a POST request
    var data = $form.serialize();

    console.log(data);

    //AJAX requests are sent to the backend
    $.ajax({

        //Sends the request to the route which handles registration
        url: "/user/set_availability",

        //POST request is used to create a new user 
        type: "POST",

        //Sends the form data
        data: data,

        //Expecting a json response
        dataType: "json",

        //If the response is succesfull
        success: function(resp) {

            //Logs the servers response in the console
            console.log(resp);
            
            $error.text("Registration successful!").removeClass("error--hidden").addClass("success");
        },
        error: function(resp) {

            //Logs the error response in the browser console
            console.log(resp);

            //This will look at our models.py file and return the appropriate error message
            $error.text(resp.responseJSON.error).removeClass("error--hidden"); 
        }
    });


});


//Finds the form with name:remove_skills_form, when submitted it run this function
$("form[name='add_new_skill_form']").submit(function(e) {
    
    //Prevents the page reloading
    e.preventDefault();

    //Stores the form object
    var $form = $(this);

    //Finds the error class to display error messages
    var $error = $form.find(".error");

    //Collects the data submitted from the form to be sent to the server as a POST request
    var data = $form.serialize();

    //AJAX requests are sent to the backend
    $.ajax({

        //Sends the request to the route which handles skill updates
        url: "/user/add_new_skill",

        //POST request
        type: "POST",

        //Sends the form data
        data: data,

        //Expecting a json response
        dataType: "json",

        //If the response is succesfull
        success: function(resp) {

            //Logs the servers response in the console
            console.log(resp);
            
            $error.text("Successful Update!").removeClass("error--hidden").addClass("success");
        },

        error: function(resp) {

            //Logs the error response in the browser console
            console.log(resp);

            //This will look at our models.py file and return the appropriate error message
           // $error.text(resp.responseJSON.error).removeClass("error--hidden"); 
        }
    });

});


//Finds the form with name:remove_skills_form, when submitted it run this function
$("form[name='admin_remove_skill_form']").submit(function(e) {
    
    //Prevents the page reloading
    e.preventDefault();

    //Stores the form object
    var $form = $(this);

    //Finds the error class to display error messages
    var $error = $form.find(".error");

    //Collects the data submitted from the form to be sent to the server as a POST request
    var data = $form.serialize();

    //AJAX requests are sent to the backend
    $.ajax({

        //Sends the request to the route which handles skill updates
        url: "/user/admin_remove_skill",

        //POST request
        type: "POST",

        //Sends the form data
        data: data,

        //Expecting a json response
        dataType: "json",

        //If the response is succesfull
        success: function(resp) {

            //Logs the servers response in the console
            console.log(resp);
            
            $error.text("Successful Update!").removeClass("error--hidden").addClass("success");
        },

        error: function(resp) {

            //Logs the error response in the browser console
            console.log(resp);

            //This will look at our models.py file and return the appropriate error message
           // $error.text(resp.responseJSON.error).removeClass("error--hidden"); 
        }
    });

});


//This is used to send the _id of the availability slot we want to drop to the backend

$(document).ready(function() {

    //Event listener for the drop button
    $(document).on("click", ".drop-button", function(e) {

        e.preventDefault(); // Prevent page from refreshing

        var slot_id = $(this).data("id"); // Get the _id from data attribute
        //var slot_element = $(this).closest(".availability-slot"); // Find the parent container

        console.log("Removing availability with _id:", slot_id); // Debugging

        $.ajax({
            url: "/user/drop_availability", 
            type: "POST",
            data: { _id: slot_id }, // Send the _id to the backend
            dataType: "json",

            success: function(resp) {

                console.log(resp);

                $error.text("Successful Update!").removeClass("error--hidden").addClass("success");


            },

            error: function(resp) {

                console.log(resp);

            }

        });
    });
});




//Finds the form with name:add_new_building_form, when submitted it run this function
$("form[name='add_new_building_form']").submit(function(e) {
    
    //Prevents the page reloading
    e.preventDefault();

    //Stores the form object
    var $form = $(this);

    //Finds the error class to display error messages
    var $error = $form.find(".error");

    //Collects the data submitted from the form to be sent to the server as a POST request
    var data = $form.serialize();

    //AJAX requests are sent to the backend
    $.ajax({

        //Sends the request to the route which handles skill updates
        url: "/user/add_building",

        //POST request
        type: "POST",

        //Sends the form data
        data: data,

        //Expecting a json response
        dataType: "json",

        //If the response is succesfull
        success: function(resp) {

            //Logs the servers response in the console
            console.log("Full Response from Server:", resp);

            let new_building = resp.new_building;

            if (!new_building) {
                console.error("new_building is undefined in response!");
                return;
            }


            console.log("New Building Name:", new_building.name); // Debugging

            //Setting the building name in the modal
            $("#new_building_name").text(new_building.name);

            //Populate the travel time form for the new building
            generate_travel_time_inputs(new_building._id, new_building.name);


            //Open the travel time modal
            $("#travel_time_modal").css("display", "block");


            //Success Message
            $error.text("Successful Update!").removeClass("error--hidden").addClass("success");

            
        },

        error: function(resp) {

            //Logs the error response in the browser console
            console.log(resp);
            $error.text("Error adding building").removeClass("error--hidden");

        }
    });

});



function generate_travel_time_inputs(new_building_id, new_building_name) {
    let inputFields = "";

    // Loop over all existing buildings to generate input fields for each
    buildings.forEach(building => {
        inputFields += `
            <label for="travel_${building._id}">Travel time from ${new_building_name} to ${building.name} (minutes):</label>
            <input type="number" name="travel_time[${new_building_id}][${building._id}]" min="1" required>
        `;
    });

    // Insert the generated input fields into the modal form
    $("#travel_time_inputs").html(inputFields);
}




//Finds the form with name:add_new_building_form, when submitted it run this function
$("form[name='remove_building_form']").submit(function(e) {
    
    //Prevents the page reloading
    e.preventDefault();

    //Stores the form object
    var $form = $(this);

    //Finds the error class to display error messages
    var $error = $form.find(".error");

    //Collects the data submitted from the form to be sent to the server as a POST request
    var data = $form.serialize();

    //AJAX requests are sent to the backend
    $.ajax({

        //Sends the request to the route which handles skill updates
        url: "/user/remove_building",

        //POST request
        type: "POST",

        //Sends the form data
        data: data,

        //Expecting a json response
        dataType: "json",

        //If the response is succesfull
        success: function(resp) {

            //Logs the servers response in the console
            console.log(resp);
            
            $error.text("Successful Update!").removeClass("error--hidden").addClass("success");
        },

        error: function(resp) {

            //Logs the error response in the browser console
            console.log(resp);

            //This will look at our models.py file and return the appropriate error message
           // $error.text(resp.responseJSON.error).removeClass("error--hidden"); 
        }
    });

});







//Finds the form with name:add_new_building_form, when submitted it run this function
$("form#travel_time_form").submit(function(e) {
    
    //Prevents the page reloading
    e.preventDefault();

    //Stores the form object
    var $form = $(this);

    //Finds the error class to display error messages
    var $error = $form.find(".error");

    //Collects the data submitted from the form to be sent to the server as a POST request
    var data = $form.serialize();

    //AJAX requests are sent to the backend
    $.ajax({

        //Sends the request to the route which handles skill updates
        url: "/user/set_travel_time",

        //POST request
        type: "POST",

        //Sends the form data
        data: data,

        //Expecting a json response
        dataType: "json",

        //If the response is succesfull
        success: function(resp) {

            //Logs the servers response in the console
            console.log(resp);
            
            $error.text("Successful Update!").removeClass("error--hidden").addClass("success");
        },

        error: function(resp) {

            //Logs the error response in the browser console
            console.log(resp);

        }
    });

});


//Finds the form with name:add_new_building_form, when submitted it run this function
$("form#request_support_form").submit(function(e) {
    
    //Prevents the page reloading
    e.preventDefault();

    //Stores the form object
    var $form = $(this);

    //Finds the error class to display error messages
    var $error = $form.find(".error");

    //Collects the data submitted from the form to be sent to the server as a POST request
    var data = $form.serialize();

    //AJAX requests are sent to the backend
    $.ajax({

        //Sends the request to the route which handles skill updates
        url: "/user/request_support",

        //POST request
        type: "POST",

        //Sends the form data
        data: data,

        //Expecting a json response
        dataType: "json",

        //If the response is succesfull
        success: function(resp) {

            //Logs the servers response in the console
            console.log(resp);
            
            $error.text("Successful Update!").removeClass("error--hidden").addClass("success");
        },

        error: function(resp) {

            //Logs the error response in the browser console
            console.log(resp);
            
        }
    });

});



//Finds the form with name:add_new_building_form, when submitted it run this function
$("form[name='set_mode_form']").submit(function(e) {
    
    //Prevents the page reloading
    e.preventDefault();

    //Stores the form object
    var $form = $(this);

    //Finds the error class to display error messages
    var $error = $form.find(".error");

    //Collects the data submitted from the form to be sent to the server as a POST request
    var data = $form.serialize();

    //AJAX requests are sent to the backend
    $.ajax({

        //Sends the request to the route which handles skill updates
        url: "/user/set_mode",

        //POST request
        type: "POST",

        //Sends the form data
        data: data,

        //Expecting a json response
        dataType: "json",

        //If the response is succesfull
        success: function(resp) {

            //Logs the servers response in the console
            console.log(resp);
            
            $error.text("Successful Update!").removeClass("error--hidden").addClass("success");
        },

        error: function(resp) {

            //Logs the error response in the browser console
            console.log(resp);

            //This will look at our models.py file and return the appropriate error message
           // $error.text(resp.responseJSON.error).removeClass("error--hidden"); 
        }
    });

});



//For admin_approval_form
$(document).ready(function () {

    //Variable for storing the action (approve/deny)
    let action = ""; 

    //Capture clicked button
    $("button[name='action']").click(function () {
        //Store button value
        action = $(this).val(); 
    });

    $("form[name='admin_approval_form']").submit(function (e) {

        //Prevent page from reloading
        e.preventDefault(); 

        var $form = $(this);
        var $error = $form.find(".error");

        // Serialize form data as an array
        var data = $form.serializeArray();


        //Add action to form data
        data.push({ name: "action", value: action });

        console.log("Sending Data:", data); // Debugging

        // AJAX request
        $.ajax({
            url: "/user/manage_pending_shift",
            type: "POST",
            data: data, 
            dataType: "json",
            success: function (resp) {
                console.log(resp);
                $error.text("Successful Update!").removeClass("error--hidden").addClass("success");
            },
            error: function (resp) {
                console.log(resp);
            }
        });
    });
});
