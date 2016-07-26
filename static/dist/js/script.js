// $(function(){
//     $(".box").hide().each(function(i) {
//         $(this).delay(i*600).fadeIn(600);
//     });
// });

$(document).ready(function(){

    $.datetimepicker.setLocale('pt-BR');

    $('[widget=time]').datetimepicker({
        datepicker: false,
        mask: true,
        format: 'H:i'
    });

    $('[widget=date]').datetimepicker({
        timepicker: false,
        mask: true,
        format: 'd/m/Y'
    });

    rangeData();

    $('.datatables').DataTable({
        paging: false,
        ordering: true,
        info: false,
        language: {
            emptyTable: 'Nenhum participante encontrado',
            search: 'Buscar'
        },
        order: [
            [2, 'desc'],
            [3, 'asc']
        ]
    });
})


var rangeData = function(){
    // "dd/mm/yyyy" to "yyyy/mm/dd"
    var dmy2ymd = function(str){
        return str.split('/').reverse().join('/')
    }

    $("#id_inicio").datetimepicker('destroy');
    $("#id_termino").datetimepicker('destroy');

    $(function(){
        $("#id_inicio").datetimepicker({
            timepicker: false,
            format: 'd/m/Y',
            onShow: function( ct ){
                this.setOptions({
                    maxDate: $("#id_termino").val() ? dmy2ymd($("#id_termino").val()) : false
                })
            }
        });

        $("#id_termino").datetimepicker({
            timepicker: false,
            format: 'd/m/Y',
            onShow:function( ct ){
                this.setOptions({
                    minDate: $("#id_inicio").val() ? dmy2ymd($("#id_inicio").val()) : false
                })
            }
        });
    });
}