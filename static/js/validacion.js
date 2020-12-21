function validar_formulario(){
    var nombre = document.getElementById("nombre").value;
    var correo = document.getElementById("correo").value;
    var usuario = document.getElementById("usuario").value;
    var clave = document.getElementById("clave").value;
    var conf_clave = document.getElementById("conf_clave").value;
    if (nombre == ""){
        alert("Debe digitar un nombre.");
        document.getElementById("nombre").focus();
        return false;
    } 

    if ((usuario == "") || (usuario.length < 8)){
        alert("El usuario debe tener mínimo 8 caracteres.");
        document.getElementById("usuario").focus();
        return false;
    }

    if (correo == ""){
        alert("Debe digitar el correo.");
        document.getElementById("correo").focus();
        return false;
    } 
        
    if ((clave == "") || (clave.length < 8)){
        alert("La clave debe tener mínimo 8 caracteres.");
        document.getElementById("clave").focus();
        return false;
    }

    if (conf_clave == ""){
        alert("Debe digitar el correo.");
        document.getElementById("conf_clave").focus();
        return false;
    }
    if (clave!=conf_clave){
        alert("La contraseña es incorrecta, digite de nuevo una")
        document.getElementById("clave").focus()
    }
}

