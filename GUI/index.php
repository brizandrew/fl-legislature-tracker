<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name=viewport content="width=device-width, initial-scale=1">
	<title>FL Vote Tracker</title>
	<link rel="stylesheet" href="css/style.css">
	<link rel="stylesheet" href="js/chosen/chosen.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"> </script>
	<script src="js/chosen/chosen.jquery.min.js"></script>
	<script src="js/VoteRecord.js"></script>
	<script src="js/main.js"></script>
	<link rel='shortcut icon' type='image/x-icon' href='favs/favicon.ico'/>
</head>
<body>
	<div id="container">
		<h1>2016 FL Legislator Voting Record</h1>
		<div id="explanation">
			<p>Welcome to the Florida Congress politician tracker. Select a member of Florida's House or Senate below to see how they voted in the 2016 legislative session. See the key below for help on the types of votes.</p>
		</div>
		<div id="selectContainer">
		<select data-placeholder="Congressman" class="chosen-select" style="width:100%;" tabindex="18" id="congressmanSelect">
            <option value=""></option>
   		</select>
   		<button id="searchButton">Search</button>
   		</div>
   		<ul id="results">
   			<ul class="result yea">
   				<li><h5><a href="">Yay Vote: Bill Name and Number Would Go Here</a></h5></li>
   				<li class="vote">Y</li>
   				<li>This box style indicates the legislator voted to pass the bill ("Yay"). Click the bill number/name to go to the official bill page on the Florida House of Representatives website. Click "Full Text" below to go to the official bill document. The rest of the text here is filler text. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lobortis, leo nec tristique accumsan, eros quam ultricies enim, pharetra pulvinar elit arcu sed justo.</li>
   				<li class="fullTextLink"><a href="">Full Text</a></li>
   			</ul>
   			<ul class="result nay">
   				<li><h5><a href="">Nea Vote: Bill Name and Number Would Go Here</a></h5></li>
   				<li class="vote">N</li>
   				<li>This box style indicates the legislator voted to not pass the bill ("Nea"). Click the bill number/name to go to the official bill page on the Florida House of Representatives website. Click "Full Text" below to go to the official bill document. The rest of the text here is filler text. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lobortis, leo nec tristique accumsan, eros quam ultricies enim, pharetra pulvinar elit arcu sed justo.</li>
   				<li class="fullTextLink"><a href="">Full Text</a></li>
   			</ul>
   			<ul class="result abstain">
   				<li><h5><a href="">Abstain Vote: Bill Name and Number Would Go Here</a></h5></li>
   				<li class="vote">A</li>
   				<li>This box style indicates the legislator did not vote on the bill ("Abstain"). Click the bill number/name to go to the official bill page on the Florida House of Representatives website. Click "Full Text" below to go to the official bill document. The rest of the text here is filler text. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lobortis, leo nec tristique accumsan, eros quam ultricies enim, pharetra pulvinar elit arcu sed justo.</li>
   				<li class="fullTextLink"><a href="">Full Text</a></li>
   			</ul>
   			<ul class="result none">
   				<li><h5><a href="">No Vote Taken: Bill Name and Number Would Go Here</a></h5></li>
   				<li class="vote"></li>
   				<li>This box style indicates there was no vote taken on the bill. Click the bill number/name to go to the official bill page on the Florida House of Representatives website. Click "Full Text" below to go to the official bill document. The rest of the text here is filler text. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lobortis, leo nec tristique accumsan, eros quam ultricies enim, pharetra pulvinar elit arcu sed justo.</li>
   				<li class="fullTextLink"><a href="">Full Text</a></li>
   			</ul>
   		</ul><!-- close results -->
   		<div style="clear: both"></div>
	</div><!-- close container -->
</body>
</html>