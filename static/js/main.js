$.ajax({
        type : 'POST',
        url : 'game',
        type : 'json',
        data: {
            email : $('#email').val()
        },
        success : function(data){
            $('#waiting').hide(500);
            $('#message').removeClass().addClass((data.error === true) ? 'error' : 'success')
                .text(data.msg).show(500);
            if (data.error === true)
                $('#demoForm').show(500);
        },
        error : function(XMLHttpRequest, textStatus, errorThrown) {
            $('#waiting').hide(500);
            $('#message').removeClass().addClass('error')
                .text('There was an error.').show(500);
            $('#demoForm').show(500);
        }
    });