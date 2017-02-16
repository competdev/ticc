function showDialog(message, link) {
	$('#message').html(message);
	$('#link').attr('href', link);
}

function edit_or_delete(edit_href, delete_href){

	var edit = $(document.createElement('a'))
	.attr({'href':edit_href,'class': 'btn btn-warning pull-left', 'style': 'width: 20%; margin-left: 110px'})
	.html('Editar');

	var del = $(document.createElement('a'))
	.attr({'href':delete_href ,'class': 'btn btn-danger pull-left', 'style': 'width: 20%; margin-left: 130px'})
	.html('Excluir');

	$('.modal-title')
	.html('Escolha uma opção:')
	.attr({'align': 'center'});

	$('#cancel').hide();
	$('a').hide();
	$('#link').attr('href', '/resultados');
	$('.modal-body').append(edit, del);
}