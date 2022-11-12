function validate() {
    var username = document.getElementById("exampleInputEmail1").value;
    var password = document.getElementById("exampleInputPasword1").value;

    if (username == "tony@savvly.com" && password == "Cocoon!") {
        alert("Login successfully, you will be redirected.");
        sessionStorage.setItem('status', 'loggedIn')
        window.location = "home.html"; // Redirecting to other page.
    }else{
        alert("Error incorrect credentials, try again.");
        return false;
    }

}