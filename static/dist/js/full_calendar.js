// Js para criar e configurar o FullCalendar
$(document).ready(function() { // Inicializa com JQuery.
   	// É necessário esperar o arquivo completo carregar para começar a mexer
    var tournamentsArray = []; // Somente inicializa um vetor para armazenar os torneios
    for(i in tournamentsData){
    	tournamentsArray.push({'start' : tournamentsData[i][0], 'end': tournamentsData[i][1],     //Essas proximas 3 linhas são para adicionar
    		'title': 'Torneio no Campus '+ tournamentsData[i][2] + ' - ' +tournamentsData[i][3],  //os torneios no vetor
    		'textColor': 'black','color' : '#33cc33'});
    	//tournamentsArray.push({'start' : tournamentsData[i][0], 'end': tournamentsData[i][1], 'title': 'Torneio no Campus '+ tournamentsData[i][2] + ' - ' +tournamentsData[i][3], 'color' : '#'+Math.floor(Math.random()*16777215).toString(16)});
    	// A linha acima substitui a acima dela . A diferença é que sempre as cores serão cores aleatorias
    	// e o de baixo sempre terá as cores fixas
    }

    // As variaveis são pegas do home.html na linha 7.
    $('#calendar').fullCalendar({ // Aqui é inicializado o calendario e configurado algumas de suas especificações
        header: {	// configura o que ficará no header nas posicoes citadas
	        left: 'title',
	  		center: 'pt-br',
	    	right:  'today, prev,next'
	    },
	    locale: 'pt-br', // Colocada a lingua brasileira
		height: 500, // fixa o tamanho do calendario
		events: tournamentsArray //Pega o Array preenchido acima e coloca ele nos eventos do calendário
    })
});


// !!!!!!!!! Lembrar de olhar a parte do GOOGLE no FULL CALENDAR para configuração correta !!!!!!!!!!!!!