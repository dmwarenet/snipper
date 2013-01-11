$(document).ready(function(){
$("form#giveurl").submit(function(){
	$("#messagewindow").load("/geturl?url="+$("#msg").val()+"&type=json");
});
});
