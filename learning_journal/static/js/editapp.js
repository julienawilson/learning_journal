$(document).ready(function(){
    var button = $(".submit");
    button.on("click", function(e){
        e.preventDefault();
        var title = $(this).parent().find("input[name='title']")[0].value;
        var body = $(this).parent().find("textarea[name='body']")[0].value;
        $.ajax({
            url: '/journal/1',
            type: "POST",
            data:{
                "csrf_token": $(this).parent().find("input[name='csrf_token']")[0].value,
                "title": title,
                "body": body
            },
            success: function(){
               console.log('Post edited.')
            },
            error: function(err){
                console.error(err);
                alert("This is a problem", err.message);
            }
        });        
    });
});