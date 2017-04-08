var currentMembers = [];

$(document).ready(function() {
    $('select#id_members').hide();

    var participantsTable = $('#participants-table').DataTable({
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.13/i18n/Portuguese-Brasil.json'
        }    
    });
    var membersTable = $('#members-table').DataTable({
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.13/i18n/Portuguese-Brasil.json'
        },
        searching: false,
        paging: false
    });

    $('#participants-table tbody').on('click', '.add-btn', function() {
        var data = participantsTable.row($(this).parents('tr')).data();

        var button = '<td><button type="button" class="btn btn-xs btn-danger remove-btn">Remover</button></td>';
        data.splice(data.length - 1, 1, button);
        membersTable.row.add(data)

        participantsTable.row($(this).parents('tr')).remove();
        participantsTable.draw();
        membersTable.draw();

        currentMembers.splice(0, 0, data[0]);
    });

    $('#members-table tbody').on('click', '.remove-btn', function() {
        var data = membersTable.row($(this).parents('tr')).data();

        var button = '<td><button type="button" class="btn btn-xs btn-primary add-btn">Adicionar</button></td>';
        data.splice(data.length - 1, 1, button);
        participantsTable.row.add(data)

        membersTable.row($(this).parents('tr')).remove();
        membersTable.draw();
        participantsTable.draw();

        currentMembers.splice(currentMembers.indexOf(data[0]), 1);
    });

    membersTable.rows().every(function() {
        currentMembers.push(this.data()[0]);
    });

    $('form').submit(function() {
        $('select#id_members').val(currentMembers);
    });
});
