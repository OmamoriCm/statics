$(document).ready(function() {

    try {
        $("#delivery_date").datepicker({
            minDate: new Date()
        });
    } catch (e) {}
    var $payment = $("#payment_method");
    $payment.on("click", 'button[type="submit"],button[name="submit"]', function(ev) {
        ev.preventDefault();
        ev.stopPropagation();
        var customer_order_delivery_date = $('#delivery_date').val();
        var customer_order_delivery_comment = $('#delivery_comment').val();
        openerp.jsonRpc('/shop/customer_order_delivery/', 'call', {
            'delivery_date': customer_order_delivery_date,
            'delivery_comment': customer_order_delivery_comment
        });

	 function sleep(milliseconds) {
	  var start = new Date().getTime();
	  for (var i = 0; i < 1e7; i++) {
	    if ((new Date().getTime() - start) > milliseconds){
	      break;
	    }
	  }
	}

     sleep(1000);  
    });

   
      
   
});
