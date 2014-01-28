var support_type_ele = django.jQuery("#id_support_type")
var support_type = support_type_ele.val()

function toogle_type(support_type){
	if ( support_type != "") {
		django.jQuery(".inline-group").hide();
	} else if (support_type != ""){
		django.jQuery(".inline-group").show();
	} else {
		django.jQuery("#"+support_type+"_set_group").show();
	}
}

support_type_ele.on("change", function(){
	var that = django.jQuery(this);
	console.log(that.val())
	toogle_type(that.val())
})

// support_type_ele.change(function() {

// })



