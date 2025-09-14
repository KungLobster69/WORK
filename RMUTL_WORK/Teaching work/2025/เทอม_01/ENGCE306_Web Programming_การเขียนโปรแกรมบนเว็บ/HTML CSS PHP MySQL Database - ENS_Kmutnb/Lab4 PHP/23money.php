<?php //http://localhost/php/23money.php

function formatMoney($number, $fractional=false) { 
    if ($fractional) { 
        $number = sprintf('%.2f', $number); 
    } 
    while (true) { 
        $replaced = preg_replace('/(-?\d+)(\d\d\d)/', '$1,$2', $number); 
        if ($replaced != $number) { 
            $number = $replaced; 
        } else { break;  } 
    } 
    return $number; 
} // End Function formatMoney
$a = 19000000/7;
echo $a;                    echo "<br>"; // ปกติ
echo formatMoney($a, true);  echo "<br>"; // จัดรูปแบบ
?>

