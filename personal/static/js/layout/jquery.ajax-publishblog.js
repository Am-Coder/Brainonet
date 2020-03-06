$(document).ready(function(){


    $('.uploadBlog').click(function(){
        var title = $('.blog-title').val();
        var url = $('.blog-image').val();
        var genre = $('.blog-genre').val();
        if( title == ""  ){
            $('.blog-title').css('border-color','red');
            $('.blog-image').css('border-color','green');

        }else if(url == "" || !is_url(url) ){
            $('.blog-title').css('border-color','green');
            $('.blog-image').css('border-color','red');

        }else{
            $('.blog-title').css('border-color','green');
            $('.blog-image').css('border-color','green');
            $('.blog-genre').css('border-color','green');
            

            $("#contentarea").contents().find("div").attr('contenteditable','false');

            // var content = $("#contentarea").contents().find(".blogContent").html();
            var content = $("#contentarea").contents().find("body").html();

            console.log(content);

            if(content){

                $.ajax({
                    type : "POST",
                    cache: false,
                    // contentType : "application/json",//type of data being send to server
                    url : "uploadBlog.php",
                    data : {title: title, url: url, info: content, genre: genre },
                    
                    dataType : "json",//result expected from server
                                    //with json return type we can return java objects
                                    //With text we can return String from java conroller
                    timeout : 10000,
                    success : function(upload) {

                        console.log(upload);
                        if( upload == -1 ){
                            alert("Session Expired. Retry after logging in again");
                        }else
                            alert("Your blog is online");
                    },
                    error : function(e) {
                        alert('Some Problem Occured while uploading. Please try again after some time.')
                        console.log("ERROR: ", e);
                    },
                    complete : function(e) {
                        $('#myModalPublish').modal('hide');
                        $('.loader').hide();
                        window.location.assign("http://www.wiredonline.xyz/mainsite/index.html");

                    }
                });

            }else{
                alert("No Content to upload");
            }
        }
    })

    function is_url(str){
    regexp =  /^(?:(?:https?|ftp):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?$/;
            if (regexp.test(str))
            {
            return true;
            }
            else
            {
            return false;
            }
    }
})