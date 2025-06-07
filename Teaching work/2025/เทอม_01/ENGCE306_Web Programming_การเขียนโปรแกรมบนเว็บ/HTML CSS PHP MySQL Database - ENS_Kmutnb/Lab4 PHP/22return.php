<?php //http://localhost/php/22return.php

function area($base,$high){
   $result = 1/2*$base*$high;
   return $result;
}

$a = 2;  $b = 3;
$triangle1 = area($a,$b);
echo "Area 1 = $triangle1 <br>";

$x = 10;  $y = 5;
$triangle2 = area($x,$y);
echo "Area 2 = $triangle2 <br>";

?> 