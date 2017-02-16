function Select(tableRow)
{
       tableRow.style.backgroundColor = 'rgba(' + [34,34,51, 0.2].join(',') + ')';
}

function Diselect(tableRow)
{
       tableRow.style.backgroundColor = 'rgb(' + [255,255,255].join(',') + ')';
}


function Click(tableRow, href)
{       
        Diselect(tableRow);
        window.location.href = href;
}
