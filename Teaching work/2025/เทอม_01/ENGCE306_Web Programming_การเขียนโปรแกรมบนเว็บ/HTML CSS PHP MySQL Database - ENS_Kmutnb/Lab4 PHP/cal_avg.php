<?php //http://localhost/php/cal_avg.php

$num1 = $_POST['num1'];
$num2 = $_POST['num2'];
$num3 = $_POST['num3'];
$num4 = $_POST['num4'];
$num5 = $_POST['num5'];

?>

<!doctype html>
<html>
<head>
    <title>Cal Average</title>
</head>

<body>

<h2>โปรแกรมคำนวณค่าเฉลี่ย</h2>
<form action="cal_avg.php" method="POST">
    Number 1 : <input type="text" name="num1"><br><br>
    Number 2 : <input type="text" name="num2"><br><br>
    Number 3 : <input type="text" name="num3"><br><br>
    Number 4 : <input type="text" name="num4"><br><br>
    Number 5 : <input type="text" name="num5"><br><br>
    <input type="reset" value="Clear">
    <input type="submit" value="Cal Average"><br><br>
</form>

<?php

if(isset($num1)){
  $sum = ($num1+$num2+$num3+$num4+$num5);
  $avg = $sum/5;
  echo "<h3>คำนวณค่าเฉลี่ย</h3>";
  echo "ค่าเฉลี่ย = ".$avg."<br>";
  echo "(ผลรวม = ".$sum.")<br>";
  
}// End isset
else {
  echo "ไม่มีข้อมูล";
}


?>

</body>
</html>