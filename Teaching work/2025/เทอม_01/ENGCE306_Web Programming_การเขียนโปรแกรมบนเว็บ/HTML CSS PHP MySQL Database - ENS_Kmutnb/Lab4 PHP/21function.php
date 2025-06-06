<?php //http://localhost/php/21function.php

function hello () {
  echo "Say Hello <br>";
}
function goodbye () {
    echo "Good Bye !<br>";
  }

for($i = 1; $i<= 10; $i++) {
  echo $i." ";
  if ($i < 10) {
    hello();
  } else {
    goodbye();
  }
}
?> 