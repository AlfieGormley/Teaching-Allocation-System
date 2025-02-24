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


//Finds the form with name:remove_skills_form, when submitted it run this function
$("form[name='availability_form']").submit(function(e) {
    
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
        url: "/user/set_availability",

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
