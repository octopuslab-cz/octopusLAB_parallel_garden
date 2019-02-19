<?
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Origin: *");

if (IsSet($_GET["sel"])):$sel=$_GET["sel"];else:$sel="sgroup";endif;
if (IsSet($_GET["place"])):$place=$_GET["place"];else:$place="none";endif;
if (IsSet($_GET["device"])):$device=$_GET["device"];else:$device="240ac4a9";endif;
if (IsSet($_GET["type"])):$type=$_GET["type"];else:$type="esp";endif;
if (IsSet($_GET["limit"])):$limit=$_GET["limit"];else:$limit="200";endif;

include_once 'my_db17.php';
include_once 'mysql_class.php';

//error_reporting(0);
if(MySQL::connect($hostname, $uzivatel, $datpassw, $databaze))
{  //start
        //$sql ="SELECT * FROM `iot17` WHERE `device`=\"$device\" ORDER BY `type` DESC GROUP BY `type`";
        //$sql ="SELECT id,place,device,type FROM `iot17` WHERE `device`=\"$device\"  ORDER BY `id` DESC GROUP BY `type`";
        //$sql ="SELECT id,place,device,type FROM `iot17` WHERE `device`=\"$device\" GROUP BY `type`";
        $sql ="SELECT *
        FROM (
            SELECT id,place,device,type,value FROM `iot17` WHERE `device`=\"$device\"
            ORDER BY `id` DESC
        ) AS sub
        GROUP BY `type`";
}

$json_data=array();//create the array
$queryTable = MySQL::query($sql);
while($row = $queryTable->fetch()) {
    /*$vznik = Date("Y-m-d",$row["id"]);
    $vznikH = Date("H:i",$row["id"]);
    echo "<br />";*/
    $json_array['id']=$row['id'];
    $json_array['place']=$row['place'];
    //$json_array['device']=$row['device'];
    $json_array['type']=$row['type'];
    $json_array['value']=$row['value'];
    array_push($json_data,$json_array);
    }
    echo json_encode($json_data);
//end
?>
