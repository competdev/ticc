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
/*
function tableCreate() {
    var body = document.getElementById('teste');
    var tbl = document.createElement('table');
    tbl.style.width = '100%';
    tbl.className = 'table';
    var tbdy = document.createElement('tbody');
    for (var i = 0; i < 3; i++) {
        var tr = document.createElement('tr');
        for (var j = 0; j < 2; j++) {
            if (i == 2 && j == 1) {
                break
            } else {
                var td = document.createElement('td');
                td.appendChild(document.createTextNode('olaaaaaa'))
                i == 1 && j == 1 ? td.setAttribute('rowSpan', '2') : null;
                tr.appendChild(td)
            }
        }
        tbdy.appendChild(tr);
    }
    tbl.appendChild(tbdy);
    body.appendChild(tbl)
    alert(body);
}
*/