<?php //http://localhost/php/formget.php

$firstname = $_GET['firstname'];
$password = $_GET['password'];
$comment = $_GET['comment'];

?>

<!doctype html>
<html>
<head>
    <title>ส่งข้อมูลผ่าน Form</title>
</head>

<body>
<h2>ส่งข้อมูลผ่าน Form (Get)</h2>
<form action="formget.php" method="GET">
    First Name : <input type="text" name="firstname"><br><br>
    Password : <input type="password" name="password"><br><br>
    Comment : <textarea name="comment"></textarea><br><br>
    <input type="submit" value="SEND"><br><br>
</form>

<?php

if(isset($firstname)){
  echo "<h3>ข้อมูลที่รับเข้ามา</h3>";
    echo $firstname;
    echo '<br>';
    echo $password;
    echo '<br>';
    echo $comment;
}// End isset
else {
	echo "ไม่มีข้อมูล";
}


?>

</body>
</html>