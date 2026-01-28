$(document).ready(function(){
    endpoint = location.protocol + "//" + location.host + "/api/3/action/";

    var active_view = $('li.active.view_item:first').data('id');

    $('#canonical, #homepage').click(function(){
        var el = $(this);
        canonical_or_homepage = el.attr('id');
        
        var data = {
            'resource_view_id': active_view,
        };
        data[canonical_or_homepage] = !el.hasClass('active')
        
        $.ajax({
            method: "POST",
            data: encodeURIComponent(JSON.stringify(data)),
            url: endpoint + 'featured_upsert',
        }).done(function(result){
            if (result['result'][canonical_or_homepage] === 'True' || result['result'][canonical_or_homepage] === true){
                el.addClass('active');
            } else {
                el.removeClass('active');
            }
            // Update canonical button text when toggled
            if (canonical_or_homepage === 'canonical') {
                var labelActive = el.data('label-active');
                var labelInactive = el.data('label-inactive');
                if (labelActive && labelInactive) {
                    el.text(result['result'][canonical_or_homepage] === 'True' || result['result'][canonical_or_homepage] === true
                        ? labelActive : labelInactive);
                }
            }
        });
    });
});
