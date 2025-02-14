

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

            //This redirects to another page
            //window.location.href = "/ta/";
            
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

        //Sends the request to the route which handles registration
        url: "/user/login",

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