
function Encender(){
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

function Apagar(){
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

function ActivarExperto(){
    $.ajax({
        url:"ActivarExperto",     
        dataType: 'json',
        type: 'GET',
        success: (response) => {
            console.log(response);
        }
     });
}