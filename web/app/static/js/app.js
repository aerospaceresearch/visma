$(document).ready(function() {
    var x = document.getElementById("visma_btn")
    if(x.style.display !== "none") {
        x.style.display = "none";
    }
})

// Get expression value
function getExpr(type_of_operation) {
    console.log(type_of_operation);
    var url = `http://127.0.0.1:5000/${type_of_operation}/posts`;
    var d = document.getElementById("user_input").value;

    // Checking number is negative for not for Factorial
    var check_negative_num = parseInt(d, 10);
    if(type_of_operation==="factorial" && check_negative_num < 0) {
            alert('Factorial is not defined for negative numbers');
    }

    else {
        var data = {'expr':d}
        console.log("data is being sent");
        $.post({
            url,
            data,
            success: function (data,status) {
                console.log(status);
                console.log(`${data} and status is ${status}` );  
                document.getElementById('user_input').value = data
            },
            error: function() {
                alert('It seems that something is wrong in your Input')
            }
        });
        hideButton();
    }
}

$(".input_expr").click(function() {
    var input_val = $(this).val();
    // console.log(input_val);
    if(input_val == 'del') {
        input_box_val = document.getElementById("user_input").value;
        input_box_val_size = input_box_val.length;
        // console.log(input_box_val);
        document.getElementById("user_input").value = input_box_val.slice(0,input_box_val_size-1);
    }
    else if(input_val == "clear") {
        document.getElementById("user_input").value = "";
    }
    else {
        document.getElementById("user_input").value = document.getElementById('user_input').value + input_val
    }
});

function showButton() {
    var x = document.getElementById("visma_btn");
    console.log("show");
    input_val = document.getElementById('user_input').value;
    if(input_val === "") {
        alert('Please Provide a Input')
    }
    
    else if(x.style.display === "none") {
        x.style.display = "block";
    }
}

function hideButton() {
    var x = document.getElementById("visma_btn");
    console.log("hide");
    if(x.style.display !== "none") {
        x.style.display = "none";
    }
}