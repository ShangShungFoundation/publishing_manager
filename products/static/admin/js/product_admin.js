function toogle_type(support_type){
	if ( support_type == "") {
		django.jQuery(".inline-group").hide();
	} else if (support_type == "comp"){
		django.jQuery(".inline-group").show();
	} else {
		django.jQuery(".inline-group").hide();
		django.jQuery("#"+support_type+"_set-group").show();
	}
	django.jQuery("#productcontribution_set-group").show();
}

django.jQuery(function(){ 
	var support_type_ele = django.jQuery("#id_support_type")
	var support_type = support_type_ele.val();
	toogle_type(support_type);
	support_type_ele.on("change", function(){
		toogle_type(this.value)
	})

})
// support_type_ele.change(function() {

// })



