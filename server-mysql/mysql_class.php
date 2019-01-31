<?php
class MySQL {

    private static $pdos = array();
    private static $selected_server = "default";

    private static $host;
    private static $user;
    private static $pass;
    private static $db;
    private static $charset = "utf8";
    private static $prepared_sqls = array();

    public static function setCharset($charset) {
        self::$charset = $charset;
    }

    public static function connect($host, $user, $pass, $db, $pdoName = "default") {
        self::$host = $host;
        self::$user = $user;
        self::$pass = $pass;
        self::$db = $db;
        try {
            self::$pdos[$pdoName] = new \PDO("mysql:host=" . self::$host . ";dbname=" . self::$db . ";charset=" . self::$charset, self::$user, self::$pass);
            return true;
        } catch (\PDOException $ex) {
            echo "MySQL Error ! (Error code: " . $ex->getCode() . ", Message: " . $ex->getMessage() . ")";
        }
    }

    public static function setPdoName($name) {
        self::$selected_server = $name;
    }

    public static function query($query) {
        $args = func_get_args();
        array_shift($args);
        if(sizeof($args) > 0) {
        	if(is_array($args[0])) {
        		$args = $args[0];
        	}
        }
        $response = self::$pdos[self::$selected_server]->prepare($query);
        $response->execute($args);
        self::$selected_server = "default";
        return $response;
    }

    public static function getLastInsertedId() {
      return self::getPDO()->lastInsertId();
    }

    public static function getPDO() {
        return self::$pdos[self::$selected_server];
    }

}
