$(document).ready(function(){
    var button = $(".submit");
    button.on("click", function(e){
        e.preventDefault();
        var title = $(this).parent().find("input[name='title']")[0].value;
        var body = $(this).parent().find("textarea[name='body']")[0].value;
        $.ajax({
            url: '/',
            type: "POST",
            data:{
                "csrf_token": $(this).parent().find("input[name='csrf_token']")[0].value,
                "title": title,
                "body": body
            },
            success: function(){
                var href = $('h2 a').attr('href').split('/').slice(1);
                var new_post_id = Number(href[1]) + 1;
                var new_post_href = href[0] + '/' + new_post_id.toString();
                post_template = '<h2><a href="' + new_post_href + '">' + title + '</a></h2>'+
                    '<p class="lead">by <a href="/about_me">Julien Wilson</a></p>'+
                    '<p><span class="glyphicon glyphicon-time"></span> Posted Just Now</p>'+
                    '<br/>'
                $('#posts').prepend(post_template);
                $('form')[0].reset();
            },
            error: function(err){
                console.error(err);
                alert("This is a problem", err.message);
            }
        });        
    });
});