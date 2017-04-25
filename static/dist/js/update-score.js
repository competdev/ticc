// $(function() {
//     var table = $('.datatables').DataTable({
//         buttons: [
//             {
//                 extend: 'print',
//                 autoPrint: false,
//                 className: 'btn-box-tool',
//                 text: '<span class="glyphicon glyphicon-print">',
//                 title: 'Seletiva - Participantes',
//                 message: 
//                         '<p><strong>Data: </strong>'+trial.date+'</p> \
//                         <p><strong>Horário: </strong>'+trial.time+'</p> \
//                         <p><strong>Local: </strong>'+trial.location+'</p> \
//                         <p><strong>Responsável: </strong>'+trial.responsible+'</p>',
//                 customize: function(win) 
//                 {   
//                     $(win.document.body)
//                         .addClass('container');
//                     $(win.document.body).find('table')
//                         .addClass('table-bordered'); 
//                     columns = $('.datatables > tbody').find('> tr:first > td').length;
//                     for (var i = columns; i > 2; i--) {
//                         $(win.document.body).find('table tr th:nth-child('+i+'), table tr td:nth-child('+i+')')
//                             .hide();
//                     }    
//                 }
//             },
//         ],
//         paging: false,
//         ordering: true,
//         info: false,
//         autoWidth: false,
//         language: {
//             emptyTable: 'Nenhum objeto encontrado',
//             search: 'Buscar'
//         }
//     });

//     table.on( 'order.dt search.dt', function () {
//         table.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
//             cell.innerHTML = i+1;
//         } );
//     }).draw();

//     table.buttons().container()
//         .appendTo(
//             $('.datatables').closest('.box').find('.box-tools')
//         );
//     $('.buttons-print').removeClass('btn-default');
// });
