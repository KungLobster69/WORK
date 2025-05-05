<?php //http://localhost/php/20array2.php

$std[1][1] = 'Meena';
$std[1][2] = 75;
$std[2][1] = 'Kanya';
$std[2][2] = 82;
$std[3][1] = 'Thanwa';
$std[3][2] = 56;

for($i=1; $i<=3; $i++)
  for($j=1; $j<=2; $j++)
    echo $std[$i][$j]."<br>";
?> 