// $(function () { // Same as document.addEventListener("DOMContentLoaded"..

//     // Same as document.querySelector("#navbarToggle").addEventListener("blur",...
//     $("#navbarToggle").blur(function (event) {
//       var screenWidth = window.innerWidth;
//       if (screenWidth < 768) {
//         $("#collapsable-nav").collapse('hide');
//       }
//     });
//   });

// function sayhello () {
//   var name =  document.getElementById("one").value;
//    document.getElementById("content").textContent ="Hello "+name;

// };

//   // (function (global) {

//   // var dc = {};

//   // var homeHtml = "snippets/home-snippet.html";
//   // var allCategoriesUrl = 
//   //   "http://davids-restaurant.herokuapp.com/categories.json";
//   // var categoriesTitleHtml = "snippets/categories-title-snippet.html";
//   // var categoryHtml = "snippets/category-snippet.html";
//   // var menuItemsUrl = 
//   //   "http://davids-restaurant.herokuapp.com/menu_items.json?category=";
//   // var menuItemsTitleHtml = "snippets/menu-items-title.html";
//   // var menuItemHtml = "snippets/menu-item.html";

//   // // Convinience function for inserting innerHTML for 'select'
//   // var insertHtml = function (selector, html) {
//   //   var targetElem = document.querySelector(selector);
//   //   targetElem.innerHTML = html;
//   // };

//   // Show loading icon inside element identified by 'selector'.
//   var showLoading = function (selector) {
//     var html = "<div class='text-center'>";
//     html += "<img src='images/ajax-loader.gif'></div>";
//     insertHtml(selector, html);
//   };

//   // Return substitute of '{{propName}}' 
//   // with propValue in given 'string' 
//   var insertProperty = function (string, propName, propValue) {
//     var propToReplace = "{{" + propName + "}}";
//     string = string
//       .replace(new RegExp(propToReplace, "g"), propValue);
//     return string;
//   }

//   // Remove the class 'active' from home and switch to Menu button
//   var switchMenuToActive = function () {
//     // Remove 'active' from home button
//     var classes = document.querySelector("#navHomeButton").className;
//     classes = classes.replace(new RegExp("active", "g"), "");
//     document.querySelector("#navHomeButton").className = classes;

//     // Add 'active' to menu button if not already there
//     classes = document.querySelector("#navMenuButton").className;
//     if (classes.indexOf("active") == -1) {
//       classes += " active";
//       document.querySelector("#navMenuButton").className = classes;
//     }
//   };

//   // On page load (before images or CSS)
//   document.addEventListener("DOMContentLoaded", function (event) {

//   // On first load, show home view
//   showLoading("#main-content");
//   $ajaxUtils.sendGetRequest(
//     homeHtml, 
//     function (responseText) {
//       document.querySelector("#main-content")
//         .innerHTML = responseText;
//     }, 
//     false);
//   });

//   // Load the menu categories view
//   dc.loadMenuCategories = function () {
//     showLoading("#main-content");
//     $ajaxUtils.sendGetRequest(
//       allCategoriesUrl,
//       buildAndShowCategoriesHTML);
//   };


//   // Load the menu items view
//   // 'categoryShort' is a short_name for a category
//   dc.loadMenuItems = function (categoryShort) {
//     showLoading("#main-content");
//     $ajaxUtils.sendGetRequest(
//       menuItemsUrl + categoryShort,
//       buildAndShowMenuItemsHTML);
//   };


//   // Builds HTML for the categiries page based on the data
//   // from the server
//   function buildAndShowCategoriesHTML (categories) {
//     // Load title snippet of categories page
//     $ajaxUtils.sendGetRequest(
//       categoriesTitleHtml,
//       function (categoriesTitleHtml) {
//         // Retrieve single category snippet
//         $ajaxUtils.sendGetRequest(
//           categoryHtml,
//           function (categoryHtml) {
//             // Switch CSS class active to menu button
//             switchMenuToActive();

//             var categoriesViewHtml = 
//               buildCategoriesViewHtml(categories, 
//                                       categoriesTitleHtml,
//                                       categoryHtml);
//             insertHtml("#main-content", categoriesViewHtml);
//           },
//           false);
//       },
//       false);
//   }


//   // Using categories data and snippets html
//   // build categories view HTML to be inserted into page
//   function buildCategoriesViewHtml(categories, 
//                                    categoriesTitleHtml,
//                                    categoryHtml) {

//     var finalHtml = categoriesTitleHtml;
//     finalHtml += "<section class='row'>";

//     // Loop over categories
//     for (var i = 0; i < categories.length; i++) {
//       // Insert category values
//       var html = categoryHtml;
//       var name = "" + categories[i].name;
//       var short_name = categories[i].short_name;
//       html = 
//         insertProperty(html, "name", name);
//       html = 
//         insertProperty(html, 
//                        "short_name",
//                        short_name);
//       finalHtml += html;
//     }

//     finalHtml += "</section>";
//     return finalHtml;
//   }



//   // Builds HTML for the single category page based on the data
//   // from the server
//   function buildAndShowMenuItemsHTML (categoryMenuItems) {
//     // Load title snippet of menu items page
//     $ajaxUtils.sendGetRequest(
//       menuItemsTitleHtml,
//       function (menuItemsTitleHtml) {
//         // Retrieve single menu item snippet
//         $ajaxUtils.sendGetRequest(
//           menuItemHtml,
//           function (menuItemHtml) {
//             // Switch CSS class active to menu button
//             switchMenuToActive();

//             var menuItemsViewHtml = 
//               buildMenuItemsViewHtml(categoryMenuItems, 
//                                      menuItemsTitleHtml,
//                                      menuItemHtml);
//             insertHtml("#main-content", menuItemsViewHtml);
//           },
//           false);
//       },
//       false);
//   }


//   // Using category and menu items data and snippets html
//   // build menu items view HTML to be inserted into page
//   function buildMenuItemsViewHtml(categoryMenuItems, 
//                                   menuItemsTitleHtml,
//                                   menuItemHtml) {

//     menuItemsTitleHtml = 
//       insertProperty(menuItemsTitleHtml,
//                      "name",
//                      categoryMenuItems.category.name);
//     menuItemsTitleHtml = 
//       insertProperty(menuItemsTitleHtml,
//                      "special_instructions",
//                      categoryMenuItems.category.special_instructions);

//     var finalHtml = menuItemsTitleHtml;
//     finalHtml += "<section class='row'>";

//     // Loop over menu items
//     var menuItems = categoryMenuItems.menu_items;
//     var catShortName = categoryMenuItems.category.short_name;
//     for (var i = 0; i < menuItems.length; i++) {
//       // Insert menu item values
//       var html = menuItemHtml;
//       html = 
//         insertProperty(html, "short_name", menuItems[i].short_name);
//       html = 
//         insertProperty(html, 
//                        "catShortName",
//                        catShortName);
//       html =
//         insertItemPrice(html,
//                         "price_small",
//                         menuItems[i].price_small); 
//       html =
//         insertItemPortionName(html,
//                               "small_portion_name",
//                               menuItems[i].small_portion_name);
//       html = 
//         insertItemPrice(html,
//                         "price_large",
//                         menuItems[i].price_large);
//       html =
//         insertItemPortionName(html,
//                               "large_portion_name",
//                               menuItems[i].large_portion_name);
//       html = 
//         insertProperty(html, 
//                        "name",
//                        menuItems[i].name);
//       html = 
//         insertProperty(html, 
//                        "description",
//                        menuItems[i].description);

//       // Add clearfix after every second menu item
//       if (i % 2 != 0) {
//         html += 
//           "<div class='clearfix visible-lg-block visible-md-block'></div>";
//       }

//       finalHtml += html;
//     }

//     finalHtml += "</section>";
//     return finalHtml;
//   }


//   // Appends price with '$' if price exists
//   function insertItemPrice(html,
//                            pricePropName,
//                            priceValue) {
//     // If not specified, replace with empty string
//     if (!priceValue) {
//       return insertProperty(html, pricePropName, "");;
//     }

//     priceValue = "$" + priceValue.toFixed(2);
//     html = insertProperty(html, pricePropName, priceValue);
//     return html;
//   }


//   // Appends portion name in parens if it exists
//   function insertItemPortionName(html,
//                                  portionPropName,
//                                  portionValue) {
//     // If not specified, return original string
//     if (!portionValue) {
//       return insertProperty(html, portionPropName, "");
//     }

//     portionValue = "(" + portionValue + ")";
//     html = insertProperty(html, portionPropName, portionValue);
//     return html;
//   }


//   global.$dc = dc;


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
