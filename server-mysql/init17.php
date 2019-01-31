<?
//-----------------------------
//init17 - IoT.. etc.
//-----------------------------
?>
<HTML><HEAD>
<META content="text/html; charset=UTF8" http-equiv=Content-Type>
 <link href="../main_s.css" rel="StyleSheet" type="text/css">
<title>tab.info - init mysql</title>
</HEAD> 
octopusengine.org | scripts<br /><hr />
| <a href=tabbrow.php>tabbrow</a> | <a href=list.php>list</a> |<br /> 

<?                             
include_once 'my_db17.php';      //pristup k db
include_once 'mysql_class.php';  //prace s db
//error_reporting(0);

if(MySQL::connect($hostname, $uzivatel, $datpassw, $databaze)) {  //start
  echo "Připojeno do db";
   
  echo "<hr> init17.php > init table<br />";
  $sql = "create table iot17 (id int, place varchar(8), device varchar(8), type varchar(8), value int, notice varchar(32), klic1 varchar(1), klic2 varchar(2), num3 int)";
  if($query = MySQL::query($sql)) echo  $sql."OK<br />"; 
} //end