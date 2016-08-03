var table;

$(function () {
    table = $('#participantes-table').DataTable({
        'paging': false,
        'lengthChange': false,
        'searching': true,
        'ordering': true,
        'info': true,
        'autoWidth': false,
        'language': {
            'decimal':        ',',
            'emptyTable':     'Nenhum dado encontrado',
            'info':           '',
            'infoEmpty':      '',
            'infoFiltered':   '',
            'infoPostFix':    '',
            'thousands':      '.',
            'lengthMenu':     'Mostrando _MENU_ itens',
            'loadingRecords': 'Carregando...',
            'processing':     'Processando...',
            'search':         'Buscar:   ',
            'zeroRecords':    'Nenhum dado encontrado',
            'paginate': {
                'first':      'Primeiro',
                'last':       'Último',
                'next':       'Próximo',
                'previous':   'Anterior'
            }
        },
        'aria': {
            'sortAscending':  ': activate to sort column ascending',
            'sortDescending': ': activate to sort column descending'
        }
    });
});

$('#update').click( function() {
    var data = table.$('input, select').serialize();
    alert(
        "The following data would have been submitted to the server: \n\n"+
        data
    );
    return false;
} );
