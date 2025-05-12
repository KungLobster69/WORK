<?php //http://localhost/php/16forfor.php
  for ($i=2; $i<=5; $i++){
    echo "รอบใหญ่ที่ $i <br>";
    for ($j=1; $j<=3; $j++){
      echo " รอบเล็กที่ $j ($i*$j) ,";
    } // End for รอบเล็ก
    echo "<br><br>";
  } // End for รอบใหญ่
?>