<?php include 'database.php'; ?>

<?php

if (isset($_POST['lname'])) {
	$lname = sanitizeMySQL($conn, $_POST['lname']);
	$query = "SELECT billid, name, number, vote, summary, url, fullTextURL
				FROM votes
				JOIN bills
				ON votes.billid = bills.id
				WHERE votes.congressman = ?
				ORDER BY bills.id";

	$stmt = mysqli_prepare($conn, $query);

    mysqli_stmt_bind_param($stmt, 's', $lname);
    mysqli_stmt_execute($stmt);

	mysqli_stmt_bind_result($stmt, $billid, $name, $number, $vote, $summary, $url, $fullTextURL);

	$output = "{";
	while (mysqli_stmt_fetch($stmt)) {
		$output = $output.'"'.$billid.'":{';
		$output = $output.'"name":"'.$name.'",';
		$output = $output.'"number":"'.$number.'",';
		$output = $output.'"vote":"'.$vote.'",';
		$output = $output.'"summary":"'.sanitizeOutput($summary).'",';
		$output = $output.'"url":"'.$url.'",';
		$output = $output.'"fullTextURL":"'.$fullTextURL.'"';
		$output = $output.'},';
    };
    $output = substr($output, 0, -1);
	$output = $output.'}';
	echo $output;


	mysqli_stmt_close($stmt);
	mysqli_close($conn);
}

function sanitizeMySQL($conn, $var) {
    $var = strip_tags($var);
    $var = mysqli_real_escape_string($conn, $var);
    return $var;
}

function sanitizeOutput($str){
	$str = str_replace('"', '\"', $str);
	$str = preg_replace('/[\x00-\x1F\x80-\xFF]/', '', $str);
	return $str;
}

?>