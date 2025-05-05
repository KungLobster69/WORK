<?php //http://localhost/php/sample_2.php

  $number1 = 10;
  $number2 = 7;

  $result = $number1/$number2;
  $result = intval($result);
  $remain = $number1%$number2;

  echo "ผลลัพธ์ = ".$result."<br>";
  echo "เศษ = ".$remain;  

?>