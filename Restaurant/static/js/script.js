document.addEventListener("DOMContentLoaded", function () {

  var addToCartBtn = document.getElementById("add-to-cart-btn");
  var cartPopup = document.getElementById("cart-popup");
  
  function updateCartCount(count) {
    document.getElementById("cart-count").textContent = count;
  }

  // Fetch initial cart count when the page loads
  fetch('/get_cart_count')
    .then(response => response.json())
    .then(data => {
      updateCartCount(data.cart_count);
    })
    .catch(error => {
      console.error('Error:', error);
    });

  const item = document.querySelectorAll(".addtocart");
  item.forEach(function (button) {
    button.addEventListener("click", function () {
      
      const item = button.getAttribute("item-id");
      cartPopup.textContent = "🛒 Item added to your cart! Happy shopping! 🎉";
      cartPopup.style.display = "block";

    // Hide the message after 3 seconds (3000 milliseconds)
    setTimeout(function() {
      cartPopup.style.display = "none";
    }, 3000);

      fetch('/addtocart', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ pid: item })
      })
        .then(response => response.json())
        .then(data => {
          // Update the cart count on the webpage
          document.getElementById("cart-count").textContent = data.cart_count;
        })
        .catch(error => {
          console.error('Error:', error);
        });
    })
  })



  const decreaseButtons = document.querySelectorAll(".decrease-btn");
  const increaseButtons = document.querySelectorAll(".increase-btn");

  decreaseButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      const itemname = button.getAttribute("data-item-id");


      const itemprice = button.getAttribute("item-price");
      let bp = parseInt(itemprice);

      let totalElement = document.getElementById('total');
      let total = parseInt(totalElement.innerText);
      total = total - bp;
      totalElement.innerText = total;


      const currprice = document.getElementById('currprice' + itemname);
      let cp = parseInt(currprice.innerText);
      cp -= bp
      currprice.innerText = cp


      const quantityElement = document.getElementById("count" + itemname);
      let quantity = parseInt(quantityElement.innerText);
      let item = document.getElementById("item" + itemname);
      if (quantity > 0) {
        quantity--;
        quantityElement.innerText = quantity;
        updateSession(itemname, quantity);
      }
      if (quantity == 0) {
        item.style.display = "none";
        updateSession(itemname, quantity);

      }


    });
  });

  increaseButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      const itemname = button.getAttribute("data-item-id");

      const itemprice = button.getAttribute("item-price");
      let bp = parseInt(itemprice);
      let totalElement = document.getElementById('total');
      let total = parseInt(totalElement.innerText);
      total = total + bp;
      totalElement.innerText = total;

      const currprice = document.getElementById('currprice' + itemname);
      let cp = parseInt(currprice.innerText);
      cp += bp
      currprice.innerText = cp

      const quantityElement = document.getElementById("count" + itemname);
      let quantity = parseInt(quantityElement.innerText);

      quantity++;
      quantityElement.innerText = quantity;
      updateSession(itemname, quantity);
    });
  });
  function updateSession(itemname, quantity) {

    fetch('/update_session', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ [itemname]: quantity })
    })
      .then(response => {
        if (response.ok) {
          console.log('Session data updated successfully');
        } else {
          console.error('Failed to update session data');
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }

});
