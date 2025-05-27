<?php //http://localhost/php/15forif.php
  for ($i=1; $i<=10; $i++){
    echo $i;
    if ($i%2 == 0){
      echo " เป็นเลขคู่";
    } else {
      echo " เป็นเลขคี่";
    } 
    echo "<br>";
  } // END for
?>