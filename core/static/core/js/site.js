
var Encender = () => {
    $.ajax({
        url:"Encender",     
        data: { 'desc': "Todo bien" },
        dataType: 'json',
        type: 'GET',
        success: (response) => {
            console.log(response);
            var Respuesta = response;
            try {
                if (Respuesta.code == "OK") {
                    console.log(Respuesta.description);
                } else {
                    console.log(Respuesta.description);
                }
            } catch (ex) {
                console.log(ex);
            }
        }
     });
}

var Apagar = () =>{
    $.ajax({
        url:"Apagar",     
        data: { 'desc': "Todo bien" },
        dataType: 'json',
        type: 'GET',
        success: (response) => {
            console.log(response);
            var Respuesta = response;
            try {
                if (Respuesta.code == "OK") {
                    console.log(Respuesta.description);
                } else {
                    console.log(Respuesta.description);
                }
            } catch (ex) {
                console.log(ex);
            }
        }
     });
}