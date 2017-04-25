var currentTeams = [];

$(document).ready(function() {
    $('select#id_teams').hide();

    var allTeamsTable = $('#all-teams-table').DataTable({
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.13/i18n/Portuguese-Brasil.json'
        }    
    });
    var currentTeamsTable = $('#current-teams-table').DataTable({
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.13/i18n/Portuguese-Brasil.json'
        },
        searching: false,
        paging: false
    });

    $('#current-teams-table tbody').on('click', '.remove-btn', function() {
        var data = currentTeamsTable.row($(this).parents('tr')).data();

        var button = '<td><button type="button" class="btn btn-xs btn-primary add-btn">Adicionar</button></td>';
        data.splice(data.length - 1, 1, button);
        allTeamsTable.row.add(data)

        currentTeamsTable.row($(this).parents('tr')).remove();
        currentTeamsTable.draw();
        allTeamsTable.draw();

        currentTeams.splice(currentTeams.indexOf(data[0]), 1);
    });

    $('#all-teams-table tbody').on('click', '.add-btn', function() {
        var data = allTeamsTable.row($(this).parents('tr')).data();

        var button = '<td><button type="button" class="btn btn-xs btn-danger remove-btn">Remover</button></td>';
        data.splice(data.length - 1, 1, button);
        currentTeamsTable.row.add(data)

        allTeamsTable.row($(this).parents('tr')).remove();
        allTeamsTable.draw();
        currentTeamsTable.draw();

        currentTeams.splice(0, 0, data[0]);
    });

    currentTeamsTable.rows().every(function() {
        currentTeams.push(this.data()[0]);
    });

    $('form').submit(function() {
        $('select#id_teams').val(currentTeams);
    });
});
