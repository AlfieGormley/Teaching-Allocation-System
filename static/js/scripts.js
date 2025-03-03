//Using AJAXs means we can submit form data to the server without the need for a page refresh

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


//Java script for a TA to update their skill set


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




$(document).ready(function() {
    console.log("Document ready - Checking for Date Range Picker...");

    if ($('form[name="availability_form"]').length) {
        console.log("Initializing Date Range Picker on ta.html");

        $('input[name="datetimes"]').daterangepicker({
            timePicker: true,
            startDate: moment().startOf('hour'),
            endDate: moment().startOf('hour').add(32, 'hour'),
            locale: { format: 'M/DD hh:mm A' }
        });

        //Listen for apply event
        $('input[name="datetimes"]').on('apply.daterangepicker', function(ev, picker) {
            console.log("Date Range Selected:", picker.startDate.format('YYYY-MM-DD HH:mm'), "to", picker.endDate.format('YYYY-MM-DD HH:mm'));

            // Prepare the data to send
            var formData = {
                start_date: picker.startDate.format('YYYY-MM-DD HH:mm'),
                end_date: picker.endDate.format('YYYY-MM-DD HH:mm')
            };

            
            // Send data to the backend via AJAX
            $.ajax({
                url: "/user/set_availability",  
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify(formData),  // Convert to JSON
                dataType: "json",
                success: function(response) {
                    console.log("Server Response:", response);
                    //alert("Availability data received successfully!");
                },
                error: function(error) {
                    console.error("Error sending data:", error);
                    //alert("An error occurred while sending data.");
                }
            });
        });

    } 
});
