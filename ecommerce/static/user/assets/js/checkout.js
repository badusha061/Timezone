$(document).ready(function() {
    $('#proceedPayment').click(function(e) {
        e.preventDefault();

        var fname = $("#firstname").data('name');
        var lname = $("#lastname").data('name');
        var address = $("#address").data('name');
        var number = $("#phone").data('name');
        var email = $("#email").data('name');
        var city = $("#city").data('name');
        var pincode = $("#pincode").data('name');
        var state = $("#state").data('name');
        var country = $("#country").data('name');
        var selectedAddress = $("input[name='default_address']:checked").val();
        var token = $("[name='csrfmiddlewaretoken']").val();
        var selectedPaymentMethod = $("input[name='payment-method']:checked").val();

        if (!selectedAddress) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Select Address!',
                footer: '<a href="">Why do I have this issue?</a>'
              })
            return false;
        }
        if (!selectedPaymentMethod) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Select Payment Method!',
                footer: '<a href="">Why do I have this issue?</a>'
              })
            return false;
        }

        if (selectedPaymentMethod === 'cod') {
            var postData = {
                "address": selectedAddress,
                "payment-method": selectedPaymentMethod,
                'csrfmiddlewaretoken': token
            }

            $.ajax({
                method: "POST",
                url: "placeorder",
                data: postData,
                success: function(responsec) {
                    
                    var userOrderUrl = "{% url 'userauth:home' %}";
                    window.location.href = userOrderUrl;

                    Swal.fire("Congratulations!", responsec.status, "success")
                },
                error: function(xhr, status, error) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'Something went wrong!',
                        footer: '<a href="">Why do I have this issue?</a>'
                      })
                    return false
                }
            });
            
         } else if (selectedPaymentMethod === 'wallet') {
            console.log('the wallet is taken')
            var postData = {
                "address": selectedAddress,
                "payment-method": selectedPaymentMethod,
                'csrfmiddlewaretoken': token
            }

            $.ajax({
                method: "POST",
                url: "placeorder",
                data: postData,
                success: function(responsec) {
                    console.log("Server responded with:", responsec);
                    if (responsec.status === "You Do Not Have Sufficient Balance") {
                        Swal.fire({
                            icon: 'error',
                            title: 'Oops...',
                            text: responsec.status,
                            footer: '<a href="">Why do I have this issue?</a>'
                        });
                    } else if (responsec.status === "Order has been placed") {
                        Swal.fire("Congratulations!", responsec.status, "success");
                    } else if (responsec.status == "No Wallet found for the user") {
                        Swal.fire({
                            icon: 'error',
                            title: 'Oops...',
                            text: responsec.status,
                            footer: '<a href="">Contact support?</a>'
                        });
                    }
                },
                
            });
            

        } else if (selectedPaymentMethod === 'paypal') {
            $.ajax({
                method: "GET",
                url: "proceed-to-pay",
                success: function(data) {
                    console.log(data);

                    var options = {
                        "key": "rzp_test_CHjcfdYGx6z4Ib",
                        "amount": data.total_price * 100,
                        "currency": "INR",
                        "name": "Time Zone",
                        "description": "Thanks for buying from us",
                        "image": "https://example.com/your_logo",
                        "order_id": data.order_id,
                        "handler": function(responseb) {
                            console.log(responseb);
                            alert(responseb.razorpay_payment_id);
                            alert(responseb.razorpay_order_id);
                            alert(responseb.razorpay_signature);

                            var postData = {
                                "address": selectedAddress,
                                "payment-method": selectedPaymentMethod,
                                "payment_id": responseb.razorpay_payment_id,
                                'csrfmiddlewaretoken': token
                            }

                            $.ajax({
                                method: "POST",
                                url: "placeorder",
                                data: postData,
                                success: function(responsec) {
                                    Swal.fire("Order has been placed", responsec.status, "success")
                                    
                                },
                                error: function(xhr, status, error) {
                                    console.error("AJAX error in POST:", status, error);
                                }
                            });
                        }
                    };

                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                },
            
            });
        }
    });
});

    