var EstadoExperto = false;


function Encender(){
    $.ajax({
        url:"Encender",
        dataType: 'json',
        type: 'GET',
        success: (response) => {
            try {
                switch (response.code){
                    case 200:
                        EstadoExperto = true;
                        $("#CardESP").removeClass();
                        $("#CardESP").addClass("card mb-3 border-success");
                        $("#CardESP_Body").removeClass();
                        $("#CardESP_Body").addClass("card-body text-success");
                        $("#CardESP_Title").text("Encendido");
                        $("#CardESP_Text").text("El dispositivo esta encendido y consumiendo energia.");
                        break;
                    case 202:
                        EstadoExperto = true;
                        $("#CardESP").removeClass();
                        $("#CardESP").addClass("card mb-3 border-success");
                        $("#CardESP_Body").removeClass();
                        $("#CardESP_Body").addClass("card-body text-success");
                        $("#CardESP_Title").text("Ya encendido");
                        $("#CardESP_Text").text("El dispositivo ya esta encendido y consumiendo energia.");
                        break;                    
                    default:
                        EstadoExperto = false;
                        $("#CardESP").removeClass();
                        $("#CardESP").addClass("card mb-3 border-danger");
                        $("#CardESP_Body").removeClass();
                        $("#CardESP_Body").addClass("card-body text-danger");
                        $("#CardESP_Title").text("Ocurrio un error con el dispositivo");
                        $("#CardESP_Text").text(response.description);
                        console.log(response)
                        break;
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
        dataType: 'json',
        type: 'GET',
        success: (response) => {
            console.log(response);
            var Respuesta = response;
            try {
                switch (response.code){
                    case 200:
                        $("#CardESP").removeClass();
                        $("#CardESP").addClass("card mb-3 border-warning");
                        $("#CardESP_Body").removeClass();
                        $("#CardESP_Body").addClass("card-body text-warning");
                        $("#CardESP_Title").text("Apagado");
                        $("#CardESP_Text").text("El dispositivo esta en modo reposo, ahorrando un poco de energia.");
                        break;
                    case 202:
                        $("#CardESP").removeClass();
                        $("#CardESP").addClass("card mb-3 border-warning");
                        $("#CardESP_Body").removeClass();
                        $("#CardESP_Body").addClass("card-body text-warning");
                        $("#CardESP_Title").text("Ya en reposo");
                        $("#CardESP_Text").text("El dispositivo ya en reposo y ahorrando algo de energia.");
                        break;                    
                    default:
                        $("#CardESP").removeClass();
                        $("#CardESP").addClass("card mb-3 border-danger");
                        $("#CardESP_Body").removeClass();
                        $("#CardESP_Body").addClass("card-body text-danger");
                        $("#CardESP_Title").text("Ocurrio un error con el dispositivo");
                        $("#CardESP_Text").text(response.description);
                        console.log(response)
                        break;
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
            //cards
            $("#ConsumoDia").text(response.Hoy + " Kwh");
            $("#ConsumoMes").text(response.Mes + " Kwh");
            $("#ConsumoAyer").text(response.Ayer + " Kwh");
            $("#ConsumoMesPasado").text(response.MesPasado + " Kwh");

            //Sugerencias y notas
            if(parseFloat(response.Hoy) <= parseFloat(response.Ayer)){
                $("#CardDia").addClass("border-success");
                $("#CardDia_Body").removeClass();
                $("#CardDia_Body").addClass("card-body text-success");
                $("#CardDia_Title").text("¡BIEN!");
                $("#CardDia_Text").text("El consumo de hoy es menor que el registrado ayer, ¡mantenlo asi y ayuda al planeta!.");

                let consumo = (parseFloat(response.Ayer) - parseFloat(response.Hoy)) * 0.839;
                $("#Gasto1").addClass("list-group-item list-group-item-success");
                $("#Gasto1").text("Hoy llevas ahorrado " + consumo.toFixed(2) + "$ Mxn a comparación de ayer. Esto a la seman sería " + (consumo*7).toFixed(2) + "$ Mxn");

            }else{
                $("#CardDia").addClass("border-danger");
                $("#CardDia_Body").removeClass();
                $("#CardDia_Body").addClass("card-body text-danger");
                $("#CardDia_Title").text("¡CUIDADO!");
                $("#CardDia_Text").text("Tu consumo de hoy es mayor que el de ayer, deberias ahorrar energia es por un bien =)");

                let consumo = (parseFloat(response.Hoy) - parseFloat(response.Ayer)) * 0.839;
                $("#Gasto1").addClass("list-group-item list-group-item-warning");
                $("#Gasto1").text("Llevas " + consumo.toFixed(2) + "$ Mxn mas gastado a comparación de ayer.");
            }

            if(parseFloat(response.Mes) <= parseFloat(response.MesPasado)){
                $("#CardMes").addClass("border-success");
                $("#CardMes_Body").removeClass();
                $("#CardMes_Body").addClass("card-body text-success");
                $("#CardMes_Title").text("¡EXELENTE!");
                $("#CardMes_Text").text("El consumo de este mes aun es menor que el del mes pasado. ¡Felicidades!");

                let consumo = (parseFloat(response.MesPasado) - parseFloat(response.Mes)) * 0.839;
                $("#Gasto2").addClass("list-group-item list-group-item-success");
                $("#Gasto2").text("Hoy llevas gastado " + consumo.toFixed(2) + "$ Mxn a comparación del mes pasado. Mantenlo asi");
            }else{
                $("#CardMes").addClass("border-danger");
                $("#CardMes_Body").removeClass();
                $("#CardMes_Body").addClass("card-body text-danger");
                $("#CardMes_Title").text("¡PELIGRO!");
                $("#CardMes_Text").text("Tu consumo de este mes ya es mayor que el total del mes pasado, reducelo para ganar un ahorro de energia.");

                let consumo = (parseFloat(response.Mes) - parseFloat(response.MesPasado)) * 0.839;
                $("#Gasto2").addClass("list-group-item list-group-item-warning");
                $("#Gasto2").text("Llevas " + consumo.toFixed(2) + "$ Mxn mas gastado a comparación del mes pasado, esto afecta a tu bolsillo.");
            }


            //Chart Dia
            var ListLabels = [];
            var Data = [];
            $.each(response.Facts, function (index, item) {
                ListLabels.push(item.hora + " Hrs.");
                Data.push(item.Kwh);
            });

            var ctx = document.getElementById('ChartDia').getContext('2d');
            var Chartctx = new Chart(ctx, {
                type: 'line',
                data: {
                  labels: ListLabels,
                  datasets: [{
                    label: 'Consumo de Kwh',
                    data: Data,
                    backgroundColor: 'rgba(255, 99, 132, 0.6)',
                    borderColor: 'rgba(54, 162, 235, 0.6)',
                    fill: false,
					borderWidth: 3,
					pointStyle: 'rectRot',
					pointRadius: 10,
					pointBorderColor: 'rgb(0, 0, 0)'
                  }]
                },
                options: {
					responsive: true,
                    legend: {
                        labels: {
                             fontColor: 'orange'
                            }
                         },
                   title: {
                       display: false,
                       fontColor: 'white',
                       text: 'Consumo'
                   }     ,
                   scales: {
                       yAxes: [{
                           ticks: {
                               beginAtZero:true,
                               fontColor: 'white'
                           },
                       }],
                     xAxes: [{
                           ticks: {
                               fontColor: 'white'
                           },
                       }]
                   } 
				}
              });
            
            //CharSemana
            ListLabels = [];
            Data = [];
            $.each(response.FactsSemana, function (index, item) {
                ListLabels.push(item.anio + "-" + item.mes + "-" + item.dia);
                Data.push(item.Kwh);
            });

            var ctx = document.getElementById('ChartSemana').getContext('2d');
            var Chartctx = new Chart(ctx, {
                type: 'horizontalBar',
                data: {
                  labels: ListLabels,
                  datasets: [{
                    label: 'Consumo de Kwh',
                    data: Data,
                    backgroundColor: [
                        'rgba(240, 113, 248, 0.5)',
                        'rgba(230, 248, 113 , 0.5)',
                        'rgba(207, 113, 49, 0.5)',
                        'rgba(255, 99, 132, 0.5)',
                        'rgba(200, 207, 49, 0.5)',
                        'rgba(217, 71, 24, 0.5)',
                        'rgba(24, 217, 82, 0.5)',
                    ],
                    borderColor: 'rgba(54, 162, 235, 0.6)',
                    borderWidth: 5
                  }]
                },
                options: {
					responsive: true,
                    legend: {
                        labels: {
                             fontColor: 'orange'
                            }
                         },
                   title: {
                       display: false,
                       fontColor: 'white',
                       text: 'Consumo'
                   }     ,
                   scales: {
                       yAxes: [{
                           ticks: {
                               beginAtZero:true,
                               fontColor: 'white'
                           },
                       }],
                     xAxes: [{
                           ticks: {
                               fontColor: 'white'
                           },
                       }]
                   } 
				}
              });
        }
    });
}

function Estado(Cambio){
    $.ajax({
        url:"Estado",
        dataType: 'json',
        data: {'cambio': Cambio},
        type: 'GET',
        success: (response) => {
            try {
                switch (response.code){
                    case 200:
                        $("#CardESP").removeClass();
                        $("#CardESP").addClass("card mb-3 border-success");
                        $("#CardESP_Body").removeClass();
                        $("#CardESP_Body").addClass("card-body text-success");
                        $("#CardESP_Title").text("Encendido");
                        $("#CardESP_Text").text("El dispositivo esta encendido y consumiendo energia.");
                        break;
                    case 202:
                        $("#CardESP").removeClass();
                        $("#CardESP").addClass("card mb-3 border-warning");
                        $("#CardESP_Body").removeClass();
                        $("#CardESP_Body").addClass("card-body text-warning");
                        $("#CardESP_Title").text("Apagado");
                        $("#CardESP_Text").text("El dispositivo esta en modo reposo, ahorrando un poco de energia.");
                        break;                    
                    default:
                        $("#CardESP").removeClass();
                        $("#CardESP").addClass("card mb-3 border-danger");
                        $("#CardESP_Body").removeClass();
                        $("#CardESP_Body").addClass("card-body text-danger");
                        $("#CardESP_Title").text("Ocurrio un error con el dispositivo, no se pudo conectar.");
                        $("#CardESP_Text").text(response.description);
                        console.log(response)
                        break;
                }
                switch (response.autonomia){
                    case true:
                        $("#CardHoras").removeClass();
                        $("#CardHoras").addClass("card mb-3 border-success");
                        $("#CardHoras_Title").removeClass();
                        $("#CardHoras_Title").addClass("card-title text-success");
                        $("#CardHoras_Title").text("Autonomia activada");
                        $("#CardHoras_Horas").removeClass();
                        $("#CardHoras_Horas").addClass("card-text text-success");
                        $("#CardHoras_Horas").text("Horas de reposo: " + response.horaInicio + " - " + response.horaFin + " Hrs.");
                        $("#CardHoras_Button").removeClass();
                        $("#CardHoras_Button").addClass("btn btn-block btn-lg btn-danger mb-3");
                        $("#CardHoras_Button").text("Desactivar autonomia");

                        break;
                    case false:
                        $("#CardHoras").removeClass();
                        $("#CardHoras").addClass("card mb-3 border-danger");
                        $("#CardHoras_Title").removeClass();
                        $("#CardHoras_Title").addClass("card-title text-danger");
                        $("#CardHoras_Title").text("Autonomia desactivada");
                        $("#CardHoras_Horas").removeClass();
                        $("#CardHoras_Horas").addClass("card-text text-danger");
                        $("#CardHoras_Horas").text("Horas de reposo: " + response.horaInicio + " - " + response.horaFin + " Hrs. (No activado)");
                        $("#CardHoras_Button").removeClass();
                        $("#CardHoras_Button").addClass("btn btn-block btn-lg btn-success mb-3");
                        $("#CardHoras_Button").text("Activar autonomia");
                        break;
                    default:
                        break;
                }

            } catch (ex) {
                console.log(ex);
            }
        }
     });  
}