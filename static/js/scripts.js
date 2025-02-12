//Find the form called register_form, when it is submitted run this function

$("form[name='register_form']").submit(function(e) {
    e.preventDefault();

    var $form = $(this);
    var $error = $form.find(".error");
    //Collects the data submitted from the form
    var data = $form.serialize();

    $.ajax({
        url: "/user/register",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            console.log(resp);
            $error.text("Registration successful!").removeClass("error--hidden").addClass("success");
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden"); //This will look at our models.py file and return the appropriate error message
        }
    });

    
});