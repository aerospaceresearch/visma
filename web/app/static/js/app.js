$(document).ready(function() {
    var x = document.getElementById("visma_btn")
    if(x.style.display !== "none") {
        x.style.display = "none";
    }
})

// Get a value expression
function getExpr() {
    // alert("here")
    var url = 'http://127.0.0.1:5000/simplify/posts';
    var d = document.getElementById("user_input").value;
    
    var data = {'expr':d}
    console.log("data is being sent");
    $.post({
        url,
        data,
        function (data,status) {
            console.log(`${data} and status is ${status}` );  
        }
    });
    document.getElementById('simplify').href = "{{ url_for('index') }}"
    hideButton();
}

function getValue() {
    console.log("getting value");
    // var v = $(this).val();
    // console.log(v);
    // document.getElementById('user_input').innerHTML = document.getElementById('user_input')
}

$(".input_expr").click(function() {
    var input_val = $(this).val();
    console.log(input_val);
    
    document.getElementById("user_input").value = document.getElementById('user_input').value + input_val
});

function showButton() {
    var x = document.getElementById("visma_btn");
    console.log("show");
    if(x.style.display === "none") {
        x.style.display = "block";
    }
}

function hideButton() {
    var x = document.getElementById("visma_btn");
    var ui = document.getElementById("user_input").value;
    console.log("hide");
    if(x.style.display !== "none") {
        x.style.display = "none";
    }
}