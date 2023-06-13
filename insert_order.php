<?php
// Database connection
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "keto_shop";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Retrieve the user ID and cart data from the request
$data = json_decode(file_get_contents('php://input'), true);
$userId = $data['uid'];
$cart = $data['cart'];

// Insert each product in the cart into the order_details table
foreach ($cart as $product) {
    $productId = $product['PID'];
    $productName = $product['Name'];
    $productPrice = $product['Price'];
    $productQuantity = $product['Quantity'];
    $totalPrice = $productPrice * $productQuantity;

    $sql = "INSERT INTO order_details (userid, productID, productName, productPrice, productQuantity, totalPrice) VALUES (?, ?, ?, ?, ?, ?)";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ssssss", $userId, $productId, $productName, $productPrice, $productQuantity, $totalPrice);
    $stmt->execute();
}

$stmt->close();
$conn->close();

echo "Order placed successfully!";
?>
