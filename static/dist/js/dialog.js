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