$(function () {

    $(".select2").select2();

    $("#datemask").inputmask("dd/mm/yyyy", {"placeholder": "dd/mm/yyyy"});
    $("[data-mask]").inputmask();

    $(".timepicker").timepicker({
      showInputs: false,
      showMeridian: false
    });

});
