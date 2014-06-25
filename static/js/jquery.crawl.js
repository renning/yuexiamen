$(document).ready(function(){
    $("#read_view").click(function(){
        var url = $("#read_url").val();
        var name = $("#name").val();
        if(url=="" || url==null ||name=="" || name==null ){
            alert ('网址和名称不能为空');
            return (false);
        }
        $("#results").slideDown("slow");
        x=$("form").serializeArray();
        $('#results').attr('src', "/pagerule/read/content/?loading=1" );
        $.post("/pagerule/read/view/", x, function(result){
            console.log(name);
            $('#results').attr('src', "/pagerule/read/content/?url_md5=" + result);
            $('#commit').attr('id', 'read_commit');
            $('#read_commit').attr('class', 'btn btn-large btn-success');
        });
    });

    $("#read_commit").click(function(){
        console.log(33)
        x=$("form").serializeArray();

        console.log(x)
        $.post("/pagerule/read/commit/", x, function(result){
            console.log(result)
            if(result=='1'){
                    alert('保存成功')
            }
            else   {
                    alert('保存失败，请重试')
            }
        });
    });

    $("#rss_view").click(function(){
        var url = $("#rss_url").val();
        var name = $("#name").val();
        if(url=="" || url==null ||name=="" || name==null ){
            alert ('网址和名称不能为空');
            return (false);
        }
        $("#results").slideDown("slow");
        x=$("form").serializeArray();
        $('#results').attr('src', "/rssrule/content/?loading=1" );
        $.post("/rssrule/view/", x, function(result){
            $('#results').attr('src', "/rssrule/content/?url_md5=" + result);
            $('#commit').attr('id', 'read_commit');
            $('#urlmd5').val(result);
            $('#read_commit').attr('class', 'btn btn-large btn-success');
        });
    });

    $("#rss_commit").click(function(){
        console.log(33)
        x=$("form").serializeArray();

        console.log(x)
        $.post("/rssrule/commit/", x, function(result){
            console.log(result)
            if(result=='1'){
                    alert('保存成功')
            }
            else   {
                    alert('保存失败，请重试')
            }
        });
    });

    $("#dove_view").click(function(){
        var url = $("#read_url").val();
        var name = $("#name").val();
        if(url=="" || url==null ||name=="" || name==null ){
            alert ('网址和名称不能为空');
            return (false);
        }
        $("#results").slideDown("slow");
        x=$("form").serializeArray();
        $('#results').attr('src', "/pagerule/dove/content/?loading=1" );
        $.post("/pagerule/dove/view/", x, function(result){
            $('#results').attr('src', "/pagerule/dove/content/?url_md5=" + result);
            $('#commit').attr('id', 'read_commit');
            $('#read_commit').attr('class', 'btn btn-large btn-success');
        });
    });

    $("input#read_url").bind("input propertychange", function(){
            var url = $(this).val()
            var durl=/^http:\/\/(.*?)\//g;
            var ddomain=/([\w-]+)\.(se|com|net|org|gov|cc|biz|info|cn)(\.|\/)(cn|hk)*/;
            re =url.match(durl);
            domain=url.match(ddomain)
            if(re){
                var domain_str = ''
                if(domain){
                domain_str = domain[1]
                }
                var re_str=re[0]
                re_str = re_str.replace(/http/, "^http")
                re_str = re_str.replace(/\./g, "\\\.")
                $("#domain").val(domain_str);
                $("#url_regular").val(re_str);
            }
    });
});


