<?
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Origin: *");

if (IsSet($_GET["sel"])):$sel=$_GET["sel"];else:$sel="device";endif;
if (IsSet($_GET["place"])):$place=$_GET["place"];else:$place="none";endif;
if (IsSet($_GET["device"])):$device=$_GET["device"];else:$device="240ac4a9";endif;
if (IsSet($_GET["type"])):$type=$_GET["type"];else:$type="esp";endif;
if (IsSet($_GET["limit"])):$limit=$_GET["limit"];else:$limit="200";endif;

include_once 'my_db17.php';
include_once 'mysql_class.php';

//error_reporting(0);

if(MySQL::connect($hostname, $uzivatel, $datpassw, $databaze)) {  //start
    switch ($sel) {
        case "device":
              $sql ="SELECT * FROM `iot17` WHERE `device`=\"$device\" ORDER BY `id` DESC LIMIT $limit";
              $sql_fields="SELECT type FROM `iot17` WHERE `device`=\"$device\" GROUP BY `type`;";
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

    $json = array();
    $json_data = array(); //create the array
    $json_fields = array();

    $queryTable = MySQL::query($sql_fields);
    while($row = $queryTable->fetch()) {
      $json_fields[$row['type']] = array();
      switch (substr($row['type'], 0, 1)) {
        case 'l':
           $json_fields[$row['type']]['color'] = 'green';
           $json_fields[$row['type']]['label'] = 'Light';
           break;
        case 'm':
          $json_fields[$row['type']]['color'] = 'blue';
          $json_fields[$row['type']]['label'] = 'Moisture';
          break;
        case 't':
          $json_fields[$row['type']]['color'] = 'red';
          $json_fields[$row['type']]['label'] = 'Temperature';
          break;
        default:
          $json_fields[$row['type']]['color'] = 'black';
          $json_fields[$row['type']]['label'] = 'Dummy';
          break;
      }
    }

    $queryTable = MySQL::query($sql);
    while($row = $queryTable->fetch()) {
        $json_array = array();
        /*$vznik = Date("Y-m-d",$row["id"]);
        $vznikH = Date("H:i",$row["id"]);
        echo "<br />";*/
        $json_array['timestamp']=intval($row['id']);
        $json_array[$row['type']]=intval($row['value']);

        if ( $place == "none" ) {
          $place=$row['place'];
        }

          array_push($json_data,$json_array);
    }


    $json['device'] = $device;
    $json['place'] = $place;
    $json['fields'] = array();
    $json['data'] = array();

    array_push($json['fields'], $json_fields);
    array_push($json['data'], $json_data);

    echo json_encode(array($json));

}  //end

?>
