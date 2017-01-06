$(document).ready(function(){
//     console.log('yo')
//     window.onerror = function (errorMsg, url, lineNumber) {
//     alert('Error: ' + errorMsg + ' Script: ' + url + ' Line: ' + lineNumber);
// }
    // var csrf_token = "{{ request.session.get_csrf_token() }}";
    var button = $(".submit");
    button.on("click", function(e){
        e.preventDefault();
        var title = $(this).parent().find("input[name='title']")[0].value;
        var body = $(this).parent().find("textarea[name='body']")[0].value;
        // send ajax request to delete this expense
        $.ajax({
            // headers: { 'X-CSRF-Token': csrf_token},
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
                console.log(new_post_id);


                console.log(new_post_href)
                post_template = '<h2><a href="' + new_post_href + '">' + title + '</a></h2>'+
                    '<p class="lead">by <a href="/about_me">Julien Wilson</a></p>'+
                    '<p><span class="glyphicon glyphicon-time"></span> Posted on Today</p>'+
                    '<br/>'
                $('#posts').prepend(post_template);
                $('form')[0].reset();



                    //                 <h2>
                    //     <a href="/journal/{{entry['id']}}">{{entry['title']}}</a>
                    // </h2>
                    // <p class="lead">
                    //     by <a href="/about_me">Julien Wilson</a>
                    // </p>
                    // <p><span class="glyphicon glyphicon-time"></span> Posted on {{ entry['date']}}</p>
                    // <br/>

            },
            error: function(err){
                console.error(err);
                alert("This is a problem", err.message);

            }
        });        
        // // fade out expense
        // this_row = $(this.parentNode.parentNode);
        // // delete the containing row
        // this_row.animate({
        //     opacity: 500
        // }, 100, function(){
        //     $(this).remove();
        // })
    });
});