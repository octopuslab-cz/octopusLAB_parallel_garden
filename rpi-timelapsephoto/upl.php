<?php

$target_dir = "data/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$uploadkey = "KEY";

$imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));
// Check if image file is a actual image or fake image
if(isset($_POST["submit"])) {
    if ($_POST["authkey"] != "$uploadkey") { 
    echo "Bad auth key!<br />";
    return;
    }
    $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
    if($check !== false) {
        echo "File is an image - " . $check["mime"] . ".<br />";
        $uploadOk = 1;
if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
        echo "The file ". basename( $_FILES["fileToUpload"]["name"]). " has been uploaded.<br />";
	return;
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
    } else {
        echo "File is not an image.";
        $uploadOk = 0;
    }
}

?>
<br />
<form action="upl.php" method="post" enctype="multipart/form-data">
    Select image to upload:<br />
    <input type="file" name="fileToUpload" id="fileToUpload" /><br />
    Entery auth key: <input type="password" name="authkey" /><br />
    <input type="submit" value="Upload Image" name="submit" />
</form>

