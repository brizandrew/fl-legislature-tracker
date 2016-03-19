<?php include 'database.php'; ?>

<?php
	$results = array();

	$query = "SELECT fname, lname FROM representatives";
	$stmt = mysqli_query($conn, $query);
	while( $row = mysqli_fetch_assoc($stmt) ){
		array_push($results, $row['fname']."|".$row['lname']);
	};

	$query = "SELECT fname, lname FROM senators";
	$stmt = mysqli_query($conn, $query);
	while( $row = mysqli_fetch_assoc($stmt) ){
		array_push($results, $row['fname']."|".$row['lname']);
	};

	mysqli_close($conn);
	echo json_encode(utf8ize($results));

	# Code snippet courtesy Matthieu Riegler found: http://stackoverflow.com/questions/19361282/why-would-json-encode-returns-an-empty-string
	function utf8ize($d) {
	    if (is_array($d)) {
	        foreach ($d as $k => $v) {
	            $d[$k] = utf8ize($v);
	        }
	    } else if (is_string ($d)) {
	        return utf8_encode($d);
	    }
	    return $d;
	}
?>