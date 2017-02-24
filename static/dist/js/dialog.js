function showDialog(message, link) {
	$('#edit').hide();
	$('#del').hide();
	$('#message').html(message);
	$('#link').attr('href', link);
}

function edit_or_delete(edit_href, del_href){
	$('.modal-title')
	.html('Escolha uma opção:')
	.attr({'align': 'center'});

	$('.modal-body').hide();

	$('#edit').attr({'href': edit_href, 'style': 'width:20%; margin-left: 110px'});
	$('#del').attr({'href': del_href, 'style': 'width:20%; margin-right: 110px'});

	$('#cancel').hide();
	$('#link').hide();
}

function datetime_and_judge(judge, date){
	$('.modal-title')
	.html('Detalhes da publicação:')
	.attr({'align': 'center'});

	var p = document.createElement("p");
	var t = document.createTextNode("Publicado por: " + judge);
	var t2 = document.createTextNode('Data: ' + date);
	p.append(t);

	var div = document.createElement("div");
	div.append(p);
	div.append(t2);

	$('#cancel').hide();
	$('#link').hide();
	$('#edit').hide();
	$('#del').hide();

	$('.modal-body').append(div);	
}

function atualiza(){
	location.reload();
}