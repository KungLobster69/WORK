<?php //http://localhost/php/sample_3.php

$x = $_POST['x'];
$y = $_POST['y'];

?>

<!doctype html>
<html>
<head>
    <title>เครื่องคิดเลข</title>
</head>

<body>
<h2>เครื่องคิดเลข</h2>
<form action="sample_3.php" method="POST">
    ค่า x : <input type="text" name="x"><br><br>
    ค่า y : <input type="text" name="y"><br><br>
    <input type="submit" value="คำนวณ">
    <input type="reset" value="ยกเลิก"><br><br>
</form>

<?php

if(isset($x)){
  $sum = $x+$y;
  $minus = $x-$y;
  $multiple = $x*$y;
  $divide = $x*$y;
  echo "<h3>ผลลัพธ์</h3>";
  echo " $x + $y = ".$sum."<br>";
  echo " $x - $y = ".$minus."<br>";
  echo " $x * $y = ".$multiple."<br>";
  echo " $x * $y = ".$divide."<br>";
}// End isset
else {
  echo "ไม่มีข้อมูล";
}


?>

</body>
</html>