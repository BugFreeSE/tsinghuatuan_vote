/**
 * Created by 王宇炜 on 2014/11/25.
 */

function showSuccess()
{
    $('#setting').hide();
    $('#successHolder').show();
}

function submitSetting()
{
    var options = {
        url: "/u/setting/try/",
        success: showSuccess
    }
    $('#setting_context').ajaxSubmit(options);
}


