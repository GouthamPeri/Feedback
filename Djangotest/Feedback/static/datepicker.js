<input type="text" class="span2" id="dp1">
<script>
$(function(){
	$('#dp1').fdatepicker({
		initialDate: '02-12-1989',
		format: 'mm-dd-yyyy',
		disableDblClickSelection: true,
		leftArrow:'<<',
		rightArrow:'>>',
		closeIcon:'X',
		closeButton: true
	});
});
</script>