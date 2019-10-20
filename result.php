<html>
  <body>
<?php 

$command = escapeshellcmd('backend/taco_backend.py');
$output = shell_exec($command);
echo $output;

?>
  </body>
</html>
