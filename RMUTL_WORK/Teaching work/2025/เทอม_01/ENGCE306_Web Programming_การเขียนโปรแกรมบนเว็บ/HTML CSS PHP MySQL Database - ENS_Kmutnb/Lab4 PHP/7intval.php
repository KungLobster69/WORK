<?php //http://localhost/php/7intval.php

    $sum = '35abc';
    $x = 32;
    $y = 5;
    echo intval(42);        echo '<br>';
    echo intval(4.2);       echo '<br>';
    echo intval('42');      echo '<br>';
    echo intval('+42');     echo '<br>';
    echo intval('-42');     echo '<br>';
    echo intval($sum);      echo '<br>';
    echo intval($x/$y);     echo '<br>';
    echo intval($x%$y);     echo '<br>';

?>
