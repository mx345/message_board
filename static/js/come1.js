"use strict";

$(function() {
    
    $("#uname").blur(function()
    {
        var uname = $(this).val();

        //用户格式校验
        if (uname.trim() ==="")
        {
            $("#uname_tips").css("color","red")
            $("#uname_tips").text("用户名不能为空")
            return;
        }

        if(/[\u4E00-\u9FFF]/.test(uname))
        {
            $("#uname_tips").css("color","red")
            $("#uname_tips").text("用户名不能为中文")
            return;
        }
        if (uname.length<4 ||uname.length>20 )
        {
            $("#uname_tips").css("color","red")
            $("#uname_tips").text("用户名最少为4字符！最大为20字符")
            return;
        }
        if (!/[a-zA-Z0-9_]+$/.test(uname))
        {

            $("#uname_tips").css("color","red")
            $("#uname_tips").text("用户名只能包含字母数字下划线")
            return;
        }
        
    });
    var password
    $("#upass").blur(function()
    {
       password = $(this).val()
    
      if(password.length<6 ||password.length >15)
      {
        $("#upass_tips").css("color","red")
        
        $("#upass_tips").text("密码必须大于5，小于15！")
      }
      else{
        $("#upass_tips").css("color","green")
        $("#upass_tips").css("font-width","bold")
        $("#upass_tips").text("ok")  
      }
    })
    $("#upass2").blur(function()
    {   
        var password2= $(this).val()
        console.log(password2)
        console.log(password)
        if (password===password2)
        {   
            $("#upass2_tips").css("color","green")
            $("#upass2_tips").css("font-width","bold")
            $("#upass2_tips").text("ok")  

           
        }
        else{
            $("#upass2_tips").css("color","red")
            $("#upass2_tips").text("两次输入密码不一致！")
        }


    })


    });
