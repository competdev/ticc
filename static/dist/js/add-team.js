$(document).ready(function() {
    $('#id_participants').wrap('<span></span>').hide();
    var year;
    var select = $('#id_participants');
    $('#1-year').click(function(){
        $('#id_participants').wrap('<span></span>').show();
        year = $(this).attr('name');
        $.get('equipes/filtro_participantes',{year:year}, function(data){
            $('#id_participants option').remove();
            console.log(data)
            list = data.split('|')
            $.each(list,function(index,value){
                element = list[index].split(',')
                select.append($('<option></option>').attr('value',element[1]).text(element[0]));
            });
        });
    });
    $('#2-year').click(function(){
        $('#id_participants').wrap('<span></span>').show();
        year = $(this).attr('name')
        $.get('equipes/filtro_participantes',{year:year}, function(data){
            $('#id_participants option').remove();
            list = data.split('|')
            $.each(list,function(index,value){
                element = list[index].split(',')
                select.append($('<option></option>').attr('value',element[1]).text(element[0]));
            });
        });
    });
    $('#3-year').click(function(){
        $('#id_participants').wrap('<span></span>').show();
        year = $(this).attr('name')
        $.get('equipes/filtro_participantes',{year:year}, function(data){
            $('#id_participants option').remove();
            list = data.split('|')
            $.each(list,function(index,value){
                element = list[index].split(',')
                select.append($('<option></option>').attr('value',element[1]).text(element[0]));
            });
        });
    });
    $('#mix').click(function(){
        $('#id_participants').wrap('<span></span>').show();
        year = $(this).attr('name')
        $.get('equipes/filtro_participantes',{year:year}, function(data){
            $('#id_participants option').remove();
            list = data.split('|')
            $.each(list,function(index,value){
                element = list[index].split(',')
                select.append($('<option></option>').attr('value',element[1]).text(element[0]));
            });
        });
    });
});