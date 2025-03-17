

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
