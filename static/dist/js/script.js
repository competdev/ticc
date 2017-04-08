$(document).ready(function(){

    $.datetimepicker.setLocale('pt-BR');

    $('[widget=time]').mask('00:00');

    $('[widget=date]').datetimepicker({
        timepicker: false,
        format: 'd/m/Y'
    });

    rangeData();

    var trial = {
        'date': $('table tr:nth-child(1) td:nth-child(2)').html(),
        'time': $('table tr:nth-child(2) td:nth-child(2)').html(),
        'location': $('table tr:nth-child(3) td:nth-child(2)').html(),
        'responsible': $('table tr:nth-child(4) td:nth-child(2)').html(),
    }

    $('input[type=checkbox]').iCheck({
        checkboxClass: 'icheckbox_minimal',
        radioClass: 'iradio_minimal',
        increaseArea: '20%'
    });
});

var rangeData = function(){
    // "dd/mm/yyyy" to "yyyy/mm/dd"
    var dmy2ymd = function(str){
        return str.split('/').reverse().join('/')
    }

    var start = $("#id_start[widget=date]");
    var end = $("#id_end[widget=date]")

    $(start).datetimepicker('destroy');
    $(end).datetimepicker('destroy');

    $(function(){
        $(start).datetimepicker({
            timepicker: false,
            format: 'd/m/Y',
            mask: false,
            onShow: function( ct ){
                this.setOptions({
                    maxDate: $(end).val() ? dmy2ymd($(end).val()) : false
                })
            }
        });

        $(end).datetimepicker({
            timepicker: false,
            format: 'd/m/Y',
            mask: false,
            onShow:function( ct ){
                this.setOptions({
                    minDate: $(start).val() ? dmy2ymd($(start).val()) : false
                })
            }
        });
    });
}
