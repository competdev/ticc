function Select(tableRow)
{
       tableRow.style.backgroundColor = 'rgba(' + [34,34,51, 0.2].join(',') + ')';
}

function Diselect(tableRow)
{
       tableRow.style.backgroundColor = 'rgb(' + [255,255,255].join(',') + ')';
}


function Click(tableRow, bool, id)
{       
        Diselect(tableRow);
        if(bool)
            window.location.href = '/resultados/publica/' + $('#user').val() + '/'+id ;
        else  if (!bool)
            window.location.href = '/pontuacao/' + id ;
}