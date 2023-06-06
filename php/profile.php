<?php
	require_once __DIR__ . '/vendor/autoload.php';

	// https://www.mongodb.com/docs/php-library/current/tutorial/connecting/
	$client = new MongoDB\Client('mongodb://127.0.0.1:27017/');
	// https://www.mongodb.com/docs/php-library/current/tutorial/server-selection/
	$database = $client->user_database;
	// https://www.mongodb.com/docs/php-library/current/tutorial/crud/
	$collection = $database->users;
	/*
	$collection->drop();
	$insertManyResult = $collection->insertMany([
	    [
	        '_id' => 'U1IT00001',
	        'uname' => 'Alice',
	        'pw' => 'qwerty123',
	        'credit_card' => '4775462337863648',
	    ],
	    [
	        '_id' => 'U1IT00002',
	        'uname' => 'Bob',
	        'pw' => 'correct-horse-battery-staple',
	        'credit_card' => '4775468105507721',
	    ],
	]);
	*/

	$user_document = $collection->findOne(array("uname"=>$_GET["uname"] ?? "", "pw"=>$_GET["pw"] ?? ""));
?>
<html>
	<head>
		<title><?php if (is_null($user_document)) {echo "Wrong Credentials";} else {echo "Profile";} ?></title>
	</head>
	<body>
		<?php
			if (is_null($user_document)) {
				echo "<h1>Wrong Credentials</h1>";
			} else {
				echo "<h1>Profile</h1>";
				echo "Username: " . $user_document["uname"] . "<br><br>";
				echo "Credit Card: " . $user_document["credit_card"] . "<br><br>";
			}
		?>
	</body>
</html>
