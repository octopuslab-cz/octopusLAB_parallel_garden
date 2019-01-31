<?

if (IsSet($_GET["sel"])):$sel=$_GET["sel"];else:$sel="device";endif;
if (IsSet($_GET["place"])):$place=$_GET["place"];else:$place="none";endif;
if (IsSet($_GET["device"])):$device=$_GET["device"];else:$device="240ac4a9";endif;
if (IsSet($_GET["type"])):$type=$_GET["type"];else:$type="esp";endif;
if (IsSet($_GET["limit"])):$limit=$_GET["limit"];else:$limit="200";endif;

include_once 'my_db17.php';
include_once 'mysql_class.php';


//error_reporting(0);

if(MySQL::connect($hostname, $uzivatel, $datpassw, $databaze))
{  //start

switch ($sel) {
    case "device":
          $sql ="SELECT * FROM `iot17` WHERE `device`=\"$device\" ORDER BY `id` DESC LIMIT $limit";
        break;

    case "type":
          $sql ="SELECT * FROM `iot17` WHERE `type`=\"$type\" ORDER BY `id` DESC LIMIT $limit";
        break;

    case "place":
          $sql ="SELECT * FROM `iot17` WHERE `place`=\"$place\" ORDER BY `id` DESC LIMIT $limit";
        break;

   default:
        $sql ="SELECT * FROM `iot17` ORDER BY `id` DESC LIMIT $limit";
}

$json_data=array();//create the array 


$queryTable = MySQL::query($sql);
while($row = $queryTable->fetch()) {
 
    /*$vznik = Date("Y-m-d",$row["id"]);
    $vznikH = Date("H:i",$row["id"]);
    echo "<td>".$row["id"]."</td>";
    echo "<td>$vznik | $vznikH</td>";
    //echo "<td>".$row["place"]."</td>";
    $rowplace=$row["place"];
    echo "<td><a href=http://www.octopusengine.org//api/hydrop?sel=place&place=$rowplace>$rowplace</a></td>";
    $sn=$row["device"];
    echo "<td><a href=http://www.octopusengine.org//api/hydrop?sel=device&device=$sn>$sn</a></td>";
    $rowtype = $row["type"];
    echo "<td><a href=http://www.octopusengine.org//api/hydrop?sel=type&type=$rowtype>$rowtype</a></td>";

    $val =  $row["value"];
    echo "<td>$val</td>";
  
    echo "<br />";*/
    $json_array['id']=$row['id'];  
    $json_array['place']=$row['place'];  
    $json_array['device']=$row['device'];
    $json_array['type']=$row['type'];
    $json_array['value']=$row['value']; 
    array_push($json_data,$json_array);     
    }
    
    echo json_encode($json_data); 
    
}  //end

?>

