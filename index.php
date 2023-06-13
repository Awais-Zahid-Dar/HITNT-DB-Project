<!DOCTYPE html>
<html>
<head>
<link rel="shortcut icon" href="logo.jpeg">
    <script src="https://kit.fontawesome.com/aa9e7954bf.js" crossorigin="anonymous"></script>
  <title>Healthy Is The New Thin</title>
  <style>
    .product-container {
      
      margin-top: 20px;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
    }

    .product-card {
      background-color: RGB(255 253 61);
      width: calc(20% - 20px);
      margin-bottom: 20px;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }

    .product-image {
      width: 100%;
      height: auto;
    }

    .product-title {
      font-weight: bold;
      margin-top: 10px;
      color: RGB(73 84 92);
    }

    .product-description {
      margin-top: 5px;
      color: RGB(73 84 92);
    }

    .product-price {
      font-weight: bold;
      margin-top: 10px;
      color: RGB(73 84 92);
    }

    .quantity {
      width: 50px;
    }

    .add-to-cart {
      margin-left:10px;
      margin-top: 10px;
      padding: 5px 10px;
      background-color: RGB(73 84 92);
      color: RGB(255 253 61);
      border: none;
      cursor: pointer;
    }
    .add-to-cart:hover{
      text-decoration: underline;
      color: white;


    }

    .place-order {
      text-align: center;
      margin-top: 20px;
    }

    .place-order button {
      padding: 10px 20px;
      background-color: #f44336;
      color: #fff;
      border: none;
      cursor: pointer;
    }
    .place-order button:hover{
      text-decoration: underline;
      font-weight: bold;
    }

    .order-details {
      text-align: center;
      margin-top: 20px;
    }

    .order-details p {
      font-weight: bold;
    }
    .header {
      display: flex;
      align-items: center;
      justify-content: space-around;
      padding: 20px;
      background-color: RGB(255 253 61);
    }

    .logo {
      display: flex;
      align-items: center;
    }

    .logo img {
      height: 30px;
      margin-right: 10px;
    }

    .logo h1 {
      margin: 0;
      font-size: 24px;
      display: flex;
      align-items: center;
      color:RGB(73 84 92);
    }

    

    .social-icons {
      display: flex;
      align-items: center;
    }

    .social-icons a {
      margin-right: 10px;
      text-decoration: none;
      color:RGB(73 84 92);
    }
    .social-icons a:hover{
      text-decoration: underline;
      text-decoration-color: RGB(73 84 92);
    }
    body{
      background-color: RGB(73 84 92);
    }
     i{
    display: inline-block;
    margin: 10px;

   padding-top: 10px;
}
  </style>
</head>
<body>
<div class="header">
    <div class="logo">
      <img src="logo.jpeg" alt="Logo">
      <h1>Healthy Is The New Thin</h1>
    </div>
    <div class="social-icons">
    <a href="https://www.facebook.com/mamoonahossain"> Facebook  <i class="fa-brands fa-square-facebook" style="color: RGB(73 84 92);"></i></a>
    <a href="https://instagram.com/keto_with_mona?igshid=NTc4MTIwNjQ2YQ=="> Instagram <i class="fa-brands fa-square-instagram" style="color: RGB(73 84 92);"></i></a>
    </div>
  </div>
  <div class="product-container">
    <?php
    if(isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on')   
    $url = "https://";   
    else  
    $url = "http://";   
    // Append the host(domain name, ip) to the URL.   
    $url.= $_SERVER['HTTP_HOST'];   
    
    // Append the requested resource location to the URL   
    $url.= $_SERVER['REQUEST_URI'];    
    
    #echo $url;  
    $url_components = parse_url($url);
    
    // Use parse_str() function to parse the
    // string passed via URL
    parse_str($url_components['query'], $params);
    #echo ' Hi '.$params['uid'];
    // Database connection
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "keto_shop";

    $conn = new mysqli($servername, $username, $password, $dbname);

    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // Fetching product data from the database
    $sql = "SELECT * FROM product";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            echo '<div class="product-card" data-id="' . $row["PID"] . '">';
            echo '<img class="product-image" src="data:image/png;base64,' .base64_encode( $row['Pic'] ) .'" />';
            #echo '<img class="product-image" src="' . $row["Pic"] . '"/>';
            echo '<h2 class="product-title">' . $row["Name"] . '</h2>';
            echo '<p class="product-description">' . $row["Description"] . '</p>';
            echo '<p class="product-price">$' . $row["Price"] . '</p>';
            echo '<input type="number" class="quantity" min="1" value="1">';
            echo '<button class="add-to-cart" onclick="addToCart(' . $row["PID"] . ', \'' . $row["Name"] . '\', ' . $row["Price"] . ')">Add to Cart</button>';
            echo '</div>';
        }
    } else {
        echo "No products found.";
    }

    $conn->close();
    ?>
</div>
   

    <script>
      var cart = [];

      function addToCart(productId, productName, productPrice) {
        var quantityInput = document.querySelector('.product-card[data-id="' + productId + '"] .quantity');
        var quantity = parseInt(quantityInput.value);
        var product = {
          PID: productId,
          Name: productName,
          Price: productPrice,
          Quantity: quantity
        };
        cart.push(product);
        quantityInput.value = 1;
        alert('Product added to cart.');
      }

      function placeOrder() {
  var orderDetailsDiv = document.getElementById('orderDetails');
  var orderSummaryDiv = document.getElementById('orderSummary');
  orderSummaryDiv.innerHTML = '';

  if (cart.length > 0) {
    var totalPrice = 0;
    for (var i = 0; i < cart.length; i++) {
      var product = cart[i];
      var productTotalPrice = product.Price * product.Quantity;
      totalPrice += productTotalPrice;

      var orderSummary = document.createElement('p');
      orderSummary.innerHTML = 'Product: ' + product.Name + ' | Quantity: ' + product.Quantity + ' | Price: $' + product.Price + ' | Total: $' + productTotalPrice;
      orderSummaryDiv.appendChild(orderSummary);
    }
    var totalPriceDisplay = document.createElement('p');
    totalPriceDisplay.innerHTML = 'Total Price: $' + totalPrice;
    orderSummaryDiv.appendChild(totalPriceDisplay);
    orderDetailsDiv.style.display = "block";

    // Call the PHP file for insertion using fetch API
    fetch('insert_order.php', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        uid: '<?php echo $params['uid']; ?>', // Pass the user ID from PHP
        cart: cart // Pass the cart data
      })
    })
    .then(function(response) {
      return response.text();
    })
    .then(function(data) {
      alert(data); // Display the response from the PHP file
    })
    .catch(function(error) {
      console.log(error);
    });
  } else {
    alert('No products in cart.');
  }
}

    </script>

    <div class="place-order">
      <button onclick="placeOrder()">Place Order</button>
    </div>
    <div class="order-details" id="orderDetails">
      <h2>Order Details</h2>
      <div id="orderSummary"></div>
    </div>

</body>
</html>
