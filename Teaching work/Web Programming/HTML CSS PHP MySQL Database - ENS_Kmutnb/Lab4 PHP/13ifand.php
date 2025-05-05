<?php //http://localhost/php/13ifand.php
  $age = 22;
  if($age >= 60) {
    echo "ผู้สูงอายุ"; } 
  elseif ($age>=18 and $age <60) {
    echo "คนทั่วไป";
  } else {
    echo "เยาวชน";
  }
?>