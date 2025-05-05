<!DOCTYPE html>
<html>
<head>
    <title>การเขียนเว็บด้วย PHP</title>
</head>
<body>
<h3>แสดงเวลาปัจจุบัน</h3>
<?php //http://localhost/php/9html2.php
date_default_timezone_set("Asia/Bangkok");
   $time = date("d/m/Y");
   echo "วันนี้วันที่ ".$time."<br>";
   echo "เวลา ".date("H:i.s");
   echo "<br>";
?>
ข้อความในส่วนภาษา HTML
</body>
</html>