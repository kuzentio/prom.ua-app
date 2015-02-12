$(document).ready(function(e) {
        $("input:checkbox:checked").attr("disabled", true);

        $('.send-vote').click(function(e){
            var thisCheck = $(this),
                answerId = $(e.currentTarget).parent().data('answer_id');

            $(e.currentTarget).attr("disabled", true);

            if ( thisCheck.is(':checked') ){
                $.post('/answers/'+answerId+'/vote/');
                    var vote_val = $(e.currentTarget).parent().find('span.count_votes');
                    vote_val.html(parseInt(vote_val.text()) + 1);
            }
        });
    });
